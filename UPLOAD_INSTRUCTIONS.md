# 📤 Exact Upload Instructions

## Where to Upload Your Files

### Step 1: Create Folders (if they don't exist)

```bash
mkdir -p data/videos
mkdir -p data/annotations
```

### Step 2: Upload Your Files

#### Videos → `data/videos/`

Upload all your MP4 video files here:

```
data/videos/
├── video1.mp4
├── video2.mp4
├── video3.mp4
└── ... (all your video files)
```

**Format:** `.mp4` files (or `.avi`, `.mov`)

---

#### JSON Annotations → `data/annotations/`

Upload JSON files with the **same filename** as the video (but `.json` extension):

```
data/annotations/
├── video1.json    ← Matches video1.mp4
├── video2.json    ← Matches video2.mp4
├── video3.json    ← Matches video3.mp4
└── ... (one JSON per video)
```

**Format:** `.json` files

**Important:** The JSON filename must match the video filename (except extension)

---

## JSON File Format

Each JSON file should contain a list of pig objects. Example:

```json
[
  {
    "tracking_id": 1,
    "frames": [0, 1, 2, 3, 4],
    "bounding_box": [
      [100, 150, 200, 250],
      [105, 152, 205, 252],
      [110, 155, 210, 255],
      [115, 157, 215, 257],
      [120, 160, 220, 260]
    ],
    "behavior_label": "tail_biting",
    "visibility": 1.0,
    "ground_truth": true
  },
  {
    "tracking_id": 2,
    "frames": [10, 11, 12, 13],
    "bounding_box": [
      [300, 200, 400, 300],
      [302, 201, 402, 301],
      [304, 202, 404, 302],
      [306, 203, 406, 303]
    ],
    "behavior_label": "eating",
    "visibility": 1.0,
    "ground_truth": true
  }
]
```

### JSON Fields Explained

- **`tracking_id`**: Unique ID for each pig in the video (number or string)
- **`frames`**: List of frame numbers where this pig appears (e.g., `[0, 1, 2, 3]`)
- **`bounding_box`**: List of bounding boxes, one per frame
  - Format: `[x1, y1, x2, y2]` (top-left and bottom-right corners)
  - OR: `[x, y, width, height]` (top-left corner + dimensions)
- **`behavior_label`**: One of: `"tail_biting"`, `"ear_biting"`, `"aggression"`, `"eating"`, `"sleeping"`, `"rooting"`
- **`visibility`**: Number between 0.0 and 1.0 (typically 1.0 for visible pigs)
- **`ground_truth`**: `true` or `false` (use `true` for training data)

---

## Example File Structure

After uploading, your structure should look like:

```
data/
├── videos/
│   ├── pig_video_001.mp4
│   ├── pig_video_002.mp4
│   └── pig_video_003.mp4
└── annotations/
    ├── pig_video_001.json
    ├── pig_video_002.json
    └── pig_video_003.json
```

**Note:** `pig_video_001.json` matches `pig_video_001.mp4`

---

## After Uploading

Once files are uploaded, run:

```bash
./scripts/train_from_annotations.sh data/videos data/annotations
```

This will:
1. Read each video file
2. Find matching JSON file
3. Extract labeled pig crops
4. Train the model

---

## Quick Checklist

- [ ] Videos uploaded to `data/videos/`
- [ ] JSON files uploaded to `data/annotations/`
- [ ] JSON filenames match video filenames (except extension)
- [ ] Each JSON contains list of pig objects
- [ ] Each pig object has: tracking_id, frames, bounding_box, behavior_label, visibility, ground_truth
- [ ] Behavior labels are: tail_biting, ear_biting, aggression, eating, sleeping, or rooting

---

**That's it! Upload and run the training script!** 🐷

