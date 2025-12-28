"""
Unique Features for Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

Unique and innovative features for video classification dataset management.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import hashlib
import json
from collections import Counter


def detect_duplicate_videos(video_paths: List[str], threshold: float = 0.95) -> Dict[str, List[str]]:
    """
    Detect duplicate or similar videos using perceptual hashing.
    
    Args:
        video_paths: List of video file paths
        threshold: Similarity threshold (0-1)
        
    Returns:
        Dictionary mapping video paths to list of similar videos
    """
    def compute_video_hash(video_path: str) -> str:
        """Compute hash for video based on key frames."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return ""
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sample_indices = np.linspace(0, total_frames - 1, min(10, total_frames), dtype=int)
        
        frame_hashes = []
        for idx in sample_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                # Resize and convert to grayscale for hashing
                small = cv2.resize(frame, (8, 8))
                gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
                frame_hash = hashlib.md5(gray.tobytes()).hexdigest()
                frame_hashes.append(frame_hash)
        
        cap.release()
        return "".join(frame_hashes)
    
    video_hashes = {}
    for video_path in video_paths:
        video_hash = compute_video_hash(video_path)
        if video_hash:
            video_hashes[video_path] = video_hash
    
    # Find similar videos
    duplicates = {}
    video_list = list(video_hashes.items())
    
    for i, (video1, hash1) in enumerate(video_list):
        similar = []
        for j, (video2, hash2) in enumerate(video_list):
            if i != j:
                # Simple similarity based on hash comparison
                similarity = sum(a == b for a, b in zip(hash1, hash2)) / len(hash1) if hash1 else 0
                if similarity >= threshold:
                    similar.append(video2)
        
        if similar:
            duplicates[video_path] = similar
    
    return duplicates


def auto_categorize_video(video_path: str, category_models: Dict = None) -> Optional[str]:
    """
    Auto-categorize video based on visual features (simplified version).
    
    Args:
        video_path: Path to video file
        category_models: Dictionary of category models (placeholder for ML models)
        
    Returns:
        Predicted category name or None
    """
    # This is a simplified version - in production, use trained ML models
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    
    # Extract sample frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    sample_indices = np.linspace(0, total_frames - 1, min(5, total_frames), dtype=int)
    
    features = []
    for idx in sample_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            # Extract simple features (color histogram, motion, etc.)
            hist = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            features.append(hist.flatten())
    
    cap.release()
    
    # Placeholder for actual ML model prediction
    # In production, use trained classifier here
    return None  # Would return predicted category


def smart_video_splitting(video_path: str, 
                          output_dir: str,
                          segment_duration: float = 10.0,
                          overlap: float = 0.0) -> List[str]:
    """
    Intelligently split long videos into shorter segments.
    
    Args:
        video_path: Input video path
        output_dir: Output directory for segments
        segment_duration: Duration of each segment in seconds
        overlap: Overlap between segments in seconds
        
    Returns:
        List of output video paths
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    frames_per_segment = int(segment_duration * fps)
    frames_overlap = int(overlap * fps)
    
    output_paths = []
    segment_num = 0
    current_frame = 0
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    video_name = Path(video_path).stem
    
    while current_frame < total_frames:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = Path(output_dir) / f"{video_name}_segment_{segment_num:03d}.mp4"
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        frames_written = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        
        while frames_written < frames_per_segment and current_frame < total_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            out.write(frame)
            frames_written += 1
            current_frame += 1
        
        out.release()
        output_paths.append(str(output_path))
        
        # Move to next segment with overlap
        current_frame -= frames_overlap
        segment_num += 1
        
        if frames_written == 0:
            break
    
    cap.release()
    return output_paths


def generate_video_thumbnail(video_path: str, 
                            output_path: str,
                            method: str = 'middle') -> bool:
    """
    Generate thumbnail from video.
    
    Args:
        video_path: Input video path
        output_path: Output thumbnail path
        method: Method to select frame ('middle', 'first', 'best')
        
    Returns:
        True if successful
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return False
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if method == 'middle':
        frame_idx = total_frames // 2
    elif method == 'first':
        frame_idx = 0
    elif method == 'best':
        # Find frame with highest sharpness
        best_frame = None
        best_sharpness = 0
        
        sample_indices = np.linspace(0, total_frames - 1, min(20, total_frames), dtype=int)
        for idx in sample_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
                if sharpness > best_sharpness:
                    best_sharpness = sharpness
                    best_frame = frame
        
        cap.release()
        if best_frame is not None:
            cv2.imwrite(output_path, best_frame)
            return True
        return False
    else:
        frame_idx = 0
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        cv2.imwrite(output_path, frame)
        return True
    
    return False


