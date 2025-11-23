#!/bin/bash

# Complete training pipeline using JSON annotations
# Usage: ./scripts/train_from_annotations.sh <video_dir> <json_dir>

set -e

if [ $# -lt 2 ]; then
    echo "Usage: ./scripts/train_from_annotations.sh <video_dir> <json_dir>"
    echo ""
    echo "Example:"
    echo "  ./scripts/train_from_annotations.sh data/videos data/annotations"
    exit 1
fi

VIDEO_DIR=$1
JSON_DIR=$2

echo "=========================================="
echo "Pig Behavior Training from Annotations"
echo "=========================================="
echo ""

# Step 1: Parse annotations and extract crops
echo "Step 1: Parsing annotations and extracting pig crops..."
echo ""

# Split videos into train/val (80/20)
# You can adjust this based on your needs
mkdir -p data/pig_crops/{train,val}

# For now, process all videos (you can split them manually or programmatically)
echo "Processing all videos..."
python3 scripts/parse_annotations.py "$VIDEO_DIR" "$JSON_DIR" data/pig_crops/train

echo ""
echo "Step 1 complete!"
echo ""

# Step 2: Split into train/val (80/20 split)
echo "Step 2: Splitting into train/val sets..."
echo ""

# Simple split: move 20% of images from each behavior to val
for behavior in tail_biting ear_biting aggression eating sleeping rooting; do
    if [ -d "data/pig_crops/train/$behavior" ]; then
        mkdir -p "data/pig_crops/val/$behavior"
        
        # Count images
        total=$(find "data/pig_crops/train/$behavior" -name "*.jpg" -o -name "*.png" | wc -l | xargs)
        val_count=$((total / 5))  # 20%
        
        if [ $val_count -gt 0 ]; then
            find "data/pig_crops/train/$behavior" -name "*.jpg" -o -name "*.png" | \
                head -n $val_count | \
                xargs -I {} mv {} "data/pig_crops/val/$behavior/"
            echo "  $behavior: Moved $val_count images to validation set"
        fi
    fi
done

echo ""
echo "Step 2 complete!"
echo ""

# Step 3: Prepare YOLO datasets
echo "Step 3: Preparing YOLO datasets..."
echo ""

python3 scripts/prepare_yolo_from_crops.py data/pig_crops/train data/yolo_dataset/train
python3 scripts/prepare_yolo_from_crops.py data/pig_crops/val data/yolo_dataset/val

echo ""
echo "Step 3 complete!"
echo ""

# Step 4: Create data.yaml
echo "Step 4: Creating data.yaml..."
echo ""

mkdir -p data/yolo_dataset
cat > data/yolo_dataset/data.yaml << EOF
path: $(pwd)/data/yolo_dataset
train: train/images
val: val/images

names:
  0: tail_biting
  1: ear_biting
  2: aggression
  3: eating
  4: sleeping
  5: rooting

nc: 6
EOF

echo "data.yaml created!"
echo ""

# Step 5: Train model
echo "Step 5: Training YOLO model..."
echo "This may take 1-4 hours depending on your GPU and dataset size."
echo ""

python3 scripts/train_pig_behavior.py

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

