#!/usr/bin/env python3
"""
Frame Extraction Script for Video Classification Dataset
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

This script extracts frames from video files for video classification tasks.
"""

import cv2
import os
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


def extract_frames(video_path, output_dir, fps=1, format='jpg', quality=95):
    """
    Extract frames from a video file.
    
    Args:
        video_path: Path to the video file
        output_dir: Directory to save extracted frames
        fps: Frames per second to extract (1 = 1 frame per second)
        format: Image format (jpg, png)
        quality: JPEG quality (1-100)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return False
    
    # Get video properties
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Avoid division by zero
    if fps <= 0 or video_fps <= 0:
        print(f"Error: Invalid FPS (video_fps={video_fps}, extract_fps={fps})")
        cap.release()
        return False
    
    frame_interval = int(video_fps / fps)  # Extract frame every N frames
    if frame_interval <= 0:
        frame_interval = 1
    
    frame_count = 0
    saved_count = 0
    
    # Get video filename without extension
    video_name = Path(video_path).stem
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Extract frame at specified interval
        if frame_count % frame_interval == 0:
            frame_filename = f"{video_name}_frame_{saved_count:06d}.{format}"
            frame_path = os.path.join(output_dir, frame_filename)
            
            # Save frame
            if format.lower() == 'jpg':
                cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
            else:
                cv2.imwrite(frame_path, frame)
            
            saved_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"Extracted {saved_count} frames from {video_path}")
    return True


def process_directory(input_dir, output_dir, config):
    """
    Process all videos in a directory and extract frames.
    
    Args:
        input_dir: Directory containing video files
        output_dir: Directory to save extracted frames
        config: Configuration dictionary
    """
    video_formats = config['video']['formats']
    frame_config = config['frame_extraction']
    
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
    for video_path in tqdm(video_files, desc="Extracting frames"):
        # Maintain directory structure in output
        relative_path = video_path.relative_to(input_dir)
        category_dir = relative_path.parent
        
        # Create output directory maintaining category structure
        video_output_dir = os.path.join(output_dir, category_dir, video_path.stem)
        os.makedirs(video_output_dir, exist_ok=True)
        
        # Extract frames
        extract_frames(
            str(video_path),
            video_output_dir,
            fps=frame_config['fps'],
            format=frame_config['format'],
            quality=frame_config.get('quality', 95)
        )


def main():
    parser = argparse.ArgumentParser(description='Extract frames from video files')
    parser.add_argument('--input', type=str, required=True,
                       help='Input directory containing video files')
    parser.add_argument('--output', type=str, required=True,
                       help='Output directory for extracted frames')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--fps', type=float, default=None,
                       help='Frames per second to extract (overrides config)')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override fps if provided
    if args.fps is not None:
        config['frame_extraction']['fps'] = args.fps
    
    # Process videos
    process_directory(args.input, args.output, config)
    
    print("Frame extraction completed!")


if __name__ == '__main__':
    main()

