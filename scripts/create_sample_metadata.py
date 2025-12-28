#!/usr/bin/env python3
"""
Create Sample Metadata Script
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

This script creates metadata files for the dataset.
"""

import json
import os
import yaml
from pathlib import Path
from utils.dataset_utils import get_dataset_statistics, get_categories, get_videos_by_category


def load_config(config_path='config.yaml'):
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        if config is None:
            raise ValueError(f"Configuration file is empty or invalid: {config_path}")
        return config


def create_metadata_file(output_path='metadata.json', dataset_dir='data'):
    """
    Create metadata JSON file for the entire dataset.
    
    Args:
        output_path: Path to save metadata file
        dataset_dir: Root dataset directory
    """
    config = load_config()
    metadata = {
        'dataset_info': {
            'name': config['dataset']['name'],
            'version': config['dataset']['version'],
            'description': config['dataset']['description'],
            'author': config['metadata']['author'],
            'designer': config['metadata']['designer'],
            'website': config['metadata']['website'],
            'email': config['metadata']['email'],
            'phone': config['metadata']['phone'],
            'organization': config['metadata']['organization']
        },
        'categories': config['categories'],
        'splits': {}
    }
    
    # Process each split
    for split in ['train', 'test', 'validation']:
        split_dir = os.path.join(dataset_dir, split)
        if os.path.exists(split_dir):
            stats = get_dataset_statistics(split_dir)
            videos_by_category = get_videos_by_category(split_dir)
            
            metadata['splits'][split] = {
                'total_categories': stats['total_categories'],
                'total_videos': stats['total_videos'],
                'categories': {}
            }
            
            for category, videos in videos_by_category.items():
                metadata['splits'][split]['categories'][category] = {
                    'count': len(videos),
                    'files': [os.path.basename(v) for v in videos]
                }
    
    # Save metadata
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata saved to: {output_path}")
    return metadata


def print_dataset_summary(metadata):
    """Print a summary of the dataset."""
    print("\n" + "=" * 70)
    print("Dataset Summary")
    print("=" * 70)
    print(f"Name: {metadata['dataset_info']['name']}")
    print(f"Version: {metadata['dataset_info']['version']}")
    print(f"Categories: {', '.join(metadata['categories'])}")
    print("\nVideo Counts by Split:")
    print("-" * 70)
    
    for split, split_data in metadata['splits'].items():
        print(f"\n{split.upper()}:")
        print(f"  Total Videos: {split_data['total_videos']}")
        print(f"  Categories: {split_data['total_categories']}")
        print("  Videos per Category:")
        for category, cat_data in split_data['categories'].items():
            print(f"    {category}: {cat_data['count']} videos")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Create dataset metadata')
    parser.add_argument('--dataset-dir', type=str, default='data',
                       help='Dataset directory')
    parser.add_argument('--output', type=str, default='metadata.json',
                       help='Output metadata file path')
    parser.add_argument('--summary', action='store_true',
                       help='Print dataset summary')
    
    args = parser.parse_args()
    
    # Create metadata
    metadata = create_metadata_file(args.output, args.dataset_dir)
    
    # Print summary if requested
    if args.summary:
        print_dataset_summary(metadata)


if __name__ == '__main__':
    main()

