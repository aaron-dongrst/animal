"""
Extract frames from pig behavior videos for YOLO training.
"""
import cv2
import os
from pathlib import Path

def extract_frames(video_dir, output_dir, fps_interval=1.0):
    """
    Extract frames from videos in video_dir and save to output_dir.
    
    Args:
        video_dir: Directory containing videos
        output_dir: Where to save extracted frames
        fps_interval: Extract every N seconds (default: 1.0)
    """
    video_dir = Path(video_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    video_files = list(video_dir.glob("*.mp4")) + \
                  list(video_dir.glob("*.avi")) + \
                  list(video_dir.glob("*.mov"))
    
    print(f"Found {len(video_files)} videos in {video_dir}")
    
    for video_path in video_files:
        print(f"Processing: {video_path.name}")
        
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * fps_interval) if fps > 0 else 1
        
        frame_count = 0
        saved_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                # Save frame
                frame_filename = f"{video_path.stem}_{saved_count:06d}.jpg"
                frame_path = output_dir / frame_filename
                cv2.imwrite(str(frame_path), frame)
                saved_count += 1
            
            frame_count += 1
        
        cap.release()
        print(f"  Extracted {saved_count} frames")
    
    print(f"\nDone! Frames saved to: {output_dir}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python extract_frames.py <video_dir> <output_dir> [fps_interval]")
        print("\nExample:")
        print("  python extract_frames.py data/pig_training/train/tail_biting data/pig_frames/train/tail_biting 1.0")
        sys.exit(1)
    
    video_dir = sys.argv[1]
    output_dir = sys.argv[2]
    fps_interval = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    extract_frames(video_dir, output_dir, fps_interval)

