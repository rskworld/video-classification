"""
Advanced Features for Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

Advanced features including video augmentation, batch processing, and analytics.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
import json
from datetime import datetime


def augment_video_frame(frame: np.ndarray, augmentation_type: str = 'all') -> np.ndarray:
    """
    Apply data augmentation to a video frame.
    
    Args:
        frame: Input frame as numpy array
        augmentation_type: Type of augmentation ('flip', 'rotate', 'brightness', 'contrast', 'all')
        
    Returns:
        Augmented frame
    """
    augmented = frame.copy()
    
    if augmentation_type in ['flip', 'all']:
        # Random horizontal flip
        if np.random.random() > 0.5:
            augmented = cv2.flip(augmented, 1)
    
    if augmentation_type in ['rotate', 'all']:
        # Random rotation
        angle = np.random.uniform(-15, 15)
        h, w = augmented.shape[:2]
        M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
        augmented = cv2.warpAffine(augmented, M, (w, h))
    
    if augmentation_type in ['brightness', 'all']:
        # Random brightness adjustment
        brightness = np.random.uniform(0.7, 1.3)
        augmented = cv2.convertScaleAbs(augmented, alpha=1, beta=(brightness-1)*50)
    
    if augmentation_type in ['contrast', 'all']:
        # Random contrast adjustment
        contrast = np.random.uniform(0.8, 1.2)
        augmented = cv2.convertScaleAbs(augmented, alpha=contrast, beta=0)
    
    return augmented


def extract_key_frames(video_path: str, method: str = 'uniform', num_frames: int = 10) -> List[np.ndarray]:
    """
    Extract key frames from video using different methods.
    
    Args:
        video_path: Path to video file
        method: Extraction method ('uniform', 'scene_change', 'random')
        num_frames: Number of frames to extract
        
    Returns:
        List of key frames
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    
    if method == 'uniform':
        # Extract frames at uniform intervals
        frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
    
    elif method == 'random':
        # Extract random frames
        frame_indices = np.random.choice(total_frames, num_frames, replace=False)
        for idx in sorted(frame_indices):
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
    
    elif method == 'scene_change':
        # Extract frames at scene changes (simplified)
        prev_frame = None
        threshold = 30.0
        
        frame_idx = 0
        while len(frames) < num_frames and frame_idx < total_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            if prev_frame is not None:
                diff = cv2.absdiff(frame, prev_frame)
                mean_diff = np.mean(diff)
                
                if mean_diff > threshold:
                    frames.append(frame)
            
            prev_frame = frame
            frame_idx += 1
    
    cap.release()
    return frames


def batch_process_videos(video_paths: List[str], 
                        process_func, 
                        batch_size: int = 10,
                        progress_callback=None) -> List:
    """
    Process videos in batches for memory efficiency.
    
    Args:
        video_paths: List of video file paths
        process_func: Function to process each video
        batch_size: Number of videos to process at once
        progress_callback: Optional callback function for progress updates
        
    Returns:
        List of processed results
    """
    results = []
    total = len(video_paths)
    
    for i in range(0, total, batch_size):
        batch = video_paths[i:i + batch_size]
        batch_results = []
        
        for video_path in batch:
            try:
                result = process_func(video_path)
                batch_results.append(result)
            except Exception as e:
                print(f"Error processing {video_path}: {e}")
                batch_results.append(None)
        
        results.extend(batch_results)
        
        if progress_callback:
            progress_callback(i + len(batch), total)
    
    return results


def analyze_video_quality(video_path: str) -> dict:
    """
    Analyze video quality metrics.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Dictionary with quality metrics
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {}
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    # Sample frames for quality analysis
    sample_frames = []
    sample_indices = np.linspace(0, total_frames - 1, min(10, total_frames), dtype=int)
    
    for idx in sample_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            sample_frames.append(frame)
    
    cap.release()
    
    if not sample_frames:
        return {}
    
    # Calculate average sharpness
    sharpness_scores = []
    for frame in sample_frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        sharpness_scores.append(laplacian_var)
    
    avg_sharpness = np.mean(sharpness_scores) if sharpness_scores else 0
    
    # Calculate average brightness
    brightness_scores = [np.mean(frame) for frame in sample_frames]
    avg_brightness = np.mean(brightness_scores) if brightness_scores else 0
    
    return {
        'fps': fps,
        'resolution': f"{width}x{height}",
        'width': width,
        'height': height,
        'total_frames': total_frames,
        'duration': duration,
        'sharpness': avg_sharpness,
        'brightness': avg_brightness,
        'quality_score': (avg_sharpness / 100) * (avg_brightness / 255) * 100
    }


def create_video_summary(video_path: str, output_path: str, num_frames: int = 16):
    """
    Create a summary video with key frames.
    
    Args:
        video_path: Input video path
        output_path: Output summary video path
        num_frames: Number of frames to include in summary
    """
    key_frames = extract_key_frames(video_path, method='uniform', num_frames=num_frames)
    
    if not key_frames:
        return False
    
    # Get video properties
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = key_frames[0].shape[1], key_frames[0].shape[0]
    cap.release()
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Write frames
    for frame in key_frames:
        out.write(frame)
    
    out.release()
    return True


def generate_dataset_report(dataset_dir: str, output_path: str = 'dataset_report.json'):
    """
    Generate comprehensive dataset report.
    
    Args:
        dataset_dir: Root dataset directory
        output_path: Path to save report
    """
    from utils.dataset_utils import get_dataset_statistics, get_videos_by_category
    from utils.video_utils import get_video_info
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'dataset_directory': dataset_dir,
        'splits': {}
    }
    
    for split in ['train', 'test', 'validation']:
        split_dir = Path(dataset_dir) / split
        if not split_dir.exists():
            continue
        
        stats = get_dataset_statistics(str(split_dir))
        videos_by_category = get_videos_by_category(str(split_dir))
        
        split_report = {
            'total_videos': stats['total_videos'],
            'total_categories': stats['total_categories'],
            'categories': {}
        }
        
        # Analyze each category
        for category, videos in videos_by_category.items():
            if not videos:
                continue
            
            category_info = {
                'video_count': len(videos),
                'sample_analysis': []
            }
            
            # Analyze sample videos
            sample_size = min(5, len(videos))
            for video_path in videos[:sample_size]:
                info = get_video_info(video_path)
                if info:
                    category_info['sample_analysis'].append({
                        'video': Path(video_path).name,
                        'duration': info['duration'],
                        'resolution': f"{info['width']}x{info['height']}",
                        'fps': info['fps']
                    })
            
            split_report['categories'][category] = category_info
        
        report['splits'][split] = split_report
    
    # Save report
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    return report

