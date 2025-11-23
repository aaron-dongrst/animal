"""
Test trained YOLO model on a pig video.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.yolo_behavior_classifier import YOLOBehaviorClassifier

def main():
    if len(sys.argv) < 3:
        print("Usage: python test_pig_model.py <video_path> <model_path>")
        print("\nExample:")
        print("  python test_pig_model.py data/test_videos/pig_video.mp4 pig_behavior_classification/yolov8_pig_behavior/weights/best.pt")
        sys.exit(1)
    
    video_path = sys.argv[1]
    model_path = sys.argv[2]
    
    print("="*60)
    print("Pig Behavior Analysis")
    print("="*60)
    print()
    
    print("Loading YOLO model...")
    classifier = YOLOBehaviorClassifier(model_path=model_path)
    
    if classifier.model is None:
        print("Error: Model not loaded. Check model path.")
        sys.exit(1)
    
    print(f"Analyzing video: {video_path}")
    print()
    
    percentages = classifier.analyze_video_percentages(video_path)
    
    print("Behavior Percentages:")
    for behavior, percentage in sorted(percentages.items(), key=lambda x: x[1], reverse=True):
        print(f"  {behavior.capitalize():15s}: {percentage:6.1%}")
    
    # Calculate distress
    distress_result = classifier.calculate_distress_level(percentages)
    
    print()
    print("Distress Assessment:")
    print(f"  Distress Level:      {distress_result['distress_level'].upper()}")
    print(f"  Distress Percentage: {distress_result['distress_percentage']:.1%}")
    print(f"  Normal Percentage:   {distress_result['normal_percentage']:.1%}")
    print(f"  Is Distressed:       {'YES' if distress_result['is_distressed'] else 'NO'}")
    
    # Verify percentages sum to 1.0
    total = sum(percentages.values())
    print()
    print(f"Total: {total:.2f} {'✓' if abs(total - 1.0) < 0.01 else '✗ (ERROR)'}")

if __name__ == "__main__":
    main()

