# Upload Your Videos Here

## Instructions

1. Upload all your MP4 video files to this folder
2. Each video should have a matching JSON file in `../annotations/`
3. JSON filename must match video filename (except extension)

## Example

- Video: `pig_video_001.mp4` → Upload here
- JSON: `pig_video_001.json` → Upload to `../annotations/`

## Supported Formats

- `.mp4` (recommended)
- `.avi`
- `.mov`

## After Uploading

Run: `./scripts/train_from_annotations.sh data/videos data/annotations`

