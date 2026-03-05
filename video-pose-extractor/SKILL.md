---
name: video-pose-extractor
description: "Extracts human pose keypoints from a video using MediaPipe, saves to CSV, and generates an annotated output video."
category: computer-vision
risk: safe
tags: "[video, pose-estimation, mediapipe, computer-vision, keypoints]"
---

# video-pose-extractor

## Purpose

To easily process videos to extract human pose keypoints (such as shoulders, elbows, wrists, hips, knees, ankles) using Google's MediaPipe framework. It outputs the raw keypoint coordinates into a CSV file for data analysis and creates an annotated video visualizing the detected keypoints to verify the results.

## When to Use This Skill

This skill should be used when:
- The user provides an input video and asks to extract or track human poses/keypoints.
- The user needs a CSV containing X, Y, Z, and visibility coordinates for all 33 MediaPipe pose landmarks across each frame of a video.
- The user wants a visualization (annotated video) of the pose tracking results for verification.

## Prerequisites

Before running the skill, ensure you have installed the required dependencies from the skill folder:
```bash
pip install -r {skill_path}/requirements.txt
```
*(Dependencies: `opencv-python`, `mediapipe`, `pandas`)*

## Execution Instructions

To execute this skill, run the provided Python script located in the `scripts/` directory:

```bash
python {skill_path}/scripts/extract_keypoints.py <path_to_input_video.mp4>
```

### Optional Arguments:
- `--output_csv <path>` : Define a custom path for the generated CSV keypoint data.
- `--output_video <path>` : Define a custom path for the annotated output video.
- `--display` : Open a preview window showing the processing in real-time (can be slower).

**Example Execution:**
```bash
python scripts/extract_keypoints.py C:/Users/user/Desktop/running.mp4 --output_csv C:/Users/user/Desktop/running_data.csv
```

## Output Artifacts

Running this skill generates two main files by default alongside the input video:
1. `<video_name>_keypoints.csv` : Contains the frame number, timestamp in ms, and 33 sets of X, Y, Z, and visibility values for each MediaPipe landmark.
2. `<video_name>_output.mp4` : The output video with the MediaPipe skeleton drawn over the detected human body.
