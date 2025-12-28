# Quick Start Guide - Video Classification Dataset

<!--
Project: Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World
-->

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Create Directory Structure

```bash
python scripts/download_sample_data.py --create-structure
```

This creates `raw_videos/` with category folders.

### Step 3: Add Your Videos

Place your video files in the appropriate category folders:

```
raw_videos/
├── action/
│   └── your_video.mp4
├── comedy/
│   └── your_video.mp4
└── ...
```

**Need videos?** See [DATASET_GUIDE.md](DATASET_GUIDE.md) for free video sources.

### Step 4: Organize Dataset

```bash
python scripts/organize_dataset.py --input raw_videos --output data
```

This automatically splits videos into train (70%), test (20%), and validation (10%) sets.

### Step 5: Verify Dataset

```bash
python scripts/create_sample_metadata.py --summary
```

## 📁 Current Dataset Structure

Your dataset is now organized as:

```
data/
├── train/          # 70% of videos
│   ├── action/
│   ├── comedy/
│   ├── drama/
│   ├── sports/
│   ├── documentary/
│   ├── news/
│   ├── music/
│   └── education/
├── test/           # 20% of videos
│   └── [same categories]
└── validation/     # 10% of videos
    └── [same categories]
```

## 🎯 Next Steps

### Option 1: Extract Frames

```bash
python scripts/extract_frames.py --input data/train --output frames/train
```

### Option 2: Process Videos

```bash
python scripts/process_videos.py --input raw_videos --output data/train
```

### Option 3: Use the Dataset

```python
from utils.dataset_utils import get_videos_by_category

# Get videos by category
videos = get_videos_by_category('data/train')
print(videos)
```

## 📊 Check Dataset Statistics

```bash
python scripts/create_sample_metadata.py --summary
```

Or in Python:

```python
from utils.dataset_utils import get_dataset_statistics

stats = get_dataset_statistics('data/train')
print(stats)
```

## 🎬 Example Usage

See complete examples in the `examples/` directory:

```bash
cd examples
python video_loader_example.py
python classification_example.py
```

## 📚 More Information

- **Full Guide**: See [DATASET_GUIDE.md](DATASET_GUIDE.md)
- **Usage**: See [USAGE.md](USAGE.md)
- **API Docs**: See [README.md](README.md)

## 🆘 Need Help?

- Website: https://rskworld.in
- Email: help@rskworld.in
- Phone: +91 93305 39277

**RSK World**
- Founder: Molla Samser
- Designer & Tester: Rima Khatun

