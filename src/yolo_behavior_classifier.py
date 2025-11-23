"""
YOLO Behavior Classifier for FaunaVision
Processes videos frame-by-frame to classify animal behaviors
and returns time percentages for each behavior class.
"""

import cv2
import numpy as np
from typing import Dict, List
from collections import Counter
import logging
import os

logger = logging.getLogger(__name__)

# YOLO integration
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logger.warning("Ultralytics YOLO not available. Install with: pip install ultralytics")


class YOLOBehaviorClassifier:
    """
    Classifies animal behaviors in videos using YOLO model.
    Returns time percentages for each behavior class.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize YOLO behavior classifier.
        
        Args:
            model_path: Path to trained YOLO model (.pt file)
                       If None, will use placeholder
        """
        self.model = None
        self.model_path = model_path
        
        # Behavior classes for pigs
        self.behavior_classes = {
            0: "tail_biting",
            1: "ear_biting",
            2: "aggression",
            3: "eating",
            4: "sleeping",
            5: "rooting"
        }
        
        # Define which behaviors indicate distress (for pigs)
        self.distress_behaviors = ["tail_biting", "ear_biting", "aggression"]
        
        if YOLO_AVAILABLE and model_path and os.path.exists(model_path):
            try:
                self.model = YOLO(model_path)
                logger.info(f"YOLO model loaded from: {model_path}")
            except Exception as e:
                logger.error(f"Failed to load YOLO model: {e}")
                self.model = None
        elif YOLO_AVAILABLE and model_path:
            logger.warning(f"YOLO model path not found: {model_path}")
        else:
            logger.warning("YOLO not available or model path not provided. Using placeholder.")
    
    def analyze_video_percentages(
        self, 
        video_path: str, 
        frame_interval: float = 1.0,
        confidence_threshold: float = 0.5
    ) -> Dict[str, float]:
        """
        Analyze video and return time percentages for each behavior.
        
        Args:
            video_path: Path to video file
            frame_interval: Process every N seconds (default: 1.0)
            confidence_threshold: Minimum confidence to accept prediction
            
        Returns:
            Dictionary with behavior percentages:
            {
                "scratching": 0.25,  # 25% of time
                "pacing": 0.60,      # 60% of time
                "sleeping": 0.15     # 15% of time
            }
            Percentages always sum to 1.0
        """
        if self.model is None:
            # Placeholder: return equal distribution
            logger.warning("YOLO model not available, using placeholder percentages")
            num_classes = len(self.behavior_classes)
            return {behavior: 1.0 / num_classes for behavior in self.behavior_classes.values()}
        
        try:
            # Open video
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video: {video_path}")
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            logger.info(f"Processing video: {total_frames} frames, {fps:.2f} FPS, {duration:.2f}s")
            
            # Calculate frame interval
            frame_skip = int(fps * frame_interval) if fps > 0 else 1
            if frame_skip < 1:
                frame_skip = 1
            
            # Process frames
            predictions = []
            frame_count = 0
            processed_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every N frames
                if frame_count % frame_skip == 0:
                    try:
                        # Run YOLO inference
                        results = self.model(frame, verbose=False)
                        
                        # Get classification result
                        if hasattr(results[0], 'probs'):
                            # Classification model
                            probs = results[0].probs
                            top_class = probs.top1
                            confidence = probs.top1conf.item()
                            
                            if confidence >= confidence_threshold:
                                behavior = self.behavior_classes.get(top_class, "unknown")
                                predictions.append(behavior)
                                processed_count += 1
                        else:
                            # Detection model - would need different handling
                            logger.warning("Detection model detected, but classification expected")
                            predictions.append("unknown")
                            processed_count += 1
                            
                    except Exception as e:
                        logger.warning(f"Error processing frame {frame_count}: {e}")
                        predictions.append("unknown")
                        processed_count += 1
                
                frame_count += 1
            
            cap.release()
            
            # Calculate percentages
            if len(predictions) == 0:
                logger.warning("No predictions made, returning equal distribution")
                num_classes = len(self.behavior_classes)
                return {behavior: 1.0 / num_classes for behavior in self.behavior_classes.values()}
            
            # Count behaviors
            behavior_counts = Counter(predictions)
            total_predictions = len(predictions)
            
            # Calculate percentages
            percentages = {}
            for behavior in self.behavior_classes.values():
                count = behavior_counts.get(behavior, 0)
                percentages[behavior] = count / total_predictions
            
            # Normalize to ensure sum = 1.0
            total = sum(percentages.values())
            if total > 0:
                percentages = {k: v / total for k, v in percentages.items()}
            else:
                # Fallback: equal distribution
                num_classes = len(self.behavior_classes)
                percentages = {behavior: 1.0 / num_classes for behavior in self.behavior_classes.values()}
            
            logger.info(f"Behavior percentages: {percentages}")
            logger.info(f"Processed {processed_count} frames from {total_frames} total frames")
            
            return percentages
            
        except Exception as e:
            logger.error(f"Error analyzing video: {e}", exc_info=True)
            # Return equal distribution on error
            num_classes = len(self.behavior_classes)
            return {behavior: 1.0 / num_classes for behavior in self.behavior_classes.values()}
    
    def get_primary_behavior(self, percentages: Dict[str, float]) -> tuple:
        """
        Get the primary (most common) behavior from percentages.
        
        Args:
            percentages: Dictionary of behavior percentages
            
        Returns:
            Tuple of (behavior_name, percentage)
        """
        if not percentages:
            return ("unknown", 0.0)
        
        primary = max(percentages.items(), key=lambda x: x[1])
        return primary
    
    def calculate_distress_level(self, percentages: Dict[str, float]) -> Dict:
        """
        Calculate distress level based on behavior percentages.
        
        Args:
            percentages: Behavior time percentages
            
        Returns:
            Dictionary with distress assessment:
            {
                "distress_level": "none" | "low" | "moderate" | "high",
                "distress_percentage": float,
                "normal_percentage": float,
                "is_distressed": bool
            }
        """
        distress_behaviors = self.distress_behaviors
        normal_behaviors = [
            behavior for behavior in self.behavior_classes.values()
            if behavior not in distress_behaviors
        ]
        
        distress_percentage = sum(
            percentages.get(behavior, 0.0) 
            for behavior in distress_behaviors
        )
        
        normal_percentage = sum(
            percentages.get(behavior, 0.0) 
            for behavior in normal_behaviors
        )
        
        # Determine distress level
        if distress_percentage > 0.5:  # More than 50% distress behaviors
            distress_level = "high"
        elif distress_percentage > 0.3:  # More than 30% distress behaviors
            distress_level = "moderate"
        elif distress_percentage > 0.1:  # More than 10% distress behaviors
            distress_level = "low"
        else:
            distress_level = "none"
        
        return {
            "distress_level": distress_level,
            "distress_percentage": distress_percentage,
            "normal_percentage": normal_percentage,
            "is_distressed": distress_percentage > 0.3  # Threshold for distress
        }


