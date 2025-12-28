# Dataset Guide - Adding Real Video Data

<!--
Project: Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World
-->

## Quick Start - Adding Videos

### Step 1: Create Raw Videos Directory

```bash
# Run the helper script to create directory structure
python scripts/download_sample_data.py --create-structure
```

This creates:
```
raw_videos/
├── action/
├── comedy/
├── drama/
├── sports/
├── documentary/
├── news/
├── music/
└── education/
```

### Step 2: Add Your Videos

Place your video files in the appropriate category folders:

```
raw_videos/
├── action/
│   ├── video1.mp4
│   ├── video2.mp4
│   └── ...
├── comedy/
│   ├── video1.mp4
│   └── ...
└── ...
```

### Step 3: Organize Dataset

```bash
# Automatically split into train/test/validation
python scripts/organize_dataset.py --input raw_videos --output data
```

### Step 4: Process Videos (Optional)

```bash
# Resize and normalize videos
python scripts/process_videos.py --input raw_videos --output data/train
```

### Step 5: Extract Frames (Optional)

```bash
# Extract frames for frame-based models
python scripts/extract_frames.py --input data/train --output frames/train
```

## Video Sources

### Free Video Sources

1. **Pexels Videos** (https://www.pexels.com/videos/)
   - Free stock videos
   - Multiple categories
   - High quality

2. **Pixabay Videos** (https://pixabay.com/videos/)
   - Free videos
   - Various categories
   - Good for training

3. **Videvo** (https://www.videvo.net/)
   - Free video clips
   - Multiple categories

4. **YouTube** (with proper permissions)
   - Download using tools like `yt-dlp`
   - Ensure you have rights to use

### Creating Your Own Videos

- Record with camera/phone
- Use screen recording for tutorials
- Create short clips (5-10 seconds)
- Ensure good lighting and quality

## Video Requirements

### Format
- **Recommended**: MP4 (H.264 codec)
- **Supported**: MP4, MOV, AVI, MKV

### Specifications
- **Resolution**: 224x224 or higher (224x224 recommended for models)
- **Duration**: 5-10 seconds per clip
- **Frame Rate**: 24-30 FPS
- **Aspect Ratio**: 16:9 or 4:3

### File Naming
Use descriptive names:
- `action_scene_001.mp4`
- `comedy_sketch_002.mp4`
- `sports_highlight_003.mp4`

## Dataset Organization

### Recommended Distribution

- **Training Set**: 70% of videos
- **Test Set**: 20% of videos
- **Validation Set**: 10% of videos

### Minimum Videos per Category

- **Minimum for testing**: 10-20 videos per category
- **Recommended for training**: 50-100+ videos per category
- **For production**: 200+ videos per category

## Using the Scripts

### 1. Interactive Mode (Easiest)

```bash
python scripts/add_videos.py --interactive
```

Follow the prompts to:
- Select category
- Select dataset split (train/test/validation)
- Specify source directory

### 2. Batch Mode

```bash
python scripts/add_videos.py \
    --source raw_videos/action \
    --target data/train \
    --category action
```

### 3. Organize Entire Dataset

```bash
python scripts/organize_dataset.py \
    --input raw_videos \
    --output data \
    --train-ratio 0.7 \
    --test-ratio 0.2 \
    --validation-ratio 0.1
```

## Category Descriptions

### Action
- Fight scenes, car chases, stunts, adventure sequences

### Comedy
- Funny moments, comedy sketches, humorous situations

### Drama
- Dramatic scenes, emotional moments, character interactions

### Sports
- Sports highlights, athletic performances, game footage

### Documentary
- Nature, history, science documentaries, educational content

### News
- News broadcasts, reports, interviews, breaking news

### Music
- Music performances, concerts, music videos, instrumental

### Education
- Tutorials, lectures, how-to videos, instructional content

## Verification

After adding videos, verify your dataset:

```python
from utils.dataset_utils import get_dataset_statistics

stats = get_dataset_statistics('data/train')
print(stats)
```

## Tips

1. **Start Small**: Begin with 10-20 videos per category for testing
2. **Quality over Quantity**: Use high-quality videos
3. **Consistent Format**: Keep video formats consistent
4. **Balanced Dataset**: Try to have similar number of videos per category
5. **Label Correctly**: Ensure videos are in correct category folders

## Troubleshooting

### Videos Not Found
- Check file extensions (case-sensitive on some systems)
- Verify video formats are supported
- Check file paths are correct

### Processing Errors
- Ensure OpenCV is installed: `pip install opencv-python`
- Check FFmpeg is installed for format conversion
- Verify video files are not corrupted

### Memory Issues
- Process videos in smaller batches
- Reduce video resolution in config.yaml
- Extract frames instead of processing full videos

## Next Steps

After adding videos:

1. **Verify Dataset**: Check statistics and counts
2. **Extract Frames**: If using frame-based models
3. **Train Model**: Use examples/classification_example.py as starting point
4. **Evaluate**: Test on test set

## Contact

For support or questions:
- Website: https://rskworld.in
- Email: help@rskworld.in, support@rskworld.in
- Phone: +91 93305 39277

**RSK World**
- Founder: Molla Samser
- Designer & Tester: Rima Khatun

