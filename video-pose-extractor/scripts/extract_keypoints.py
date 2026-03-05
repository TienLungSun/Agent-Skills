import cv2
import mediapipe as mp
import pandas as pd
import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Extract MediaPipe pose keypoints from a video.")
    parser.add_argument("input_video", help="Path to the input video file")
    parser.add_argument("--output_csv", help="Path to save the output CSV. Defaults to input_video_name_keypoints.csv", default=None)
    parser.add_argument("--output_video", help="Path to save the output video. Defaults to input_video_name_output.mp4", default=None)
    parser.add_argument("--display", action="store_true", help="Display the video while processing")
    
    args = parser.parse_args()

    input_path = args.input_video
    if not os.path.isfile(input_path):
        print(f"Error: Input video '{input_path}' does not exist.")
        sys.exit(1)

    base_name, ext = os.path.splitext(os.path.basename(input_path))
    dir_name = os.path.dirname(input_path) or '.'

    output_csv = args.output_csv or os.path.join(dir_name, f"{base_name}_keypoints.csv")
    output_video = args.output_video or os.path.join(dir_name, f"{base_name}_output.mp4")

    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    # Open video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video '{input_path}'")
        sys.exit(1)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # type: ignore
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    data = []
    frame_idx = 0

    print(f"Processing video: {input_path}")
    print(f"Resolution: {width}x{height} at {fps} FPS")

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=2 # Highest accuracy model
    ) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # To improve performance, optionally mark the frame as not writeable to
            # pass by reference.
            frame.flags.writeable = False
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            # Draw the pose annotation on the frame.
            frame.flags.writeable = True

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                )

                # Extract landmarks
                row = {'frame': frame_idx, 'timestamp_ms': cap.get(cv2.CAP_PROP_POS_MSEC)}
                landmarks = results.pose_landmarks.landmark
                
                # Iterate through all 33 keypoints
                for idx, lm in enumerate(landmarks):
                    # Mapping integer index to keypoint name
                    name = mp_pose.PoseLandmark(idx).name
                    row[f'{name}_x'] = lm.x
                    row[f'{name}_y'] = lm.y
                    row[f'{name}_z'] = lm.z
                    row[f'{name}_visibility'] = lm.visibility

                data.append(row)

            # Write the frame with annotations
            out.write(frame)

            if args.display:
                cv2.imshow('MediaPipe Pose', frame)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
                    
            if frame_idx % 100 == 0:
                print(f"Processed {frame_idx}/{frame_count} frames...")
                
            frame_idx += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Save data to CSV
    if data:
        df = pd.DataFrame(data)
        df.to_csv(output_csv, index=False)
        print(f"\nSuccess! Extraction complete.")
        print(f"Saved keypoints data to: {output_csv}")
        print(f"Saved annotated video to: {output_video}")
    else:
        print("\nNo humans were detected in the video. CSV not created.")

if __name__ == "__main__":
    main()
