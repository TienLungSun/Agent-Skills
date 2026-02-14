import torch
import torchvision
from torchvision.models.detection import keypointrcnn_resnet50_fpn, KeypointRCNN_ResNet50_FPN_Weights
from torchvision.transforms import functional as F
import cv2
import numpy as np
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='PyTorch KeypointRCNN Pose Estimation')
    parser.add_argument('--image', required=True, help='Path to input image')
    parser.add_argument('--output', default='output.jpg', help='Path to output image')
    parser.add_argument('--threshold', type=float, default=0.8, help='Confidence threshold')
    parser.add_argument('--device', default=None, help='Device to run on (cuda or cpu)')
    args = parser.parse_args()

    # Select device
    if args.device:
        device = torch.device(args.device)
    else:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load model
    print("Loading model...")
    weights = KeypointRCNN_ResNet50_FPN_Weights.DEFAULT
    model = keypointrcnn_resnet50_fpn(weights=weights)
    model.to(device)
    model.eval()

    # Load image
    print(f"Loading image: {args.image}")
    try:
        # Load using OpenCV to get original image for drawing
        img_cv2 = cv2.imread(args.image)
        if img_cv2 is None:
            print(f"Error: Could not load image from {args.image}")
            sys.exit(1)
        # Convert BGR to RGB for PyTorch
        img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
        # Convert to Tensor
        img_tensor = F.to_tensor(img_rgb).to(device)
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)

    # Inference
    print("Running inference...")
    with torch.no_grad():
        output = model([img_tensor])[0]

    # Process results
    scores = output['scores'].cpu().numpy()
    # Filter by threshold
    keep = scores > args.threshold
    
    if not np.any(keep):
        print("No persons detected above threshold.")
        sys.exit(0)

    boxes = output['boxes'][keep].cpu().numpy()
    keypoints = output['keypoints'][keep].cpu().numpy()
    keypoints_scores = output['keypoints_scores'][keep].cpu().numpy()

    # Image dimensions for coordinate transformation
    height, width = img_cv2.shape[:2]
    center_x = width / 2
    center_y = height / 2

    # Keypoint names map (COCO format)
    keypoint_names = [
        'nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
        'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
        'left_knee', 'right_knee', 'left_ankle', 'right_ankle'
    ]
    
    # Skeleton connections for drawing
    skeleton = [
        (0, 1), (0, 2), (1, 3), (2, 4), # Face
        (5, 6), (5, 7), (7, 9), (6, 8), (8, 10), # Arms
        (5, 11), (6, 12), (11, 12), # Body
        (11, 13), (13, 15), (12, 14), (14, 16) # Legs
    ]
    
    # Required keypoints to print
    required_keypoints = {
        'nose': 0,
        'left_shoulder': 5,
        'right_shoulder': 6,
        'left_hip': 11,
        'right_hip': 12,
        'left_knee': 13,
        'right_knee': 14
    }

    # Transform and Print
    for i, (kp_set, kp_score_set) in enumerate(zip(keypoints, keypoints_scores)):
        print(f"\nPerson {i+1}:")
        
        # Draw bounding box
        box = boxes[i].astype(int)
        cv2.rectangle(img_cv2, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

        # Draw skeleton
        for start_idx, end_idx in skeleton:
            if kp_score_set[start_idx] > 0.5 and kp_score_set[end_idx] > 0.5:
                pt1 = (int(kp_set[start_idx][0]), int(kp_set[start_idx][1]))
                pt2 = (int(kp_set[end_idx][0]), int(kp_set[end_idx][1]))
                cv2.line(img_cv2, pt1, pt2, (255, 0, 0), 2)

        # Draw and print keypoints
        for name, idx in required_keypoints.items():
            x_pixel, y_pixel = kp_set[idx][:2]
            score = kp_score_set[idx]

            # Only print/draw if detected with some confidence
            if score > 0.5:
                # Coordinate Transformation: Center origin, Y-up
                # x_new = x_pixel - center_x
                # y_new = center_y - y_pixel
                x_trans = x_pixel - center_x
                y_trans = center_y - y_pixel

                print(f"  {name.replace('_', ' ').title()}: ({x_trans:.1f}, {y_trans:.1f})")

                # Draw point
                cv2.circle(img_cv2, (int(x_pixel), int(y_pixel)), 4, (0, 0, 255), -1)
            else:
                 print(f"  {name.replace('_', ' ').title()}: Not detected")

    # Save output
    cv2.imwrite(args.output, img_cv2)
    print(f"\nResult saved to {args.output}")

if __name__ == "__main__":
    main()
