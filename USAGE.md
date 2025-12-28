# Video Classification Dataset - Usage Guide

<!--
Project: Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World
-->

## Quick Start

### 1. Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

### 2. Dataset Organization

Organize your raw videos into category folders, then split into train/test/validation:

```bash
python scripts/organize_dataset.py --input raw_videos --output data
```

### 3. Process Videos

Resize and normalize videos:

```bash
python scripts/process_videos.py --input raw_videos --output data/train
```

### 4. Extract Frames

Extract frames from videos:

```bash
python scripts/extract_frames.py --input data/train --output frames/train
```

## Detailed Usage

### Dataset Structure

Your dataset should be organized as follows:

```
raw_videos/
├── category1/
│   ├── video1.mp4
│   ├── video2.mp4
│   └── ...
├── category2/
│   ├── video1.mp4
│   └── ...
└── ...
```

### Scripts

#### 1. organize_dataset.py

Organizes videos into train/test/validation splits:

```bash
python scripts/organize_dataset.py \
    --input raw_videos \
    --output data \
    --train-ratio 0.7 \
    --test-ratio 0.2 \
    --validation-ratio 0.1
```

#### 2. process_videos.py

Processes videos (resize, format conversion):

```bash
python scripts/process_videos.py \
    --input raw_videos \
    --output data/train \
    --config config.yaml
```

#### 3. extract_frames.py

Extracts frames from videos:

```bash
python scripts/extract_frames.py \
    --input data/train \
    --output frames/train \
    --fps 1
```

### Using the Utilities

#### Video Utilities

```python
from utils.video_utils import get_video_info, extract_frame, preprocess_frame

# Get video information
info = get_video_info('path/to/video.mp4')
print(f"Duration: {info['duration']}s")
print(f"Resolution: {info['width']}x{info['height']}")

# Extract a frame
frame = extract_frame('path/to/video.mp4', frame_number=0)

# Preprocess frame for model input
processed = preprocess_frame(frame, size=(224, 224))
```

#### Dataset Utilities

```python
from utils.dataset_utils import (
    get_categories,
    get_videos_by_category,
    create_label_mapping,
    get_dataset_statistics
)

# Get categories
categories = get_categories('data/train')

# Get videos by category
videos_by_category = get_videos_by_category('data/train')

# Create label mapping
label_mapping = create_label_mapping(categories)

# Get statistics
stats = get_dataset_statistics('data/train')
```

### Examples

See the `examples/` directory for complete usage examples:

- `video_loader_example.py`: How to load and process videos
- `classification_example.py`: Example classification pipeline

Run examples:

```bash
cd examples
python video_loader_example.py
python classification_example.py
```

## Configuration

Edit `config.yaml` to customize:

- Dataset paths
- Train/test/validation ratios
- Video processing parameters
- Frame extraction settings
- Category list

## Tips

1. **Video Formats**: Supported formats include MP4, MOV, AVI, MKV
2. **Frame Extraction**: Adjust FPS in config for different frame rates
3. **Memory**: For large datasets, process videos in batches
4. **FFmpeg**: Required for format conversion (install separately)

## Troubleshooting

### FFmpeg not found

Install FFmpeg:
- Windows: Download from https://ffmpeg.org/download.html
- Linux: `sudo apt-get install ffmpeg`
- macOS: `brew install ffmpeg`

### OpenCV errors

Make sure you have the correct OpenCV version:
```bash
pip install opencv-python opencv-contrib-python
```

### Memory issues

Process videos in smaller batches or reduce video resolution in config.

## Contact

For support or questions:
- Website: https://rskworld.in
- Email: help@rskworld.in, support@rskworld.in
- Phone: +91 93305 39277

**RSK World**
- Founder: Molla Samser
- Designer & Tester: Rima Khatun

