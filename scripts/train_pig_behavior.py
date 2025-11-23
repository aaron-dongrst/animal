"""
Train YOLO model for pig behavior classification.
"""
from ultralytics import YOLO
import torch
import os
from pathlib import Path
import time
from datetime import datetime, timedelta
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

# Configuration
DATA_YAML = "data/yolo_dataset/data.yaml"
EPOCHS = 100
BATCH_SIZE = 16
IMAGE_SIZE = 224
MODEL_SIZE = "n"  # n=nano, s=small, m=medium, l=large, x=xlarge

def main():
    print("="*60)
    print("YOLO Pig Behavior Classification Training")
    print("="*60)
    print()
    
    # Check if dataset exists
    data_yaml_path = Path(DATA_YAML)
    if not data_yaml_path.exists():
        print(f"Error: Dataset not found at {DATA_YAML}")
        print("Please prepare your dataset first.")
        print("\nSteps:")
        print("1. Organize videos in data/pig_training/")
        print("2. Extract frames: python scripts/extract_frames.py ...")
        print("3. Prepare dataset: python scripts/prepare_yolo_dataset.py ...")
        return
    
    # Check device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    if device == "cpu":
        print("Warning: Training on CPU will be slow. Consider using GPU if available.")
    print()
    
    # Load pre-trained model
    model_name = f"yolov8{MODEL_SIZE}-cls.pt"
    print(f"Loading pre-trained model: {model_name}")
    try:
        model = YOLO(model_name)
    except Exception as e:
        print(f"Error loading model: {e}")
        print("The model will be downloaded automatically on first use.")
        return
    
    # Train
    print("\nStarting training...")
    print(f"  Epochs: {EPOCHS}")
    print(f"  Batch size: {BATCH_SIZE}")
    print(f"  Image size: {IMAGE_SIZE}")
    print(f"  Data: {DATA_YAML}")
    print(f"  Device: {device}")
    print()
    
    # Calculate estimated time
    # Rough estimate: ~2-5 seconds per epoch on GPU, 10-30 seconds on CPU
    est_seconds_per_epoch = 3 if device == "cuda" else 20
    est_total_seconds = est_seconds_per_epoch * EPOCHS
    est_time = timedelta(seconds=est_total_seconds)
    print(f"Estimated training time: ~{est_time}")
    print(f"  (Actual time may vary based on dataset size and hardware)")
    print()
    
    start_time = time.time()
    
    try:
        results = model.train(
            data=DATA_YAML,
            epochs=EPOCHS,
            imgsz=IMAGE_SIZE,
            batch=BATCH_SIZE,
            device=device,
            project="pig_behavior_classification",
            name="yolov8_pig_behavior",
            patience=10,  # Early stopping: stop if no improvement for 10 epochs
            save=True,
            plots=True,
            verbose=True
        )
        
        elapsed_time = time.time() - start_time
        elapsed_timedelta = timedelta(seconds=int(elapsed_time))
        print(f"\nActual training time: {elapsed_timedelta}")
        
        print("\n" + "="*60)
        print("Training complete!")
        print("="*60)
        print(f"Best model saved at: {results.save_dir}")
        
        # Validate
        print("\nRunning validation...")
        metrics = model.val()
        print(f"\nValidation Results:")
        print(f"  Top-1 Accuracy: {metrics.top1:.2f}%")
        print(f"  Top-5 Accuracy: {metrics.top5:.2f}%")
        
        # Save model path
        best_model_path = os.path.join(results.save_dir, "weights", "best.pt")
        if os.path.exists(best_model_path):
            print(f"\nBest model path: {best_model_path}")
            print("\nTo use this model, set:")
            print(f"  export YOLO_MODEL_PATH=\"{best_model_path}\"")
            print("\nOr use the default path:")
            print(f"  export YOLO_MODEL_PATH=\"pig_behavior_classification/yolov8_pig_behavior/weights/best.pt\"")
        else:
            print(f"\nWarning: Best model not found at {best_model_path}")
            print("Check the weights directory in the results folder.")
            
    except Exception as e:
        print(f"\nError during training: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

