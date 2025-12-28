# Video Classification Dataset - Project Information

<!--
Project: Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World
-->

## Project Metadata

```php
[
    'id' => 12,
    'title' => 'Video Classification Dataset',
    'category' => 'Video Data',
    'description' => 'Video classification dataset with labeled video clips across multiple categories for video understanding and classification tasks.',
    'full_description' => 'This dataset includes labeled video clips across multiple categories for video classification tasks. Perfect for video understanding, video categorization, and video deep learning applications.',
    'technologies' => ['MP4', 'MOV', 'OpenCV', 'FFmpeg', 'Video'],
    'difficulty' => 'Advanced',
    'source_link' => './video-classification/video-classification.zip',
    'demo_link' => './video-classification/',
    'features' => [
        'Multiple video categories',
        'Labeled video clips',
        'Training and test sets',
        'Frame extraction available',
        'Ready for video models'
    ],
    'icon' => 'fas fa-video',
    'icon_color' => 'text-secondary',
    'project_image' => './video-classification/video-classification.png',
    'project_image_alt' => 'Video Classification Dataset - rskworld.in'
]
```

## Project Structure

```
video-classification/
├── data/                    # Dataset directories
│   ├── train/              # Training videos
│   ├── test/               # Test videos
│   └── validation/         # Validation videos
├── scripts/                # Processing scripts
│   ├── extract_frames.py   # Frame extraction utility
│   ├── process_videos.py   # Video processing utility
│   └── organize_dataset.py # Dataset organization utility
├── utils/                  # Utility modules
│   ├── video_utils.py      # Video processing functions
│   └── dataset_utils.py    # Dataset management functions
├── examples/               # Example code
│   ├── classification_example.py
│   └── video_loader_example.py
├── frames/                 # Extracted frames directory
├── README.md              # Main documentation
├── USAGE.md               # Usage guide
├── CONTRIBUTING.md        # Contribution guidelines
├── LICENSE                # License information
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
├── index.html            # Demo page
└── .gitignore            # Git ignore rules
```

## Key Features

1. **Multiple Video Categories**: Organized dataset with multiple categories
2. **Labeled Video Clips**: All videos properly labeled and categorized
3. **Training and Test Sets**: Pre-organized splits for machine learning
4. **Frame Extraction**: Built-in utilities for extracting frames
5. **Ready for Video Models**: Preprocessed and ready to use

## Technologies

- **MP4/MOV**: Video format support
- **OpenCV**: Video processing and frame extraction
- **FFmpeg**: Video encoding/decoding
- **Python**: Main programming language
- **Machine Learning**: Ready for ML models

## Usage

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Organize dataset
python scripts/organize_dataset.py --input raw_videos --output data

# Extract frames
python scripts/extract_frames.py --input data/train --output frames/train
```

### Example Code

```python
from utils.video_utils import get_video_info, extract_frame
from utils.dataset_utils import get_videos_by_category

# Get video information
info = get_video_info('path/to/video.mp4')

# Extract frame
frame = extract_frame('path/to/video.mp4', frame_number=0)

# Get videos by category
videos = get_videos_by_category('data/train')
```

## Contact Information

**RSK World**
- Website: https://rskworld.in
- Email: help@rskworld.in, support@rskworld.in
- Phone: +91 93305 39277
- Founder: Molla Samser
- Designer & Tester: Rima Khatun

## License

Content used for educational purposes only. View Disclaimer at https://rskworld.in

