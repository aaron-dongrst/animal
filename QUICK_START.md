# ⚡ Quick Start - PigVision

## What You Need to Do (Only 1 Thing!)

### ⭐ Upload Your Pig Videos

Upload videos to these folders:

```
data/pig_training/
├── train/          ← 80% of videos
│   ├── tail_biting/    ← Pigs biting tails (distress)
│   ├── ear_biting/     ← Pigs biting ears (distress)
│   ├── aggression/     ← Aggressive behavior (distress)
│   ├── eating/         ← Pigs eating (normal)
│   ├── sleeping/       ← Pigs sleeping (normal)
│   └── rooting/        ← Pigs rooting (normal)
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
   export YOLO_MODEL_PATH="pig_behavior_classification/yolov8_pig_behavior/weights/best.pt"
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

## Behavior Classes

**Distress (3 classes):**
- `tail_biting` - Pigs biting tails
- `ear_biting` - Pigs biting ears
- `aggression` - Aggressive behavior

**Normal (3 classes):**
- `eating` - Pigs eating
- `sleeping` - Pigs sleeping
- `rooting` - Pigs rooting

---

**Everything is organized and ready! Just upload videos!** 🐷
