"""
Test script to run the vision engine on all available videos.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from vision_engine import VisionEngine


def test_all_videos():
    """Test the vision engine on all videos in data/raw_videos."""
    
    # Initialize the vision engine
    print("Initializing Vision Engine...")
    print("=" * 80)
    engine = VisionEngine()
    print("\n")
    
    # Define video paths
    video_dirs = {
        "Healthy": "data/raw_videos/Healthy",
        "Not Healthy": "data/raw_videos/Not Healthy"
    }
    
    results = []
    
    # Process each category
    for category, directory in video_dirs.items():
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            continue
        
        video_files = [f for f in os.listdir(directory) if f.endswith('.mp4')]
        
        if not video_files:
            print(f"No .mp4 files found in directory: {directory}")
            continue
        
        print(f"\n{'='*80}")
        print(f"Testing {category} Videos")
        print(f"{'='*80}\n")
        
        for video_file in video_files:
            video_path = os.path.join(directory, video_file)
            
            print(f"\n📹 Video: {video_file}")
            print(f"   Category: {category}")
            print(f"   Path: {video_path}")
            print("-" * 80)
            
            try:
                # Check if the file is a valid video
                if not os.path.isfile(video_path):
                    raise ValueError(f"File not found or not a valid file: {video_path}")
                
                # Get predictions
                predictions = engine.classify_video(video_path, top_k=3)
                
                top_label = predictions[0]['label']
                top_conf = predictions[0]['confidence']
                
                print(f"\n✅ Top Prediction: {top_label}")
                print(f"   Confidence: {top_conf:.2%}\n")
                
                print("   Top 3 Predictions:")
                for i, pred in enumerate(predictions, 1):
                    print(f"     {i}. {pred['label']:<40} {pred['confidence']:.2%}")
                
                results.append({
                    'video': video_file,
                    'category': category,
                    'top_prediction': top_label,
                    'confidence': top_conf,
                    'all_predictions': predictions
                })
                
            except ValueError as ve:
                print(f"\n❌ ValueError: {str(ve)}")
                results.append({
                    'video': video_file,
                    'category': category,
                    'error': f"ValueError: {str(ve)}"
                })
            except Exception as e:
                print(f"\n❌ Error processing {video_file}: {str(e)}")
                results.append({
                    'video': video_file,
                    'category': category,
                    'error': str(e)
                })
            
            print("\n" + "=" * 80)
    
    # Summary
    print(f"\n\n{'='*80}")
    print("SUMMARY OF ALL CLASSIFICATIONS")
    print(f"{'='*80}\n")
    
    for result in results:
        if 'error' not in result:
            print(f"📹 {result['video']:<30} [{result['category']}]")
            print(f"   → {result['top_prediction']:<40} ({result['confidence']:.1%})")
        else:
            print(f"❌ {result['video']:<30} [{result['category']}]")
            print(f"   → Error: {result['error']}")
        print()
    
    print(f"{'='*80}\n")
    print(f"✅ Successfully processed {len([r for r in results if 'error' not in r])} videos")
    print(f"❌ Failed to process {len([r for r in results if 'error' in r])} videos")
    print()


if __name__ == "__main__":
    test_all_videos()
