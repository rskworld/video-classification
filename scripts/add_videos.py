#!/usr/bin/env python3
"""
Add Videos Script for Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

This script helps add videos to the dataset and organize them by category.
"""

import os
import shutil
import argparse
import yaml
from pathlib import Path
from tqdm import tqdm


def load_config(config_path='config.yaml'):
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        if config is None:
            raise ValueError(f"Configuration file is empty or invalid: {config_path}")
        return config


def get_video_files(directory, formats=None):
    """
    Get all video files from a directory.
    
    Args:
        directory: Directory to search
        formats: List of video formats
    """
    if formats is None:
        formats = ['mp4', 'mov', 'avi', 'mkv']
    
    video_files = []
    for format in formats:
        video_files.extend(Path(directory).rglob(f"*.{format}"))
        video_files.extend(Path(directory).rglob(f"*.{format.upper()}"))
    
    return [str(f) for f in video_files]


def copy_videos_to_category(source_dir, target_dir, category, config):
    """
    Copy videos from source to target category directory.
    
    Args:
        source_dir: Source directory containing videos
        target_dir: Target dataset directory (train/test/validation)
        category: Category name
        config: Configuration dictionary
    """
    # Get video files
    video_files = get_video_files(source_dir, config['video']['formats'])
    
    if not video_files:
        print(f"No video files found in {source_dir}")
        return 0
    
    # Create category directory
    category_dir = os.path.join(target_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    
    # Copy videos
    copied = 0
    for video_file in tqdm(video_files, desc=f"Copying {category} videos"):
        filename = os.path.basename(video_file)
        dest_path = os.path.join(category_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(dest_path):
            continue
        
        try:
            shutil.copy2(video_file, dest_path)
            copied += 1
        except Exception as e:
            print(f"Error copying {video_file}: {e}")
    
    return copied


def interactive_add_videos(config):
    """
    Interactive mode to add videos by category.
    
    Args:
        config: Configuration dictionary
    """
    print("=" * 60)
    print("Video Classification Dataset - Add Videos")
    print("=" * 60)
    
    # Get categories
    categories = config['categories']
    
    print("\nAvailable categories:")
    for i, category in enumerate(categories, 1):
        print(f"  {i}. {category}")
    
    # Select category
    while True:
        try:
            choice = input("\nSelect category number (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                break
            
            category_idx = int(choice) - 1
            if 0 <= category_idx < len(categories):
                category = categories[category_idx]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    if choice.lower() == 'q':
        return
    
    # Select split
    print("\nSelect dataset split:")
    print("  1. train")
    print("  2. test")
    print("  3. validation")
    
    while True:
        try:
            split_choice = input("Select split (1-3): ").strip()
            split_map = {'1': 'train', '2': 'test', '3': 'validation'}
            if split_choice in split_map:
                split = split_map[split_choice]
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
    
    # Get source directory
    source_dir = input("\nEnter path to directory containing videos: ").strip()
    if not os.path.exists(source_dir):
        print(f"Error: Directory not found: {source_dir}")
        return
    
    # Get target directory
    target_dir = os.path.join(config['dataset']['paths'][split], category)
    
    print(f"\nCopying videos from {source_dir} to {target_dir}...")
    copied = copy_videos_to_category(source_dir, config['dataset']['paths'][split], category, config)
    
    print(f"\nSuccessfully copied {copied} videos to {target_dir}")


def batch_add_videos(source_dir, target_dir, category, config):
    """
    Batch mode to add videos.
    
    Args:
        source_dir: Source directory containing videos
        target_dir: Target dataset directory
        category: Category name
        config: Configuration dictionary
    """
    print(f"Adding {category} videos from {source_dir} to {target_dir}...")
    copied = copy_videos_to_category(source_dir, target_dir, category, config)
    print(f"Successfully copied {copied} videos")


def main():
    parser = argparse.ArgumentParser(description='Add videos to dataset')
    parser.add_argument('--source', type=str,
                       help='Source directory containing videos')
    parser.add_argument('--target', type=str,
                       help='Target dataset directory (train/test/validation)')
    parser.add_argument('--category', type=str,
                       help='Category name')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Interactive mode
    if args.interactive:
        interactive_add_videos(config)
        return
    
    # Batch mode
    if not all([args.source, args.target, args.category]):
        print("Error: --source, --target, and --category are required in batch mode")
        print("Or use --interactive for interactive mode")
        return
    
    if not os.path.exists(args.source):
        print(f"Error: Source directory not found: {args.source}")
        return
    
    if args.category not in config['categories']:
        print(f"Error: Invalid category. Available categories: {config['categories']}")
        return
    
    batch_add_videos(args.source, args.target, args.category, config)


if __name__ == '__main__':
    main()

