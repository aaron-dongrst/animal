# FaunaVision - Pig Behavior Analysis System

AI-powered system for analyzing pig behavior and health using computer vision and AI.

## About the Project

### Inspiration

FaunaVision was inspired by the critical need for early detection of animal distress behaviors in agricultural and research settings. Traditional monitoring methods are labor-intensive and often miss subtle behavioral indicators of health issues. By automating behavior analysis through computer vision, we can enable proactive intervention and improve animal welfare outcomes.

### What We Learned

This project provided hands-on experience with several cutting-edge technologies:

- **Computer Vision**: Training YOLO models for behavior classification from video frames
- **Multi-modal AI**: Integrating vision models (YOLO) with large language models (Gemini) for comprehensive analysis
- **Video Processing**: Frame extraction, temporal analysis, and behavior time-budget calculations
- **Full-Stack Development**: Building a React frontend with Flask backend API
- **Ensemble Methods**: Combining multiple AI models with weighted averaging: $$\text{final} = 0.8 \times \text{Gemini} + 0.2 \times \text{YOLO} + \epsilon$$ where $\epsilon$ represents added noise for realism

### How We Built It

**Backend Architecture:**
- Flask API server handling video uploads and processing
- YOLO model for frame-by-frame behavior classification (6 classes: tail_biting, ear_biting, aggression, eating, sleeping, rooting)
- Gemini Vision API for direct video analysis and behavior estimation
- Weighted ensemble combining both models (80% Gemini, 20% YOLO) with ±5% noise
- Gemini API for health assessment using behavior percentages and animal parameters

**Frontend:**
- React application with modern UI/UX design
- Multi-page landing experience with smooth animations
- Real-time video upload and analysis interface
- Comprehensive results visualization with behavior distributions

**Training Pipeline:**
- JSON annotation parsing from video tracking data
- Automated frame extraction and pig cropping
- YOLO dataset preparation for classification training
- Google Colab integration for cloud-based model training

### Challenges Faced

1. **Video Processing Complexity**: Handling large video files, frame extraction, and temporal analysis required careful memory management and optimization.

2. **Model Integration**: Combining YOLO (specialized behavior detection) with Gemini Vision (general video understanding) required developing a robust ensemble method that balanced accuracy and reliability.

3. **Data Annotation**: Converting raw JSON tracking data with bounding boxes and behavior labels into a format suitable for YOLO classification training involved complex data preprocessing pipelines.

4. **API Compatibility**: Navigating different API versions and model availability (e.g., `gemini-pro` → `gemini-1.5-flash` → `models/gemini-2.0-flash`) required iterative testing and adaptation.

5. **Real-time Performance**: Ensuring the system could process videos efficiently while maintaining accuracy, leading to frame sampling strategies and confidence threshold tuning.

6. **Frontend-Backend Communication**: Handling large file uploads, CORS configuration, and error handling across the full stack required careful design of the API contract.

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

