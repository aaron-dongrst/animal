# 🐷 PigVision - Pig Distress Detection System

AI-powered system to detect pig distress behaviors through video analysis using YOLO and OpenAI/Gemini.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install ultralytics
cd frontend && npm install
```

### 2. Upload Pig Videos ⭐
Upload your pig behavior videos to:
- `data/pig_training/train/tail_biting/` - Pigs biting tails (distress)
- `data/pig_training/train/ear_biting/` - Pigs biting ears (distress)
- `data/pig_training/train/aggression/` - Aggressive behavior (distress)
- `data/pig_training/train/eating/` - Pigs eating (normal)
- `data/pig_training/train/sleeping/` - Pigs sleeping (normal)
- `data/pig_training/train/rooting/` - Pigs rooting (normal)

**Split your videos:**
- 80% → `train/` folders
- 10% → `val/` folders
- 10% → `test/` folders

### 3. Train Model
```bash
./scripts/run_all_steps.sh
```

### 4. Configure & Run
```bash
# Set environment variables
export YOLO_MODEL_PATH="pig_behavior_classification/yolov8_pig_behavior/weights/best.pt"
export OPENAI_API_KEY="your-key-here"

# Start backend
cd backend && python app.py

# Start frontend (in new terminal)
cd frontend && npm start
```

### 5. Use the App
Open `http://localhost:3000` in your browser!

---

## 📁 Project Structure

```
Faunavision/
├── README.md              ← You are here
├── data/
│   └── pig_training/      ← ⭐ UPLOAD VIDEOS HERE
│       ├── train/         ← 80% of videos
│       ├── val/           ← 10% of videos
│       └── test/          ← 10% of videos
├── scripts/               ← Training scripts
│   └── run_all_steps.sh  ← Run everything
├── frontend/              ← React UI (PigVision)
├── backend/               ← Flask API
└── src/                   ← Core modules
```

---

## 🐷 Behavior Classes

**Distress Behaviors:**
- `tail_biting` - Pigs biting other pigs' tails
- `ear_biting` - Pigs biting other pigs' ears
- `aggression` - Aggressive interactions

**Normal Behaviors:**
- `eating` - Pigs eating food
- `sleeping` - Pigs sleeping/resting
- `rooting` - Pigs rooting in substrate

---

## 🎯 What You Need to Do

1. ✅ **Install dependencies** (one time)
2. ⭐ **Upload pig videos** to `data/pig_training/` folders
3. ✅ **Run training**: `./scripts/run_all_steps.sh`
4. ✅ **Configure & run** backend and frontend
5. ✅ **Use the app**!

---

## 🐷 How It Works

1. **Upload video** → Frontend
2. **Process with YOLO** → Classify behaviors (tail_biting, ear_biting, aggression, eating, sleeping, rooting)
3. **Calculate percentages** → Time spent in each behavior
4. **Analyze with AI** → Determine distress level
5. **Display results** → Behavior breakdown + health recommendations

---

## 🎨 Features

- ✅ Pig-themed UI (warm pink/red colors)
- ✅ Video upload and analysis
- ✅ Behavior classification (6 pig behaviors)
- ✅ Distress detection based on behavior percentages
- ✅ Health recommendations via OpenAI/Gemini

---

## 📋 Requirements

- Python 3.8+
- Node.js 14+
- Pig behavior videos (50-100+ per behavior class)
- OpenAI API key (or Gemini API key)

---

## 🔧 Scripts

- `scripts/run_all_steps.sh` - Run complete training pipeline
- `scripts/extract_frames.py` - Extract frames from videos
- `scripts/prepare_yolo_dataset.py` - Prepare YOLO dataset
- `scripts/train_pig_behavior.py` - Train YOLO model
- `scripts/test_pig_model.py` - Test trained model

---

## 📖 Documentation

- `data/pig_training/README.md` - Video upload instructions
- `backend/README.md` - Backend API docs
- `frontend/README.md` - Frontend docs

---

## 🚀 Ready to Start?

1. Upload videos to `data/pig_training/`
2. Run `./scripts/run_all_steps.sh`
3. Start using PigVision!

---

**Made with ❤️ for pig health monitoring**
