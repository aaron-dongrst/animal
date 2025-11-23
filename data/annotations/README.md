# Upload Your JSON Annotation Files Here

## Instructions

1. Upload JSON files with the **same filename** as your videos (but `.json` extension)
2. Each JSON file should contain a list of pig objects with annotations

## Example

If you have `data/videos/pig_video_001.mp4`, upload `pig_video_001.json` here.

## JSON Format

Each JSON file should be a list of pig objects:

```json
[
  {
    "tracking_id": 1,
    "frames": [0, 1, 2, 3],
    "bounding_box": [[x1, y1, x2, y2], ...],
    "behavior_label": "tail_biting",
    "visibility": 1.0,
    "ground_truth": true
  }
]
```

## Behavior Labels

Use one of these exact labels:
- `"tail_biting"`
- `"ear_biting"`
- `"aggression"`
- `"eating"`
- `"sleeping"`
- `"rooting"`

## See Also

- `example.json` - Complete example file
- `../UPLOAD_INSTRUCTIONS.md` - Detailed instructions
