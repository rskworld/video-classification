"""
Video Utility Functions for Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

Utility functions for video processing and manipulation.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional


def get_video_info(video_path: str) -> Optional[dict]:
    """
    Get video information.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Dictionary with video information or None if error
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Avoid division by zero
    duration = frame_count / fps if fps > 0 else 0.0
    
    info = {
        'fps': fps,
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'frame_count': frame_count,
        'duration': duration,
        'fourcc': int(cap.get(cv2.CAP_PROP_FOURCC))
    }
    cap.release()
    return info


def extract_frame(video_path: str, frame_number: int) -> Optional[np.ndarray]:
    """
    Extract a specific frame from video.
    
    Args:
        video_path: Path to video file
        frame_number: Frame number to extract (0-indexed)
        
    Returns:
        Frame as numpy array or None if error
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    cap.release()
    
    return frame if ret else None


def extract_frames_at_timestamps(video_path: str, timestamps: List[float]) -> List[np.ndarray]:
    """
    Extract frames at specific timestamps.
    
    Args:
        video_path: Path to video file
        timestamps: List of timestamps in seconds
        
    Returns:
        List of frames as numpy arrays
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        cap.release()
        return []
    
    frames = []
    
    for timestamp in timestamps:
        frame_number = int(timestamp * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
    
    cap.release()
    return frames


def resize_frame(frame: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
    """
    Resize a frame.
    
    Args:
        frame: Frame as numpy array
        size: Target size (width, height)
        
    Returns:
        Resized frame
    """
    return cv2.resize(frame, size)


def normalize_frame(frame: np.ndarray) -> np.ndarray:
    """
    Normalize frame to [0, 1] range.
    
    Args:
        frame: Frame as numpy array
        
    Returns:
        Normalized frame
    """
    return frame.astype(np.float32) / 255.0


def preprocess_frame(frame: np.ndarray, size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Preprocess frame for model input.
    
    Args:
        frame: Frame as numpy array
        size: Target size (width, height)
        
    Returns:
        Preprocessed frame
    """
    # Resize
    frame = resize_frame(frame, size)
    
    # Normalize
    frame = normalize_frame(frame)
    
    return frame


def get_video_duration(video_path: str) -> float:
    """
    Get video duration in seconds.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Duration in seconds or 0 if error
    """
    info = get_video_info(video_path)
    return info['duration'] if info else 0.0


def is_valid_video(video_path: str) -> bool:
    """
    Check if video file is valid and can be opened.
    
    Args:
        video_path: Path to video file
        
    Returns:
        True if video is valid, False otherwise
    """
    cap = cv2.VideoCapture(video_path)
    is_valid = cap.isOpened()
    cap.release()
    return is_valid


def get_video_files(directory: str, formats: List[str] = None) -> List[str]:
    """
    Get all video files in a directory.
    
    Args:
        directory: Directory to search
        formats: List of video formats (default: ['mp4', 'mov', 'avi', 'mkv'])
        
    Returns:
        List of video file paths
    """
    if formats is None:
        formats = ['mp4', 'mov', 'avi', 'mkv']
    
    video_files = []
    for format in formats:
        video_files.extend(Path(directory).rglob(f"*.{format}"))
        video_files.extend(Path(directory).rglob(f"*.{format.upper()}"))
    
    return [str(f) for f in video_files]


def create_video_from_frames(frames: List[np.ndarray], output_path: str, fps: float = 30.0):
    """
    Create a video from a list of frames.
    
    Args:
        frames: List of frames as numpy arrays
        output_path: Output video path
        fps: Frames per second
    """
    if not frames:
        return False
    
    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if not out.isOpened():
        return False
    
    for frame in frames:
        out.write(frame)
    
    out.release()
    return True

