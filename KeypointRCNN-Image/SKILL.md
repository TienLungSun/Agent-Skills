---
name: PyTorch KeypointRCNN Pose Estimation
description: Detects human keypoints in an image using PyTorch's KeypointRCNN model, transforms coordinates, and visualizes results.
---

# PyTorch KeypointRCNN Pose Estimation

This skill uses a pre-trained KeypointRCNN model from `torchvision` to detect human keypoints in an image. It then transforms the coordinates to be relative to the image center (with Y-axis pointing up) and visualizes the results on the input image.

## Requirements

- Python 3.8+
- PyTorch
- TorchVision
- OpenCV
- NumPy
- Matplotlib (optional, for display if needed)

## Installation

Install the required dependencies:

```bash
pip install -r scripts/requirements.txt
```

## Usage

Run the `detect_pose.py` script with an input image path:

```bash
python scripts/detect_pose.py --image path/to/your/image.jpg
```

### Arguments

- `--image`: Path to the input image file (required).
- `--output`: Path to save the output image (optional, default: `output.jpg`).
- `--threshold`: Confidence threshold for detection (optional, default: `0.8`).
- `--device`: Device to run the model on ('cpu' or 'cuda') (optional, default: automatically selected).

## output

The script will:
1.  Print the transformed coordinates of the following keypoints for each detected person:
    -   Nose
    -   Shoulder (Left, Right)
    -   Hip (Left, Right)
    -   Knee (Left, Right)
2.  Save an image with the detected keypoints and skeleton drawn on it to the specified output path.

## Coordinate System

The output coordinates are transformed as follows:
-   **Origin (0, 0)**: The center of the input image.
-   **X-axis**: Points to the right (positive X is right of center).
-   **Y-axis**: Points upwards (positive Y is above center).

## Example Output

```text
Person 1:
  Nose: (10.5, 50.2)
  Left Shoulder: (25.1, 40.8)
  Right Shoulder: (-5.2, 42.1)
  ...
```
