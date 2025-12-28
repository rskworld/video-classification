# Video Classification Dataset

<!--
Project: Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World
Description: Video classification dataset with labeled video clips across multiple categories
-->

## Overview

This dataset includes labeled video clips across multiple categories for video classification tasks. Perfect for video understanding, video categorization, and video deep learning applications.

## Features

- Multiple video categories
- Labeled video clips
- Training and test sets
- Frame extraction available
- Ready for video models

## Dataset Structure

```
video-classification/
├── data/
│   ├── train/
│   │   ├── action/
│   │   ├── comedy/
│   │   ├── drama/
│   │   ├── sports/
│   │   ├── documentary/
│   │   ├── news/
│   │   ├── music/
│   │   └── education/
│   ├── test/
│   │   └── [same categories]
│   └── validation/
│       └── [same categories]
├── raw_videos/          # Place your videos here before organizing
│   └── [category folders]
├── frames/              # Extracted frames directory
├── scripts/
│   ├── extract_frames.py
│   ├── process_videos.py
│   ├── organize_dataset.py
│   ├── add_videos.py
│   ├── download_sample_data.py
│   └── create_sample_metadata.py
├── utils/
│   ├── video_utils.py
│   └── dataset_utils.py
├── examples/
│   ├── classification_example.py
│   └── video_loader_example.py
├── requirements.txt
├── config.yaml
├── QUICK_START.md
├── DATASET_GUIDE.md
└── README.md
```

## Technologies Used

- **MP4**: Video format support
- **MOV**: Video format support
- **OpenCV**: Video processing and frame extraction
- **FFmpeg**: Video encoding/decoding and format conversion
- **Python**: Main programming language

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Install FFmpeg (if not already installed):
   - Windows: Download from https://ffmpeg.org/download.html
   - Linux: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`

## Quick Start

1. **Create directory structure:**
   ```bash
   python scripts/download_sample_data.py --create-structure
   ```

2. **Add your videos** to `raw_videos/[category]/` folders

3. **Organize dataset:**
   ```bash
   python scripts/organize_dataset.py --input raw_videos --output data
   ```

See [QUICK_START.md](QUICK_START.md) for detailed instructions.

## Usage

### Adding Videos

**Interactive mode:**
```bash
python scripts/add_videos.py --interactive
```

**Batch mode:**
```bash
python scripts/add_videos.py --source raw_videos/action --target data/train --category action
```

### Dataset Organization

Organize dataset into train/test/validation splits:

```bash
python scripts/organize_dataset.py --input raw_videos --output data
```

### Frame Extraction

Extract frames from videos:

```bash
python scripts/extract_frames.py --input data/train --output frames/train
```

### Video Processing

Process and normalize videos:

```bash
python scripts/process_videos.py --input raw_videos --output data/train
```

### Create Metadata

Generate dataset metadata:

```bash
python scripts/create_sample_metadata.py --summary
```

## Example Usage

See the `examples/` directory for complete usage examples.

## License

Content used for educational purposes only. View Disclaimer at https://rskworld.in

## Contact

**RSK World**
- Website: https://rskworld.in
- Email: help@rskworld.in, support@rskworld.in
- Phone: +91 93305 39277
- Founder: Molla Samser
- Designer & Tester: Rima Khatun

## Disclaimer

This dataset is provided for educational and research purposes only. Please refer to the full disclaimer at https://rskworld.in

