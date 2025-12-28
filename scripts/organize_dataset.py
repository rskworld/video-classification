#!/usr/bin/env python3
"""
Dataset Organization Script for Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

This script organizes video files into train/test/validation splits.
"""

import os
import argparse
import yaml
import shutil
from pathlib import Path
import random


def load_config(config_path='config.yaml'):
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        if config is None:
            raise ValueError(f"Configuration file is empty or invalid: {config_path}")
        return config


def get_video_files(directory, video_formats):
    """
    Get all video files organized by category.
    
    Args:
        directory: Root directory containing category folders
        video_formats: List of video format extensions
    """
    videos_by_category = {}
    
    for category_dir in Path(directory).iterdir():
        if not category_dir.is_dir():
            continue
        
        category = category_dir.name
        videos = []
        
        for format in video_formats:
            videos.extend(category_dir.rglob(f"*.{format}"))
            videos.extend(category_dir.rglob(f"*.{format.upper()}"))
        
        if videos:
            videos_by_category[category] = [str(v) for v in videos]
    
    return videos_by_category


def split_dataset(videos_by_category, train_ratio, test_ratio, validation_ratio, random_seed=42):
    """
    Split dataset into train/test/validation sets.
    
    Args:
        videos_by_category: Dictionary of category -> video files
        train_ratio: Ratio for training set
        test_ratio: Ratio for test set
        validation_ratio: Ratio for validation set
        random_seed: Random seed for reproducibility
    """
    random.seed(random_seed)
    
    train_files = {}
    test_files = {}
    validation_files = {}
    
    for category, videos in videos_by_category.items():
        # Shuffle videos
        random.shuffle(videos)
        
        # Calculate split sizes
        total = len(videos)
        train_size = int(total * train_ratio)
        test_size = int(total * test_ratio)
        
        # Split videos
        train = videos[:train_size]
        remaining = videos[train_size:]
        
        test = remaining[:test_size]
        validation = remaining[test_size:]
        
        train_files[category] = train
        test_files[category] = test
        validation_files[category] = validation
        
        print(f"Category '{category}': Train={len(train)}, Test={len(test)}, Validation={len(validation)}")
    
    return train_files, test_files, validation_files


def copy_files(file_dict, output_dir):
    """
    Copy files to output directory maintaining category structure.
    
    Args:
        file_dict: Dictionary of category -> file paths
        output_dir: Output directory
    """
    for category, files in file_dict.items():
        category_dir = os.path.join(output_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        for file_path in files:
            if not os.path.exists(file_path):
                print(f"Warning: Source file not found: {file_path}")
                continue
            
            filename = os.path.basename(file_path)
            dest_path = os.path.join(category_dir, filename)
            try:
                shutil.copy2(file_path, dest_path)
            except Exception as e:
                print(f"Error copying {file_path} to {dest_path}: {e}")


def organize_dataset(input_dir, output_dir, config):
    """
    Organize dataset into train/test/validation splits.
    
    Args:
        input_dir: Input directory containing videos organized by category
        output_dir: Output directory for organized dataset
        config: Configuration dictionary
    """
    video_formats = config['video']['formats']
    splits = config['dataset']['splits']
    
    # Get all video files by category
    print("Scanning for video files...")
    videos_by_category = get_video_files(input_dir, video_formats)
    
    if not videos_by_category:
        print("No video files found!")
        return
    
    print(f"Found {len(videos_by_category)} categories")
    
    # Split dataset
    print("\nSplitting dataset...")
    train_files, test_files, validation_files = split_dataset(
        videos_by_category,
        splits['train_ratio'],
        splits['test_ratio'],
        splits['validation_ratio']
    )
    
    # Create output directories
    train_dir = os.path.join(output_dir, 'train')
    test_dir = os.path.join(output_dir, 'test')
    validation_dir = os.path.join(output_dir, 'validation')
    
    # Copy files to respective directories
    print("\nCopying files to train directory...")
    copy_files(train_files, train_dir)
    
    print("Copying files to test directory...")
    copy_files(test_files, test_dir)
    
    print("Copying files to validation directory...")
    copy_files(validation_files, validation_dir)
    
    print("\nDataset organization completed!")
    print(f"Train: {sum(len(files) for files in train_files.values())} videos")
    print(f"Test: {sum(len(files) for files in test_files.values())} videos")
    print(f"Validation: {sum(len(files) for files in validation_files.values())} videos")


def main():
    parser = argparse.ArgumentParser(description='Organize dataset into train/test/validation splits')
    parser.add_argument('--input', type=str, required=True,
                       help='Input directory containing videos organized by category')
    parser.add_argument('--output', type=str, default='data',
                       help='Output directory for organized dataset')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--train-ratio', type=float, default=None,
                       help='Training set ratio (overrides config)')
    parser.add_argument('--test-ratio', type=float, default=None,
                       help='Test set ratio (overrides config)')
    parser.add_argument('--validation-ratio', type=float, default=None,
                       help='Validation set ratio (overrides config)')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override ratios if provided
    if args.train_ratio is not None:
        config['dataset']['splits']['train_ratio'] = args.train_ratio
    if args.test_ratio is not None:
        config['dataset']['splits']['test_ratio'] = args.test_ratio
    if args.validation_ratio is not None:
        config['dataset']['splits']['validation_ratio'] = args.validation_ratio
    
    # Organize dataset
    organize_dataset(args.input, args.output, config)


if __name__ == '__main__':
    main()

