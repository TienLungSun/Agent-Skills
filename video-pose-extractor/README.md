# Video Pose Extractor Skill

A command-line skill designed to track and extract human pose keypoints from a video using [MediaPipe](https://developers.google.com/mediapipe).

## Features
- Detects the 33 3D landmarks of a human body using the MediaPipe Pose model.
- Saves all 33 keypoints (X, Y, Z, and visibility) per frame into a structured **CSV file**.
- Draws the skeleton connections directly onto the video and exports the **annotated video** as an `.mp4` file for easy verification.

## Installation

1. Make sure you have Python installed.
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

You can use the AI assistant to invoke this skill ("extract keypoints from my video"), or run it manually:

```bash
python scripts/extract_keypoints.py path/to/your/video.mp4
```

### Advanced Usage
Override the default output paths or enable real-time display:
```bash
python scripts/extract_keypoints.py input.mp4 --output_csv data.csv --output_video skeleton.mp4 --display
```

## Outputs
By default, the script places the outputs in the same directory as the input video:
- `video_keypoints.csv`
- `video_output.mp4`
