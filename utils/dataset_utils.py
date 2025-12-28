"""
Dataset Utility Functions for Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

Utility functions for dataset management and loading.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Tuple
import pandas as pd


def get_categories(dataset_dir: str) -> List[str]:
    """
    Get list of categories from dataset directory.
    
    Args:
        dataset_dir: Root directory of dataset
        
    Returns:
        List of category names
    """
    categories = []
    for item in Path(dataset_dir).iterdir():
        if item.is_dir():
            categories.append(item.name)
    return sorted(categories)


def get_videos_by_category(dataset_dir: str, video_formats: List[str] = None) -> Dict[str, List[str]]:
    """
    Get videos organized by category.
    
    Args:
        dataset_dir: Root directory of dataset
        video_formats: List of video formats (default: ['mp4', 'mov', 'avi', 'mkv'])
        
    Returns:
        Dictionary mapping category names to lists of video paths
    """
    if video_formats is None:
        video_formats = ['mp4', 'mov', 'avi', 'mkv']
    
    videos_by_category = {}
    categories = get_categories(dataset_dir)
    
    for category in categories:
        category_dir = Path(dataset_dir) / category
        videos = []
        
        for format in video_formats:
            videos.extend(category_dir.rglob(f"*.{format}"))
            videos.extend(category_dir.rglob(f"*.{format.upper()}"))
        
        videos_by_category[category] = [str(v) for v in videos]
    
    return videos_by_category


def create_dataset_metadata(dataset_dir: str, output_path: str = 'metadata.json'):
    """
    Create metadata JSON file for dataset.
    
    Args:
        dataset_dir: Root directory of dataset
        output_path: Path to save metadata JSON file
    """
    metadata = {
        'categories': get_categories(dataset_dir),
        'videos': {}
    }
    
    videos_by_category = get_videos_by_category(dataset_dir)
    
    for category, videos in videos_by_category.items():
        metadata['videos'][category] = {
            'count': len(videos),
            'files': videos
        }
    
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return metadata


def load_dataset_metadata(metadata_path: str = 'metadata.json') -> Dict:
    """
    Load dataset metadata from JSON file.
    
    Args:
        metadata_path: Path to metadata JSON file
        
    Returns:
        Metadata dictionary
    """
    with open(metadata_path, 'r') as f:
        return json.load(f)


def create_label_mapping(categories: List[str]) -> Dict[str, int]:
    """
    Create label mapping from category names to integers.
    
    Args:
        categories: List of category names
        
    Returns:
        Dictionary mapping category names to label integers
    """
    return {category: idx for idx, category in enumerate(sorted(categories))}


def get_dataset_statistics(dataset_dir: str) -> Dict:
    """
    Get statistics about the dataset.
    
    Args:
        dataset_dir: Root directory of dataset
        
    Returns:
        Dictionary with dataset statistics
    """
    videos_by_category = get_videos_by_category(dataset_dir)
    
    stats = {
        'total_categories': len(videos_by_category),
        'total_videos': sum(len(videos) for videos in videos_by_category.values()),
        'categories': {}
    }
    
    for category, videos in videos_by_category.items():
        stats['categories'][category] = len(videos)
    
    return stats


def split_videos_by_category(videos_by_category: Dict[str, List[str]], 
                             train_ratio: float = 0.7,
                             test_ratio: float = 0.2,
                             validation_ratio: float = 0.1) -> Tuple[Dict, Dict, Dict]:
    """
    Split videos by category into train/test/validation sets.
    
    Args:
        videos_by_category: Dictionary mapping categories to video lists
        train_ratio: Ratio for training set
        test_ratio: Ratio for test set
        validation_ratio: Ratio for validation set
        
    Returns:
        Tuple of (train, test, validation) dictionaries
    """
    import random
    random.seed(42)
    
    train = {}
    test = {}
    validation = {}
    
    for category, videos in videos_by_category.items():
        random.shuffle(videos)
        
        total = len(videos)
        train_size = int(total * train_ratio)
        test_size = int(total * test_ratio)
        
        train[category] = videos[:train_size]
        test[category] = videos[train_size:train_size + test_size]
        validation[category] = videos[train_size + test_size:]
    
    return train, test, validation


def create_dataframe(dataset_dir: str, split: str = None) -> pd.DataFrame:
    """
    Create pandas DataFrame from dataset.
    
    Args:
        dataset_dir: Root directory of dataset
        split: Dataset split ('train', 'test', 'validation') or None for all
        
    Returns:
        DataFrame with columns: 'video_path', 'category', 'label'
    """
    if split:
        dataset_dir = os.path.join(dataset_dir, split)
    
    videos_by_category = get_videos_by_category(dataset_dir)
    label_mapping = create_label_mapping(list(videos_by_category.keys()))
    
    data = []
    for category, videos in videos_by_category.items():
        for video in videos:
            data.append({
                'video_path': video,
                'category': category,
                'label': label_mapping[category]
            })
    
    return pd.DataFrame(data)

