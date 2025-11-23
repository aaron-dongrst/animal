# 🐷 PigVision - Pig Distress Detection

AI-powered system to detect pig distress behaviors through video analysis.

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install ultralytics
cd frontend && npm install
```

### 2. Upload Videos and Annotations ⭐

**Option A: Using JSON Annotations (Recommended)**
1. Place videos in `data/videos/`
2. Place JSON annotation files in `data/annotations/` (same filename as video, but .json)
3. Run: `./scripts/train_from_annotations.sh data/videos data/annotations`

**Option B: Manual Organization**
Upload videos to `data/pig_training/train/` folders (tail_biting, ear_biting, etc.)
Then run: `./scripts/run_all_steps.sh`

### 3. Train Model

**With annotations:**
```bash
./scripts/train_from_annotations.sh data/videos data/annotations
```

**Manual organization:**
```bash
./scripts/run_all_steps.sh
```

### 4. Run Application
```bash
# Set environment variables
export YOLO_MODEL_PATH="pig_behavior_classification/yolov8_pig_behavior/weights/best.pt"
export OPENAI_API_KEY="your-key-here"

# Start backend
cd backend && python app.py

# Start frontend (new terminal)
cd frontend && npm start
```

Open `http://localhost:3000`

---

## JSON Annotation Format

Each JSON file should contain a list of pig objects:

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

See `data/annotations/README.md` for details and `data/annotations/example.json` for an example.

---

## Behavior Classes

**Distress (3):** tail_biting, ear_biting, aggression  
**Normal (3):** eating, sleeping, rooting

---

## Scripts

- `scripts/train_from_annotations.sh` - Train using JSON annotations (recommended)
- `scripts/run_all_steps.sh` - Train with manually organized videos
- `scripts/parse_annotations.py` - Parse JSON and extract crops
- `scripts/train_pig_behavior.py` - Train YOLO model

---

## Train on Google Colab

Don't have a GPU? Use `Train_on_Colab.ipynb` - see `COLAB_TRAINING_GUIDE.md`

---

**Ready? Upload videos + JSON annotations and run training!** 🐷
