# ⚡ Quick Start - DogVision

## What You Need to Do (Only 1 Thing!)

### ⭐ Upload Your Dog Videos

Upload videos to these folders:

```
data/dog_training/
├── train/          ← 80% of videos
│   ├── pacing/     ← Dogs pacing
│   ├── scratching/ ← Dogs scratching
│   ├── sleeping/   ← Dogs sleeping
│   ├── walking/    ← Dogs walking
│   └── resting/    ← Dogs resting
├── val/            ← 10% of videos (same structure)
└── test/           ← 10% of videos (same structure)
```

**That's it!** Everything else is ready.

---

## After Uploading Videos

1. **Train model:**
   ```bash
   ./scripts/run_all_steps.sh
   ```

2. **Configure:**
   ```bash
   export YOLO_MODEL_PATH="dog_behavior_classification/yolov8_dog_behavior/weights/best.pt"
   export OPENAI_API_KEY="your-key-here"
   ```

3. **Run:**
   ```bash
   # Backend
   cd backend && python app.py
   
   # Frontend (new terminal)
   cd frontend && npm start
   ```

4. **Use:** Open `http://localhost:3000`

---

## 📚 Need More Help?

- **`README.md`** - Main project overview
- **`docs/START_HERE.md`** - Quick start guide
- **`docs/EXACT_STEPS.md`** - Detailed instructions

---

**Everything is organized and ready! Just upload videos!** 🐕

