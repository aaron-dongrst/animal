"""
Parse JSON annotations and extract labeled pig crops from videos.
"""
import json
import cv2
import os
from pathlib import Path
from typing import List, Dict

def parse_json_annotation(json_path: str) -> List[Dict]:
    """
    Parse JSON annotation file.
    
    Supports multiple JSON formats:
    - List of pig objects
    - Dict with 'pigs' or 'annotations' key
    - Dict with video-level data containing pig list
    
    Returns:
        List of pig objects with tracking_id, frames, bboxes, labels, etc.
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Handle different JSON structures
    if isinstance(data, list):
        # Direct list of pigs
        return data
    elif isinstance(data, dict):
        # Try common keys
        if 'pigs' in data:
            return data['pigs']
        elif 'annotations' in data:
            return data['annotations']
        elif 'objects' in data:
            return data['objects']
        elif 'tracks' in data:
            return data['tracks']
        else:
            # If dict has frame-level data, might need to restructure
            # Check if it's a single pig object
            if 'tracking_id' in data or 'id' in data:
                return [data]
            else:
                # Return empty list if structure is unclear
                print(f"Warning: Unrecognized JSON structure in {json_path}")
                return []
    else:
        return []

def extract_pig_crops(video_path: str, annotations: List[Dict], output_dir: str, 
                     behavior_classes: Dict[str, int], min_visibility: float = 0.5):
    """
    Extract cropped pig images from video based on annotations.
    
    Args:
        video_path: Path to video file
        annotations: List of pig annotation objects
        output_dir: Directory to save cropped images
        behavior_classes: Mapping of behavior labels to class IDs
        min_visibility: Minimum visibility threshold (0-1)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return 0
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    saved_count = 0
    
    # Process each pig annotation
    for pig_annotation in annotations:
        tracking_id = pig_annotation.get('tracking_id', pig_annotation.get('id', 'unknown'))
        frames = pig_annotation.get('frames', [])
        bboxes = pig_annotation.get('bounding_box', pig_annotation.get('bbox', []))
        behavior_label = pig_annotation.get('behavior_label', pig_annotation.get('label', ''))
        visibility = pig_annotation.get('visibility', pig_annotation.get('visibility_flag', 1.0))
        ground_truth = pig_annotation.get('ground_truth', pig_annotation.get('ground_truth_flag', True))
        
        # Skip if not ground truth or visibility too low
        if not ground_truth or visibility < min_visibility:
            continue
        
        # Get class ID for this behavior
        behavior_label_clean = behavior_label.lower().replace(' ', '_')
        class_id = behavior_classes.get(behavior_label_clean, None)
        if class_id is None:
            print(f"Warning: Unknown behavior label '{behavior_label}', skipping...")
            continue
        
        # Process each frame for this pig
        if isinstance(frames, list) and isinstance(bboxes, list):
            # If frames and bboxes are lists, they should be the same length
            for i, frame_num in enumerate(frames):
                # Handle case where bboxes might be shorter or longer
                if i >= len(bboxes):
                    # If no bbox for this frame, skip
                    continue
                
                bbox = bboxes[i]
                if not bbox or len(bbox) < 4:
                    continue
                
                # Set video to specific frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                # Extract bounding box (assuming format: [x, y, width, height] or [x1, y1, x2, y2])
                if len(bbox) == 4:
                    if bbox[2] > bbox[0] and bbox[3] > bbox[1]:
                        # Format: [x1, y1, x2, y2]
                        x1, y1, x2, y2 = map(int, bbox)
                    else:
                        # Format: [x, y, width, height]
                        x, y, w, h = map(int, bbox)
                        x1, y1, x2, y2 = x, y, x + w, y + h
                else:
                    continue
                
                # Ensure coordinates are within frame bounds
                h_frame, w_frame = frame.shape[:2]
                x1 = max(0, min(x1, w_frame))
                y1 = max(0, min(y1, h_frame))
                x2 = max(0, min(x2, w_frame))
                y2 = max(0, min(y2, h_frame))
                
                if x2 <= x1 or y2 <= y1:
                    continue
                
                # Crop the pig
                crop = frame[y1:y2, x1:x2]
                
                if crop.size == 0:
                    continue
                
                # Save cropped image
                image_name = f"{Path(video_path).stem}_pig{tracking_id}_frame{frame_num:06d}.jpg"
                image_path = output_dir / behavior_label_clean / image_name
                image_path.parent.mkdir(parents=True, exist_ok=True)
                
                cv2.imwrite(str(image_path), crop)
                saved_count += 1
    
    cap.release()
    return saved_count

def process_video_with_annotations(video_path: str, json_path: str, output_base_dir: str,
                                   behavior_classes: Dict[str, int]):
    """
    Process a video file with its corresponding JSON annotation.
    
    Args:
        video_path: Path to video file
        json_path: Path to JSON annotation file
        output_base_dir: Base directory for output
        behavior_classes: Mapping of behavior labels to class IDs
    """
    print(f"Processing: {Path(video_path).name}")
    
    # Parse annotations
    annotations = parse_json_annotation(json_path)
    print(f"  Found {len(annotations)} pig annotations")
    
    # Extract crops
    saved = extract_pig_crops(video_path, annotations, output_base_dir, behavior_classes)
    print(f"  Extracted {saved} cropped images")
    
    return saved

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python parse_annotations.py <video_dir> <json_dir> <output_dir>")
        print("\nExample:")
        print("  python parse_annotations.py data/videos data/annotations data/pig_crops")
        sys.exit(1)
    
    video_dir = sys.argv[1]
    json_dir = sys.argv[2]
    output_dir = sys.argv[3]
    
    # Behavior classes
    BEHAVIOR_CLASSES = {
        "tail_biting": 0,
        "ear_biting": 1,
        "aggression": 2,
        "eating": 3,
        "sleeping": 4,
        "rooting": 5
    }
    
    video_dir = Path(video_dir)
    json_dir = Path(json_dir)
    
    total_saved = 0
    
    # Find all video files
    video_files = list(video_dir.glob("*.mp4")) + list(video_dir.glob("*.avi")) + list(video_dir.glob("*.mov"))
    
    for video_path in video_files:
        # Find corresponding JSON file
        json_name = video_path.stem + ".json"
        json_path = json_dir / json_name
        
        if not json_path.exists():
            print(f"Warning: No JSON found for {video_path.name}, skipping...")
            continue
        
        saved = process_video_with_annotations(
            str(video_path),
            str(json_path),
            output_dir,
            BEHAVIOR_CLASSES
        )
        total_saved += saved
    
    print(f"\nTotal cropped images extracted: {total_saved}")

