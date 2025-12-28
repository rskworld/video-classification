#!/usr/bin/env python3
"""
Sample Data Download Helper Script
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

This script provides instructions and helper functions for downloading sample video data.
"""

import os
import yaml
from pathlib import Path


def load_config(config_path='config.yaml'):
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        if config is None:
            raise ValueError(f"Configuration file is empty or invalid: {config_path}")
        return config


def print_download_instructions():
    """Print instructions for downloading sample video data."""
    print("=" * 70)
    print("Video Classification Dataset - Sample Data Download Guide")
    print("=" * 70)
    print("\nTo add real video data to this dataset, you can:")
    print("\n1. DOWNLOAD FROM FREE SOURCES:")
    print("   - Pexels Videos: https://www.pexels.com/videos/")
    print("   - Pixabay Videos: https://pixabay.com/videos/")
    print("   - Videvo: https://www.videvo.net/")
    print("   - YouTube (with proper permissions)")
    print("\n2. USE YOUR OWN VIDEOS:")
    print("   - Record videos with your camera/phone")
    print("   - Use existing video collections")
    print("   - Create your own video clips")
    print("\n3. ORGANIZE VIDEOS:")
    print("   - Create a 'raw_videos' directory")
    print("   - Organize by category:")
    print("     raw_videos/")
    print("     ├── action/")
    print("     ├── comedy/")
    print("     ├── drama/")
    print("     ├── sports/")
    print("     ├── documentary/")
    print("     ├── news/")
    print("     ├── music/")
    print("     └── education/")
    print("\n4. ADD VIDEOS TO DATASET:")
    print("   Option A - Use organize_dataset.py:")
    print("     python scripts/organize_dataset.py --input raw_videos --output data")
    print("\n   Option B - Use add_videos.py (interactive):")
    print("     python scripts/add_videos.py --interactive")
    print("\n   Option B - Use add_videos.py (batch):")
    print("     python scripts/add_videos.py --source raw_videos/action --target data/train --category action")
    print("\n5. RECOMMENDED VIDEO SPECIFICATIONS:")
    print("   - Format: MP4 (recommended), MOV, AVI, or MKV")
    print("   - Resolution: 224x224 or higher")
    print("   - Duration: 5-10 seconds per clip")
    print("   - Frame rate: 24-30 FPS")
    print("   - Minimum videos per category: 10-20 for testing")
    print("\n6. PROCESS VIDEOS:")
    print("   - Resize videos:")
    print("     python scripts/process_videos.py --input raw_videos --output data/train")
    print("   - Extract frames:")
    print("     python scripts/extract_frames.py --input data/train --output frames/train")
    print("\n" + "=" * 70)
    print("For more information, visit: https://rskworld.in")
    print("=" * 70)


def create_sample_structure():
    """Create sample directory structure for raw videos."""
    config = load_config()
    categories = config['categories']
    
    raw_videos_dir = Path('raw_videos')
    raw_videos_dir.mkdir(exist_ok=True)
    
    print("\nCreating sample directory structure...")
    for category in categories:
        category_dir = raw_videos_dir / category
        category_dir.mkdir(exist_ok=True)
        
        # Create README in each category
        readme_content = f"""# {category.capitalize()} Category

<!--
Project: Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World
-->

## Instructions

Place your {category} video files in this directory.

Supported formats: MP4, MOV, AVI, MKV

After adding videos, run:
```bash
python scripts/organize_dataset.py --input raw_videos --output data
```
"""
        
        readme_path = category_dir / 'README.md'
        readme_path.write_text(readme_content)
        print(f"  Created: {category_dir}/")
    
    print(f"\nSample structure created in: {raw_videos_dir}")
    print("Now add your video files to the appropriate category folders!")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Sample data download helper')
    parser.add_argument('--create-structure', action='store_true',
                       help='Create sample directory structure')
    parser.add_argument('--instructions', action='store_true',
                       help='Show download instructions')
    
    args = parser.parse_args()
    
    if args.create_structure:
        create_sample_structure()
    elif args.instructions:
        print_download_instructions()
    else:
        print_download_instructions()
        print("\n" + "-" * 70)
        response = input("\nWould you like to create the sample directory structure? (y/n): ")
        if response.lower() == 'y':
            create_sample_structure()


if __name__ == '__main__':
    main()

