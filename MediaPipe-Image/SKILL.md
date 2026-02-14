---
name: Pose Estimation Image
description: Detects human pose landmarks in an image using MediaPipe Tasks API, transforms coordinates to center-origin, and visualizes the results.
---

# Pose Estimation Image Skill

This skill uses Google MediaPipe (Tasks API) to perform pose estimation on a single image.

## Features
-   Detects 33 pose landmarks using `pose_landmarker_heavy.task` model.
-   **Automatic Model Download**: The script automatically downloads the required model file if it's missing.
-   Draws landmarks and connections on the image.
-   Transforms keypoint coordinates to a coordinate system where:
    -   (0, 0) is the center of the image.
    -   X-axis increases to the right.
    -   Y-axis increases upwards.
-   Prints the transformed coordinates for:
    -   Nose
    -   Shoulders (Left, Right)
    -   Hips (Left, Right)
    -   Knees (Left, Right)

## Usage

1.  Place your input image in the same directory or provide the path.
2.  Run the script:

```bash
python scripts/process_image.py --input "path/to/your/image.jpg"
# Optional: Specify output path
python scripts/process_image.py --input "image.jpg" --output "output.jpg"
```

## Requirements
-   Python 3.x
-   See `requirements.txt` for dependencies.
