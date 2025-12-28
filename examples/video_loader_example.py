"""
Video Loader Example
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

Example script demonstrating how to load and process videos from the dataset.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))

from utils.video_utils import (
    get_video_info,
    extract_frame,
    extract_frames_at_timestamps,
    preprocess_frame,
    get_video_files
)
from utils.dataset_utils import (
    get_categories,
    get_videos_by_category,
    create_label_mapping,
    get_dataset_statistics
)


def example_load_single_video():
    """Example: Load and process a single video."""
    print("=" * 60)
    print("Example 1: Loading a Single Video")
    print("=" * 60)
    
    # Find a video file
    dataset_dir = '../data/train'
    video_files = get_video_files(dataset_dir)
    
    if not video_files:
        print("No video files found. Please add videos to the dataset first.")
        return
    
    video_path = video_files[0]
    print(f"Loading video: {video_path}")
    
    # Get video information
    info = get_video_info(video_path)
    if info:
        print(f"FPS: {info['fps']:.2f}")
        print(f"Resolution: {info['width']}x{info['height']}")
        print(f"Frame count: {info['frame_count']}")
        print(f"Duration: {info['duration']:.2f} seconds")
    
    # Extract a frame
    frame = extract_frame(video_path, 0)
    if frame is not None:
        print(f"Extracted frame shape: {frame.shape}")
    
    # Preprocess frame
    processed_frame = preprocess_frame(frame)
    print(f"Processed frame shape: {processed_frame.shape}")
    print(f"Processed frame range: [{processed_frame.min():.2f}, {processed_frame.max():.2f}]")


def example_load_by_category():
    """Example: Load videos organized by category."""
    print("\n" + "=" * 60)
    print("Example 2: Loading Videos by Category")
    print("=" * 60)
    
    dataset_dir = '../data/train'
    videos_by_category = get_videos_by_category(dataset_dir)
    
    if not videos_by_category:
        print("No videos found. Please add videos to the dataset first.")
        return
    
    print(f"Found {len(videos_by_category)} categories:")
    for category, videos in videos_by_category.items():
        print(f"  {category}: {len(videos)} videos")
    
    # Create label mapping
    categories = list(videos_by_category.keys())
    label_mapping = create_label_mapping(categories)
    print("\nLabel mapping:")
    for category, label in label_mapping.items():
        print(f"  {category}: {label}")


def example_extract_multiple_frames():
    """Example: Extract frames at specific timestamps."""
    print("\n" + "=" * 60)
    print("Example 3: Extracting Frames at Timestamps")
    print("=" * 60)
    
    dataset_dir = '../data/train'
    video_files = get_video_files(dataset_dir)
    
    if not video_files:
        print("No video files found. Please add videos to the dataset first.")
        return
    
    video_path = video_files[0]
    print(f"Processing video: {video_path}")
    
    # Get video duration
    info = get_video_info(video_path)
    if info:
        duration = info['duration']
        print(f"Video duration: {duration:.2f} seconds")
        
        # Extract frames at 1s, 2s, 3s intervals
        timestamps = [1.0, 2.0, 3.0]
        frames = extract_frames_at_timestamps(video_path, timestamps)
        print(f"Extracted {len(frames)} frames at timestamps: {timestamps}")


def example_dataset_statistics():
    """Example: Get dataset statistics."""
    print("\n" + "=" * 60)
    print("Example 4: Dataset Statistics")
    print("=" * 60)
    
    dataset_dir = '../data'
    
    # Get statistics for each split
    for split in ['train', 'test', 'validation']:
        split_dir = os.path.join(dataset_dir, split)
        if os.path.exists(split_dir):
            stats = get_dataset_statistics(split_dir)
            print(f"\n{split.upper()} Set:")
            print(f"  Total categories: {stats['total_categories']}")
            print(f"  Total videos: {stats['total_videos']}")
            print("  Videos per category:")
            for category, count in stats['categories'].items():
                print(f"    {category}: {count}")


def example_iterate_dataset():
    """Example: Iterate through dataset for training."""
    print("\n" + "=" * 60)
    print("Example 5: Iterating Through Dataset")
    print("=" * 60)
    
    dataset_dir = '../data/train'
    videos_by_category = get_videos_by_category(dataset_dir)
    label_mapping = create_label_mapping(list(videos_by_category.keys()))
    
    if not videos_by_category:
        print("No videos found. Please add videos to the dataset first.")
        return
    
    print("Iterating through dataset:")
    print("-" * 60)
    
    sample_count = 0
    max_samples = 5  # Show only first 5 examples
    
    for category, videos in videos_by_category.items():
        label = label_mapping[category]
        print(f"\nCategory: {category} (label: {label})")
        
        for video in videos[:max_samples]:
            info = get_video_info(video)
            if info:
                print(f"  Video: {os.path.basename(video)}")
                print(f"    Duration: {info['duration']:.2f}s, "
                      f"Resolution: {info['width']}x{info['height']}")
                sample_count += 1
        
        if len(videos) > max_samples:
            print(f"  ... and {len(videos) - max_samples} more videos")
    
    print(f"\nTotal samples shown: {sample_count}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Video Classification Dataset - Loader Examples")
    print("=" * 60)
    print("Author: Molla Samser")
    print("Designer & Tester: Rima Khatun")
    print("Website: https://rskworld.in")
    print("=" * 60 + "\n")
    
    # Run examples
    example_load_single_video()
    example_load_by_category()
    example_extract_multiple_frames()
    example_dataset_statistics()
    example_iterate_dataset()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()

