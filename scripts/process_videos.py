#!/usr/bin/env python3
"""
Video Processing Script for Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

This script processes video files: resizing, format conversion, and validation.
"""

import cv2
import os
import argparse
import yaml
from pathlib import Path
from tqdm import tqdm
import subprocess


def load_config(config_path='config.yaml'):
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        if config is None:
            raise ValueError(f"Configuration file is empty or invalid: {config_path}")
        return config


def get_video_info(video_path):
    """Get video information."""
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
        'duration': duration
    }
    cap.release()
    return info


def resize_video(input_path, output_path, target_size=(224, 224)):
    """
    Resize video to target dimensions.
    
    Args:
        input_path: Input video path
        output_path: Output video path
        target_size: Target (width, height)
    """
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        return False
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Use default FPS if invalid
    if fps <= 0:
        fps = 30.0
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, target_size)
    
    if not out.isOpened():
        cap.release()
        return False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        resized_frame = cv2.resize(frame, target_size)
        out.write(resized_frame)
    
    cap.release()
    out.release()
    return True


def convert_video_format(input_path, output_path, output_format='mp4'):
    """
    Convert video format using FFmpeg.
    
    Args:
        input_path: Input video path
        output_path: Output video path
        output_format: Output format (mp4, mov, etc.)
    """
    try:
        cmd = [
            'ffmpeg', '-i', str(input_path),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-y',  # Overwrite output file
            str(output_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"FFmpeg not found or error converting {input_path}")
        return False


def validate_video(video_path, config):
    """
    Validate video file meets requirements.
    
    Args:
        video_path: Path to video file
        config: Configuration dictionary
    """
    info = get_video_info(video_path)
    if info is None:
        return False, "Could not open video"
    
    max_duration = config['video']['processing'].get('max_duration', None)
    if max_duration and info['duration'] > max_duration:
        return False, f"Video duration {info['duration']:.2f}s exceeds max {max_duration}s"
    
    return True, "Valid"


def process_video(input_path, output_path, config, resize=True, convert=False):
    """
    Process a single video file.
    
    Args:
        input_path: Input video path
        output_path: Output video path
        config: Configuration dictionary
        resize: Whether to resize video
        convert: Whether to convert format
    """
    # Validate video
    is_valid, message = validate_video(input_path, config)
    if not is_valid:
        print(f"Warning: {input_path} - {message}")
        return False
    
    # Create output directory
    output_dir = os.path.dirname(output_path)
    if output_dir:  # Only create directory if path contains a directory
        os.makedirs(output_dir, exist_ok=True)
    
    # Get target resolution
    target_size = tuple(config['video']['processing']['resolution'])
    
    # Process video
    if resize:
        return resize_video(input_path, output_path, target_size)
    elif convert:
        return convert_video_format(input_path, output_path)
    else:
        # Just copy if no processing needed
        import shutil
        shutil.copy2(input_path, output_path)
        return True


def process_directory(input_dir, output_dir, config):
    """
    Process all videos in a directory.
    
    Args:
        input_dir: Directory containing video files
        output_dir: Directory to save processed videos
        config: Configuration dictionary
    """
    video_formats = config['video']['formats']
    
    # Find all video files
    video_files = []
    for format in video_formats:
        video_files.extend(Path(input_dir).rglob(f"*.{format}"))
        video_files.extend(Path(input_dir).rglob(f"*.{format.upper()}"))
    
    if not video_files:
        print(f"No video files found in {input_dir}")
        return
    
    print(f"Found {len(video_files)} video files")
    
    # Process each video
    for video_path in tqdm(video_files, desc="Processing videos"):
        # Maintain directory structure in output
        relative_path = video_path.relative_to(input_dir)
        output_path = os.path.join(output_dir, relative_path)
        
        # Ensure output format is mp4
        output_path = str(Path(output_path).with_suffix('.mp4'))
        
        # Process video
        process_video(str(video_path), output_path, config, resize=True)


def main():
    parser = argparse.ArgumentParser(description='Process video files')
    parser.add_argument('--input', type=str, required=True,
                       help='Input directory containing video files')
    parser.add_argument('--output', type=str, required=True,
                       help='Output directory for processed videos')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--no-resize', action='store_true',
                       help='Skip resizing videos')
    parser.add_argument('--convert', action='store_true',
                       help='Convert video format')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Process videos
    process_directory(args.input, args.output, config)
    
    print("Video processing completed!")


if __name__ == '__main__':
    main()

