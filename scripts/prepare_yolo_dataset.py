"""
Prepare pig behavior frames for YOLO classification training.
"""
import os
import shutil
from pathlib import Path

# Pig behavior classes (mapped to numbers)
BEHAVIOR_CLASSES = {
    "tail_biting": 0,
    "ear_biting": 1,
    "aggression": 2,
    "eating": 3,
    "sleeping": 4,
    "rooting": 5
}

def prepare_yolo_dataset(frames_dir, output_dir):
    """
    Prepare frames for YOLO classification format.
    
    YOLO classification format:
    - images/ folder with all images
    - labels/ folder with .txt files (one line: class_id)
    """
    frames_dir = Path(frames_dir)
    output_dir = Path(output_dir)
    
    images_dir = output_dir / "images"
    labels_dir = output_dir / "labels"
    
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each behavior class
    for behavior_name, class_id in BEHAVIOR_CLASSES.items():
        behavior_frames_dir = frames_dir / behavior_name
        
        if not behavior_frames_dir.exists():
            print(f"Warning: {behavior_frames_dir} not found, skipping...")
            continue
        
        print(f"Processing {behavior_name} (class {class_id})...")
        
        frame_files = list(behavior_frames_dir.glob("*.jpg")) + \
                     list(behavior_frames_dir.glob("*.png"))
        
        for frame_file in frame_files:
            # Copy image
            new_image_name = f"{behavior_name}_{frame_file.name}"
            new_image_path = images_dir / new_image_name
            shutil.copy2(frame_file, new_image_path)
            
            # Create label file
            label_name = new_image_name.replace(".jpg", ".txt").replace(".png", ".txt")
            label_path = labels_dir / label_name
            
            with open(label_path, 'w') as f:
                f.write(str(class_id))
        
        print(f"  Processed {len(frame_files)} frames")
    
    print(f"\nDataset prepared at: {output_dir}")
    total_images = len(list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")))
    print(f"Total images: {total_images}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python prepare_yolo_dataset.py <frames_dir> <output_dir>")
        print("\nExample:")
        print("  python prepare_yolo_dataset.py data/pig_frames/train data/yolo_dataset/train")
        sys.exit(1)
    
    frames_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    prepare_yolo_dataset(frames_dir, output_dir)

