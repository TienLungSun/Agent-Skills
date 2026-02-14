import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import argparse
import os
import urllib.request

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task"
MODEL_NAME = "pose_landmarker_heavy.task"

def download_model(model_path):
    if not os.path.exists(model_path):
        print(f"Downloading model to {model_path}...")
        try:
            urllib.request.urlretrieve(MODEL_URL, model_path)
            print("Download complete.")
        except Exception as e:
            print(f"Error downloading model: {e}")
            return False
    return True

def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Connections for Pose Landmarker (33 keypoints)
    # Sourced from MediaPipe documentation / common knowledge
    # We can perform a subset of connections for visualization
    CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8),
        (9, 10), (11, 12), (11, 13), (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),
        (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20),
        (11, 23), (12, 24), (23, 24), (23, 25), (24, 26), (25, 27), (26, 28),
        (27, 29), (28, 30), (29, 31), (30, 32), (27, 31), (28, 32)
    ]

    for pose_landmarks in pose_landmarks_list:
        # Draw connections
        for connection in CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            
            start_landmark = pose_landmarks[start_idx]
            end_landmark = pose_landmarks[end_idx]
            
            h, w, _ = annotated_image.shape
            start_point = (int(start_landmark.x * w), int(start_landmark.y * h))
            end_point = (int(end_landmark.x * w), int(end_landmark.y * h))
            
            cv2.line(annotated_image, start_point, end_point, (255, 255, 255), 2) # White lines

        # Draw landmarks
        for idx, landmark in enumerate(pose_landmarks):
            h, w, _ = annotated_image.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(annotated_image, (cx, cy), 4, (0, 0, 255), -1) # Red dots

    return annotated_image

def process_image(input_path, output_path, model_path):
    if not download_model(model_path):
        return

    # Create PoseLandmarker
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=False)
    detector = vision.PoseLandmarker.create_from_options(options)

    # Load image
    # MediaPipe Image accepts RGB, OpenCV reads BGR
    cv_image = cv2.imread(input_path)
    if cv_image is None:
        print(f"Error: Could not read image from {input_path}")
        return

    image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

    # Detect pose
    detection_result = detector.detect(mp_image)

    if not detection_result.pose_landmarks:
        print("No pose landmarks detected.")
        return

    # Draw landmarks
    annotated_image_rgb = draw_landmarks_on_image(image_rgb, detection_result)
    annotated_image_bgr = cv2.cvtColor(annotated_image_rgb, cv2.COLOR_RGB2BGR)

    # Coordinate Transformation and Tracking
    height, width, _ = cv_image.shape
    center_x = width / 2
    center_y = height / 2

    keypoints_map = {
        'Nose': 0,
        'Left Shoulder': 11,
        'Right Shoulder': 12,
        'Left Hip': 23,
        'Right Hip': 24,
        'Left Knee': 25,
        'Right Knee': 26
    }

    print(f"{'Keypoint':<15} | {'X':<10} | {'Y':<10}")
    print("-" * 41)

    # Assuming single person detection, take the first pose
    pose_landmarks = detection_result.pose_landmarks[0]

    for name, idx in keypoints_map.items():
        landmark = pose_landmarks[idx]
        
        pixel_x = landmark.x * width
        pixel_y = landmark.y * height
        
        # Transformation: (0,0) at center, X right, Y up
        transformed_x = pixel_x - center_x
        transformed_y = center_y - pixel_y
        
        print(f"{name:<15} | {transformed_x:<10.2f} | {transformed_y:<10.2f}")

    # Save output
    if output_path:
        cv2.imwrite(output_path, annotated_image_bgr)
        print(f"\nAnnotated image saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MediaPipe Pose Estimation on Image (Tasks API)")
    parser.add_argument("--input", required=True, help="Path to input image")
    parser.add_argument("--output", help="Path to output image (optional)")
    
    args = parser.parse_args()
    
    # Determine model path (in the same directory as this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Actually, let's put it in the parent directory or same directory.
    # We'll put it in the skill root (parent of script) to be clean.
    skill_root = os.path.dirname(script_dir)
    model_path = os.path.join(skill_root, MODEL_NAME)

    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
    else:
        # Determine output path if not provided
        if not args.output:
            base, ext = os.path.splitext(args.input)
            if ext.lower() == '.jfif':
                ext = '.jpg'
            output_path = f"{base}_annotated{ext}"
        else:
            output_path = args.output
            
        process_image(args.input, output_path, model_path)
