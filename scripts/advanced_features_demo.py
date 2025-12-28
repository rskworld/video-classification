#!/usr/bin/env python3
"""
Advanced Features Demo Script
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

Demonstrates advanced features of the video classification dataset.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.advanced_features import (
    augment_video_frame,
    extract_key_frames,
    analyze_video_quality,
    create_video_summary,
    generate_dataset_report
)
from utils.unique_features import (
    detect_duplicate_videos,
    smart_video_splitting,
    generate_video_thumbnail,
    analyze_dataset_balance
)
import cv2
import numpy as np


def demo_augmentation():
    """Demonstrate video frame augmentation."""
    print("=" * 60)
    print("Demo: Video Frame Augmentation")
    print("=" * 60)
    
    # Load a sample frame (you would load from actual video)
    print("Note: This demo requires a video file.")
    print("Usage: augment_video_frame(frame, augmentation_type='all')")
    print("Augmentation types: 'flip', 'rotate', 'brightness', 'contrast', 'all'")


def demo_key_frames():
    """Demonstrate key frame extraction."""
    print("\n" + "=" * 60)
    print("Demo: Key Frame Extraction")
    print("=" * 60)
    
    print("Methods available:")
    print("  1. Uniform - Extract frames at uniform intervals")
    print("  2. Random - Extract random frames")
    print("  3. Scene Change - Extract frames at scene changes")
    print("\nUsage:")
    print("  key_frames = extract_key_frames('video.mp4', method='uniform', num_frames=10)")


def demo_quality_analysis():
    """Demonstrate video quality analysis."""
    print("\n" + "=" * 60)
    print("Demo: Video Quality Analysis")
    print("=" * 60)
    
    print("Analyzes:")
    print("  - FPS, Resolution, Duration")
    print("  - Sharpness score")
    print("  - Brightness level")
    print("  - Overall quality score")
    print("\nUsage:")
    print("  quality = analyze_video_quality('video.mp4')")
    print("  print(quality)")


def demo_duplicate_detection():
    """Demonstrate duplicate video detection."""
    print("\n" + "=" * 60)
    print("Demo: Duplicate Video Detection")
    print("=" * 60)
    
    print("Features:")
    print("  - Perceptual hashing for similarity detection")
    print("  - Configurable similarity threshold")
    print("  - Identifies duplicate or very similar videos")
    print("\nUsage:")
    print("  duplicates = detect_duplicate_videos(video_paths, threshold=0.95)")


def demo_smart_splitting():
    """Demonstrate smart video splitting."""
    print("\n" + "=" * 60)
    print("Demo: Smart Video Splitting")
    print("=" * 60)
    
    print("Features:")
    print("  - Split long videos into shorter segments")
    print("  - Configurable segment duration")
    print("  - Optional overlap between segments")
    print("\nUsage:")
    print("  segments = smart_video_splitting('long_video.mp4', 'output_dir/', segment_duration=10.0)")


def demo_thumbnail_generation():
    """Demonstrate thumbnail generation."""
    print("\n" + "=" * 60)
    print("Demo: Thumbnail Generation")
    print("=" * 60)
    
    print("Methods:")
    print("  - 'middle' - Middle frame of video")
    print("  - 'first' - First frame")
    print("  - 'best' - Frame with highest sharpness")
    print("\nUsage:")
    print("  generate_video_thumbnail('video.mp4', 'thumbnail.jpg', method='best')")


def demo_dataset_balance():
    """Demonstrate dataset balance analysis."""
    print("\n" + "=" * 60)
    print("Demo: Dataset Balance Analysis")
    print("=" * 60)
    
    print("Features:")
    print("  - Analyze video distribution across categories")
    print("  - Calculate imbalance ratio")
    print("  - Get recommendations for balancing")
    print("\nUsage:")
    print("  balance = analyze_dataset_balance('data/train')")
    print("  print(balance['recommendations'])")


def main():
    print("\n" + "=" * 60)
    print("Video Classification Dataset - Advanced Features Demo")
    print("=" * 60)
    print("Author: Molla Samser")
    print("Designer & Tester: Rima Khatun")
    print("Website: https://rskworld.in")
    print("=" * 60 + "\n")
    
    demo_augmentation()
    demo_key_frames()
    demo_quality_analysis()
    demo_duplicate_detection()
    demo_smart_splitting()
    demo_thumbnail_generation()
    demo_dataset_balance()
    
    print("\n" + "=" * 60)
    print("For more information, see:")
    print("  - utils/advanced_features.py")
    print("  - utils/unique_features.py")
    print("  - examples/ directory")
    print("=" * 60)


if __name__ == '__main__':
    main()

