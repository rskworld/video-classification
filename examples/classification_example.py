"""
Video Classification Example
Author: Molla Samser
Designer & Tester: Rima Khatun
Website: https://rskworld.in
Email: help@rskworld.in, support@rskworld.in
Phone: +91 93305 39277
Organization: RSK World

Example script demonstrating video classification using the dataset.
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))

from utils.video_utils import get_video_info, extract_frame, preprocess_frame
from utils.dataset_utils import get_videos_by_category, create_label_mapping


class VideoClassifier:
    """
    Simple video classifier example.
    This is a template - replace with your actual model.
    """
    
    def __init__(self, categories):
        """
        Initialize classifier.
        
        Args:
            categories: List of category names
        """
        self.categories = categories
        self.label_mapping = create_label_mapping(categories)
        self.reverse_mapping = {v: k for k, v in self.label_mapping.items()}
    
    def predict(self, video_path: str) -> str:
        """
        Predict category for a video.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Predicted category name
        """
        # Extract a sample frame (middle frame)
        info = get_video_info(video_path)
        if info is None:
            return "unknown"
        
        middle_frame = info['frame_count'] // 2
        frame = extract_frame(video_path, middle_frame)
        
        if frame is None:
            return "unknown"
        
        # Preprocess frame
        processed_frame = preprocess_frame(frame)
        
        # TODO: Replace with actual model prediction
        # For now, return a random category as example
        import random
        predicted_label = random.randint(0, len(self.categories) - 1)
        
        return self.reverse_mapping[predicted_label]
    
    def predict_batch(self, video_paths: list) -> list:
        """
        Predict categories for multiple videos.
        
        Args:
            video_paths: List of video file paths
            
        Returns:
            List of predicted category names
        """
        predictions = []
        for video_path in video_paths:
            prediction = self.predict(video_path)
            predictions.append(prediction)
        return predictions


def evaluate_classifier(classifier, test_dir: str):
    """
    Evaluate classifier on test set.
    
    Args:
        classifier: VideoClassifier instance
        test_dir: Directory containing test videos organized by category
    """
    videos_by_category = get_videos_by_category(test_dir)
    
    total = 0
    correct = 0
    
    print("Evaluating classifier...")
    print("-" * 50)
    
    for category, videos in videos_by_category.items():
        category_correct = 0
        for video in videos:
            prediction = classifier.predict(video)
            total += 1
            if prediction == category:
                correct += 1
                category_correct += 1
        
        accuracy = (category_correct / len(videos)) * 100 if videos else 0
        print(f"{category}: {category_correct}/{len(videos)} ({accuracy:.2f}%)")
    
    overall_accuracy = (correct / total) * 100 if total > 0 else 0
    print("-" * 50)
    print(f"Overall Accuracy: {correct}/{total} ({overall_accuracy:.2f}%)")


def main():
    # Example usage
    dataset_dir = '../data'
    test_dir = os.path.join(dataset_dir, 'test')
    
    if not os.path.exists(test_dir):
        print(f"Test directory not found: {test_dir}")
        print("Please organize your dataset first using organize_dataset.py")
        return
    
    # Get categories
    from utils.dataset_utils import get_categories
    categories = get_categories(test_dir)
    
    if not categories:
        print("No categories found in test directory")
        return
    
    print(f"Found categories: {categories}")
    
    # Initialize classifier
    classifier = VideoClassifier(categories)
    
    # Evaluate on test set
    evaluate_classifier(classifier, test_dir)
    
    # Example: Predict single video
    videos_by_category = get_videos_by_category(test_dir)
    if videos_by_category:
        first_category = list(videos_by_category.keys())[0]
        if videos_by_category[first_category]:
            test_video = videos_by_category[first_category][0]
            print(f"\nPredicting video: {test_video}")
            prediction = classifier.predict(test_video)
            print(f"Prediction: {prediction}")


if __name__ == '__main__':
    main()

