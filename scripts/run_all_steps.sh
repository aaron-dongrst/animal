#!/bin/bash

# Script to run all training steps automatically
# Make sure you've uploaded videos to data/dog_training/ first!

set -e  # Exit on error

echo "=========================================="
echo "Pig Behavior YOLO Training Pipeline"
echo "=========================================="
echo ""

# Check if videos exist
if [ ! -d "data/pig_training/train" ]; then
    echo "Error: data/pig_training/train not found!"
    echo "Please upload videos to data/pig_training/ first."
    exit 1
fi

# Step 1: Extract frames
echo "Step 1: Extracting frames from videos..."
echo ""

BEHAVIORS=("tail_biting" "ear_biting" "aggression" "eating" "sleeping" "rooting")
SPLITS=("train" "val" "test")

for split in "${SPLITS[@]}"; do
    for behavior in "${BEHAVIORS[@]}"; do
        video_dir="data/pig_training/${split}/${behavior}"
        frames_dir="data/pig_frames/${split}/${behavior}"
        
        if [ -d "$video_dir" ] && [ "$(ls -A $video_dir 2>/dev/null)" ]; then
            echo "Extracting frames: ${split}/${behavior}"
            python scripts/extract_frames.py "$video_dir" "$frames_dir" 1.0
        else
            echo "Skipping ${split}/${behavior} (no videos found)"
        fi
    done
done

echo ""
echo "Step 1 complete!"
echo ""

# Step 2: Prepare YOLO dataset
echo "Step 2: Preparing YOLO dataset..."
echo ""

if [ -d "data/pig_frames/train" ]; then
    echo "Preparing training dataset..."
    python scripts/prepare_yolo_dataset.py data/pig_frames/train data/yolo_dataset/train
fi

if [ -d "data/pig_frames/val" ]; then
    echo "Preparing validation dataset..."
    python scripts/prepare_yolo_dataset.py data/pig_frames/val data/yolo_dataset/val
fi

echo ""
echo "Step 2 complete!"
echo ""

# Step 3: Train model
echo "Step 3: Training YOLO model..."
echo "This may take 1-4 hours depending on your GPU and dataset size."
echo ""

python scripts/train_pig_behavior.py

echo ""
echo "=========================================="
echo "Training pipeline complete!"
echo "=========================================="
echo ""
echo "Your trained model is saved at:"
echo "  pig_behavior_classification/yolov8_pig_behavior/weights/best.pt"
echo ""
echo "To use it, set:"
echo "  export YOLO_MODEL_PATH=\"pig_behavior_classification/yolov8_pig_behavior/weights/best.pt\""
echo ""