def create_video_montage(video_paths: List[str], 
                        output_path: str,
                        grid_size: Tuple[int, int] = (2, 2),
                        frame_duration: float = 1.0) -> bool:
    """
    Create a montage video from multiple videos.
    
    Args:
        video_paths: List of input video paths
        output_path: Output montage video path
        grid_size: Grid size (rows, cols)
        frame_duration: Duration to show each frame in seconds
        
    Returns:
        True if successful
    """
    if len(video_paths) > grid_size[0] * grid_size[1]:
        video_paths = video_paths[:grid_size[0] * grid_size[1]]
    
    # Get video properties
    caps = []
    for video_path in video_paths:
        cap = cv2.VideoCapture(video_path)
        if cap.isOpened():
            caps.append(cap)
    
    if not caps:
        return False
    
    # Use first video's properties
    fps = caps[0].get(cv2.CAP_PROP_FPS)
    width = int(caps[0].get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(caps[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Calculate montage dimensions
    montage_width = width * grid_size[1]
    montage_height = height * grid_size[0]
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (montage_width, montage_height))
    
    frames_per_segment = int(fps * frame_duration)
    
    for segment in range(frames_per_segment * 10):  # Create 10 second montage
        montage_frame = np.zeros((montage_height, montage_width, 3), dtype=np.uint8)
        
        for i, cap in enumerate(caps):
            if i >= grid_size[0] * grid_size[1]:
                break
            
            row = i // grid_size[1]
            col = i % grid_size[1]
            
            ret, frame = cap.read()
            if ret:
                y_start = row * height
                y_end = y_start + height
                x_start = col * width
                x_end = x_start + width
                
                montage_frame[y_start:y_end, x_start:x_end] = frame
            else:
                # Reset video if ended
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        out.write(montage_frame)
    
    for cap in caps:
        cap.release()
    out.release()
    
    return True


def analyze_dataset_balance(dataset_dir: str) -> Dict:
    """
    Analyze dataset balance across categories.
    
    Args:
        dataset_dir: Root dataset directory
        
    Returns:
        Dictionary with balance analysis
    """
    from utils.dataset_utils import get_videos_by_category
    
    videos_by_category = get_videos_by_category(dataset_dir)
    
    category_counts = {cat: len(videos) for cat, videos in videos_by_category.items()}
    total_videos = sum(category_counts.values())
    
    if total_videos == 0:
        return {'balanced': False, 'message': 'No videos found'}
    
    # Calculate balance metrics
    avg_count = total_videos / len(category_counts) if category_counts else 0
    max_count = max(category_counts.values()) if category_counts else 0
    min_count = min(category_counts.values()) if category_counts else 0
    
    imbalance_ratio = (max_count - min_count) / avg_count if avg_count > 0 else 0
    
    return {
        'total_videos': total_videos,
        'total_categories': len(category_counts),
        'category_counts': category_counts,
        'average_per_category': avg_count,
        'max_count': max_count,
        'min_count': min_count,
        'imbalance_ratio': imbalance_ratio,
        'balanced': imbalance_ratio < 0.5,  # Consider balanced if ratio < 0.5
        'recommendations': _get_balance_recommendations(category_counts, avg_count)
    }


def _get_balance_recommendations(category_counts: Dict, avg_count: float) -> List[str]:
    """Get recommendations for balancing dataset."""
    recommendations = []
    
    for category, count in category_counts.items():
        if count < avg_count * 0.5:
            recommendations.append(f"Add more videos to '{category}' category (currently {count}, recommended {int(avg_count)})")
        elif count > avg_count * 2:
            recommendations.append(f"Consider reducing videos in '{category}' category (currently {count}, average {int(avg_count)})")
    
    if not recommendations:
        recommendations.append("Dataset is well balanced!")
    
    return recommendations

