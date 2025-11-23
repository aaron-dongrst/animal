# FaunaVision - Pig Behavior Analysis System

AI-powered system for analyzing pig behavior and health using computer vision and AI.

## Quick Start

### Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export YOLO_MODEL_PATH="models/best.pt"
export PORT=5001
export USE_GEMINI=true
export GEMINI_API_KEY="your-api-key-here"

# Start backend
python backend/app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Project Structure

```
Faunavision/
├── backend/           # Flask API server
│   ├── app.py        # Main API endpoints
│   └── start.sh      # Startup script
├── frontend/          # React frontend
│   └── src/          # React components
├── src/               # Core modules
│   └── yolo_behavior_classifier.py
├── scripts/           # Training and data processing scripts
│   ├── train_pig_behavior.py
│   ├── parse_annotations.py
│   └── prepare_yolo_from_crops.py
├── models/            # Trained YOLO models (gitignored)
├── data/              # Training data (gitignored)
└── Train_on_Colab.ipynb  # Google Colab training notebook
```

## Features

- **Dual Model Analysis**: Combines YOLO (20%) and Gemini Vision (80%) for behavior detection
- **6 Behavior Classes**: tail_biting, ear_biting, aggression, eating, sleeping, rooting
- **Health Assessment**: AI-powered health evaluation using behavior patterns
- **Video Upload**: Upload videos for real-time analysis

## API Endpoints

- `GET /health` - Health check
- `POST /analyze` - Analyze pig video and get health assessment

## Training

See `Train_on_Colab.ipynb` for training the YOLO model on Google Colab.

## Requirements

See `requirements.txt` for Python dependencies.

