"""
Parse JSON annotations and extract labeled pig crops from videos.
"""
import json
import cv2
import os
from pathlib import Path
from typing import List, Dict
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    # Fallback: create a dummy tqdm
    def tqdm(iterable, desc="", total=None, unit=""):
        return iterable

def parse_json_annotation(json_path: str) -> List[Dict]:
    """
    Parse JSON annotation file.
    
    Supports multiple JSON formats:
    - List of pig objects
    - Dict with 'objects' key (your format)
    - Dict with 'pigs' or 'annotations' key
    
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
        if 'objects' in data:
            # Your format: dict with "objects" key
            objects = data['objects']
            # Convert to our expected format
            converted = []
            for obj in objects:
                pig_id = obj.get('id', obj.get('tracking_id', 'unknown'))
                frames_list = obj.get('frames', [])
                
                # Convert frame objects to our format
                frames = []
                bboxes = []
                behaviors = []
                visibilities = []
                ground_truths = []
                
                for frame_obj in frames_list:
                    if isinstance(frame_obj, dict):
                        frames.append(frame_obj.get('frameNumber', frame_obj.get('frame', 0)))
                        
                        # Handle bbox format: {"x": 100, "y": 150, "width": 200, "height": 100}
                        bbox_dict = frame_obj.get('bbox', {})
                        if isinstance(bbox_dict, dict):
                            x = bbox_dict.get('x', 0)
                            y = bbox_dict.get('y', 0)
                            w = bbox_dict.get('width', 0)
                            h = bbox_dict.get('height', 0)
                            # Convert to [x1, y1, x2, y2] format
                            bboxes.append([x, y, x + w, y + h])
                        elif isinstance(bbox_dict, list):
                            bboxes.append(bbox_dict)
                        else:
                            bboxes.append([])
                        
                        # Get behavior (note: "behaviour" in your JSON)
                        behavior = frame_obj.get('behaviour', frame_obj.get('behavior', ''))
                        behaviors.append(behavior)
                        
                        # Get visibility (boolean in your JSON)
                        visible = frame_obj.get('visible', True)
                        visibilities.append(1.0 if visible else 0.0)
                        
                        # Get ground truth
                        gt = frame_obj.get('isGroundTruth', frame_obj.get('ground_truth', True))
                        ground_truths.append(gt)
                
                # Create pig object in our expected format
                converted.append({
                    'tracking_id': pig_id,
                    'frames': frames,
                    'bounding_box': bboxes,
                    'behavior_label': behaviors,  # List of behaviors per frame
                    'visibility': visibilities,
                    'ground_truth': ground_truths
                })
            
            return converted
        elif 'pigs' in data:
            return data['pigs']
        elif 'annotations' in data:
            return data['annotations']
        elif 'tracks' in data:
            return data['tracks']
        else:
            # If dict has frame-level data, might need to restructure
            if 'tracking_id' in data or 'id' in data:
                return [data]
            else:
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
        behavior_labels = pig_annotation.get('behavior_label', pig_annotation.get('label', []))
        visibilities = pig_annotation.get('visibility', pig_annotation.get('visibility_flag', []))
        ground_truths = pig_annotation.get('ground_truth', pig_annotation.get('ground_truth_flag', []))
        
        # Handle case where behavior_label is a single string (old format)
        if isinstance(behavior_labels, str):
            behavior_labels = [behavior_labels] * len(frames)
        if isinstance(visibilities, (int, float)):
            visibilities = [visibilities] * len(frames)
        if isinstance(ground_truths, bool):
            ground_truths = [ground_truths] * len(frames)
        
        # Process each frame for this pig
        if isinstance(frames, list) and isinstance(bboxes, list):
            # If frames and bboxes are lists, they should be the same length
            frame_iter = tqdm(enumerate(frames), total=len(frames), 
                            desc=f"  Pig {tracking_id}", leave=False, unit="frame")
            for i, frame_num in frame_iter:
                # Handle case where bboxes might be shorter or longer
                if i >= len(bboxes) or i >= len(behavior_labels):
                    continue
                
                bbox = bboxes[i]
                behavior_label = behavior_labels[i] if i < len(behavior_labels) else ''
                visibility = visibilities[i] if i < len(visibilities) else 1.0
                ground_truth = ground_truths[i] if i < len(ground_truths) else True
                
                # Skip if not ground truth or visibility too low
                if not ground_truth or visibility < min_visibility:
                    continue
                
                # Map behavior labels to our classes
                behavior_mapping = {
                    # Direct matches
                    'tail_biting': 'tail_biting',
                    'ear_biting': 'ear_biting',
                    'aggression': 'aggression',
                    'eating': 'eating',
                    'sleeping': 'sleeping',
                    'rooting': 'rooting',
                    # Your JSON format mappings
                    'sleep': 'sleeping',
                    'lying': 'sleeping',  # Map lying to sleeping (normal rest)
                    'eat': 'eating',
                    'drink': 'eating',  # Map drink to eating (normal behavior)
                    'walk': 'rooting',  # Map walk to rooting (normal exploratory behavior)
                    'run': 'rooting',  # Map run to rooting (normal movement)
                    'standing': 'rooting',  # Map standing to rooting (normal behavior)
                    'sitting': 'rooting',  # Map sitting to rooting (normal behavior)
                    'investigating': 'rooting',  # Map investigating to rooting (normal exploratory)
                    'playwithtoy': 'rooting',  # Map play to rooting (normal behavior)
                    'jumpontopof': 'rooting',  # Map play behavior to rooting
                    'fight': 'aggression',  # Map fight to aggression (distress behavior)
                    'chase': 'aggression',  # Map chase to aggression (distress behavior)
                    'nose-poke-elsewhere': 'tail_biting',  # Map nose-poke-elsewhere to tail_biting (distress)
                    'nose-to-nose': 'ear_biting',  # Map nose-to-nose to ear_biting (distress)
                    'other': 'rooting',  # Map other to rooting (default)
                    # Alternative spellings
                    'tail biting': 'tail_biting',
                    'ear biting': 'ear_biting',
                }
                
                behavior_label_clean = behavior_label.lower().strip()
                mapped_behavior = behavior_mapping.get(behavior_label_clean, behavior_label_clean)
                
                # Get class ID for this behavior
                class_id = behavior_classes.get(mapped_behavior, None)
                if class_id is None:
                    # Try direct match
                    class_id = behavior_classes.get(behavior_label_clean, None)
                    if class_id is None:
                        print(f"Warning: Unknown behavior label '{behavior_label}' (mapped: '{mapped_behavior}'), skipping...")
                        continue
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
                image_path = output_dir / mapped_behavior / image_name
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
    
    print(f"\nFound {len(video_files)} video files to process\n")
    
    video_iter = tqdm(video_files, desc="Processing videos", unit="video")
    for video_path in video_iter:
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