def main():
    """
    Example usage of YOLOBehaviorClassifier.
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python yolo_behavior_classifier.py <video_path> [model_path]")
        print("\nExample:")
        print("  python yolo_behavior_classifier.py data/raw_videos/Not Healthy/polarBearPacing.mp4 models/behavior_classifier.pt")
        sys.exit(1)
    
    video_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Initialize classifier
    classifier = YOLOBehaviorClassifier(model_path=model_path)
    
    # Analyze video
    print(f"\n{'='*60}")
    print(f"YOLO Behavior Classification")
    print(f"{'='*60}\n")
    print(f"Video: {video_path}")
    print(f"Model: {model_path or 'Placeholder'}\n")
    
    percentages = classifier.analyze_video_percentages(video_path)
    
    print("Behavior Time Percentages:")
    for behavior, percentage in percentages.items():
        print(f"  {behavior.capitalize()}: {percentage:.1%}")
    
    primary_behavior, primary_percentage = classifier.get_primary_behavior(percentages)
    print(f"\nPrimary Behavior: {primary_behavior.capitalize()} ({primary_percentage:.1%})")
    
    # Verify sum = 1.0
    total = sum(percentages.values())
    print(f"\nTotal: {total:.2f} {'✓' if abs(total - 1.0) < 0.01 else '✗ (ERROR)'}")


if __name__ == "__main__":
    main()

