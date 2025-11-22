"""
Vision Engine for ZooGuardian
Classifies video clips into action labels using VideoMAE model.

Model: MCG-NJU/videomae-base-finetuned-kinetics (Hugging Face)
Input: Path to .mp4 video file
Output: Top predicted action label (e.g., "eating carrots", "walking", "sleeping")
"""

import cv2
import torch
import numpy as np
from transformers import VideoMAEImageProcessor, VideoMAEForVideoClassification
from typing import Tuple, List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VisionEngine:
    """
    Video action classifier using VideoMAE pre-trained on Kinetics-400.
    """
    
    def __init__(self, model_name: str = "MCG-NJU/videomae-base-finetuned-kinetics"):
        """
        Initialize the vision engine with VideoMAE model.
        
        Args:
            model_name: HuggingFace model identifier
        """
        logger.info(f"Loading model: {model_name}")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Load model and processor
        self.processor = VideoMAEImageProcessor.from_pretrained(model_name)
        self.model = VideoMAEForVideoClassification.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()
        
        logger.info("Model loaded successfully")
    
    def extract_frames(self, video_path: str, num_frames: int = 16) -> np.ndarray:
        """
        Extract uniformly sampled frames from video.
        
        Args:
            video_path: Path to video file
            num_frames: Number of frames to extract (default: 16 for VideoMAE)
            
        Returns:
            numpy array of shape (num_frames, height, width, channels)
        """
        logger.info(f"Extracting {num_frames} frames from: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}. Ensure the file is not corrupted or unsupported.")
        
        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        
        logger.info(f"Video stats - Total frames: {total_frames}, FPS: {fps:.2f}, Duration: {duration:.2f}s")
        
        if total_frames < num_frames:
            logger.warning(f"Video has only {total_frames} frames, less than requested {num_frames}")
            num_frames = total_frames
        
        # Calculate frame indices to sample uniformly
        frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        
        frames = []
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            
            if ret:
                try:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(frame_rgb)
                except Exception as e:
                    logger.warning(f"Error converting frame at index {idx} to RGB: {str(e)}")
            else:
                logger.warning(f"Could not read frame at index {idx}. Skipping this frame.")
        
        cap.release()
        
        if len(frames) == 0:
            raise ValueError(f"No frames could be extracted from video: {video_path}. Check if the video is valid.")
        
        logger.info(f"Successfully extracted {len(frames)} frames")
        return np.array(frames)
    
    def classify_video(self, video_path: str, top_k: int = 5) -> List[Dict[str, float]]:
        """
        Classify a video and return top-k predictions.
        
        Args:
            video_path: Path to video file
            top_k: Number of top predictions to return
            
        Returns:
            List of dictionaries with 'label' and 'confidence' keys
        """
        logger.info(f"Classifying video: {video_path}")
        
        # Extract frames
        frames = self.extract_frames(video_path)
        
        # Preprocess frames
        inputs = self.processor(list(frames), return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
        
        # Get probabilities
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        
        # Get top-k predictions
        top_probs, top_indices = torch.topk(probabilities[0], top_k)
        
        predictions = []
        for prob, idx in zip(top_probs, top_indices):
            label = self.model.config.id2label[idx.item()]
            confidence = prob.item()
            predictions.append({
                "label": label,
                "confidence": confidence
            })
            logger.info(f"  {label}: {confidence:.4f}")
        
        return predictions
    
    def get_top_prediction(self, video_path: str) -> Tuple[str, float]:
        """
        Get the top prediction for a video.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Tuple of (label, confidence)
        """
        predictions = self.classify_video(video_path, top_k=1)
        top_pred = predictions[0]
        return top_pred["label"], top_pred["confidence"]


def main():
    """
    Example usage of VisionEngine.
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python vision_engine.py <path_to_video>")
        print("\nExample:")
        print("  python vision_engine.py data/raw_videos/Healthy/rabbit_eating.mp4")
        sys.exit(1)
    
    video_path = sys.argv[1]
    
    # Initialize engine
    engine = VisionEngine()
    
    # Classify video
    print(f"\n{'='*60}")
    print(f"Video Classification Results")
    print(f"{'='*60}\n")
    
    predictions = engine.classify_video(video_path, top_k=5)
    
    print(f"\nTop Prediction: {predictions[0]['label']}")
    print(f"Confidence: {predictions[0]['confidence']:.2%}\n")
    
    print("All Top-5 Predictions:")
    for i, pred in enumerate(predictions, 1):
        print(f"  {i}. {pred['label']:<40} {pred['confidence']:.2%}")


if __name__ == "__main__":
    main()
