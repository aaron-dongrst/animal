"""
Prepare YOLO dataset from cropped pig images organized by behavior.
"""
import shutil
from pathlib import Path
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    def tqdm(iterable, desc="", total=None, unit=""):
        return iterable

# Behavior classes
BEHAVIOR_CLASSES = {
    "tail_biting": 0,
    "ear_biting": 1,
    "aggression": 2,
    "eating": 3,
    "sleeping": 4,
    "rooting": 5
}

def prepare_yolo_dataset(crops_dir, output_dir):
    """
    Prepare cropped images for YOLO classification format.
    
    Args:
        crops_dir: Directory with behavior subfolders containing cropped images
        output_dir: Output directory for YOLO dataset
    """
    crops_dir = Path(crops_dir)
    output_dir = Path(output_dir)
    
    images_dir = output_dir / "images"
    labels_dir = output_dir / "labels"
    
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    
    total_images = 0
    
    # Process each behavior folder
    for behavior_name, class_id in BEHAVIOR_CLASSES.items():
        behavior_dir = crops_dir / behavior_name
        
        if not behavior_dir.exists():
            print(f"Warning: {behavior_name} folder not found, skipping...")
            continue
        
        # Find all images in this behavior folder
        image_files = list(behavior_dir.glob("*.jpg")) + \
                     list(behavior_dir.glob("*.png")) + \
                     list(behavior_dir.glob("*.jpeg"))
        
        if len(image_files) == 0:
            continue
        
        print(f"Processing {behavior_name} (class {class_id}): {len(image_files)} images")
        
        image_iter = tqdm(image_files, desc=f"  {behavior_name}", leave=False, unit="img")
        for image_file in image_iter:
            # Copy image
            new_image_name = f"{behavior_name}_{image_file.name}"
            new_image_path = images_dir / new_image_name
            shutil.copy2(image_file, new_image_path)
            
            # Create label file
            label_name = new_image_name.replace(".jpg", ".txt").replace(".png", ".txt").replace(".jpeg", ".txt")
            label_path = labels_dir / label_name
            
            with open(label_path, 'w') as f:
                f.write(str(class_id))
            
            total_images += 1
    
    print(f"\nTotal images prepared: {total_images}")
    return total_images

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python prepare_yolo_from_crops.py <crops_dir> <output_dir>")
        print("\nExample:")
        print("  python prepare_yolo_from_crops.py data/pig_crops/train data/yolo_dataset/train")
        sys.exit(1)
    
    crops_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    prepare_yolo_dataset(crops_dir, output_dir)
    print(f"\nYOLO dataset prepared at: {output_dir}")

