# FaunaVision Project Architecture

## Project Overview
**FaunaVision** (also referred to as ZooGuardian) is an AI-powered zoo animal surveillance and welfare monitoring system. It analyzes video footage of animals to classify their behavior and determine if they exhibit healthy or unhealthy patterns based on time-budget analysis.

---

## System Architecture

The system follows a **4-stage pipeline**:

1. **The Eye (Vision AI)** → Classifies actions in video
2. **The Brain (Logic Engine)** → Analyzes behavior patterns over time
3. **The Vet (GenAI)** → Generates veterinary reports using Gemini
4. **The Dashboard (UI)** → Displays results to zookeepers

---

## Component Breakdown

### 🎨 **FRONTEND: Dashboard** (`dashboard/app.py`)

**Status**: Currently empty/placeholder

**Intended Purpose**:
- Web-based user interface (planned to use Streamlit)
- Display video player on the left side
- Show statistics and health status on the right side
- Display real-time animal behavior classifications
- Show health alerts (Green/Red status indicators)
- Present Gemini-generated veterinary advice

**Planned Features**:
- Video upload/playback interface
- Real-time classification results
- Health status dashboard
- Alert notifications
- Veterinary report viewer

**Technology Stack**:
- Streamlit (Python web framework)
- HTML/CSS for styling
- Video display components

---

### ⚙️ **BACKEND: Processing Logic**

The backend consists of several Python modules in the `src/` directory:

#### 1. **Vision Engine** (`src/vision_engine.py`) ✅ **IMPLEMENTED**

**Purpose**: Core video classification engine using deep learning

**Key Components**:
- **Model**: VideoMAE (MCG-NJU/videomae-base-finetuned-kinetics) from Hugging Face
- **Framework**: PyTorch with Transformers library
- **Input**: Video file path (.mp4)
- **Output**: Action labels with confidence scores (e.g., "walking", "eating", "sleeping")

**How It Works**:
1. Extracts 16 uniformly sampled frames from video using OpenCV
2. Preprocesses frames using VideoMAEImageProcessor
3. Runs inference through VideoMAE model (pre-trained on Kinetics-400 dataset)
4. Returns top-k predictions with confidence scores

**Key Methods**:
- `extract_frames()`: Samples frames from video
- `classify_video()`: Returns top-k action predictions
- `get_top_prediction()`: Returns single best prediction

**Dependencies**:
- `torch` (PyTorch)
- `transformers` (Hugging Face)
- `opencv-python` (video processing)
- `numpy` (array operations)

---

#### 2. **Vision Classifier** (`src/vision_classifier.py`)

**Status**: Empty/placeholder

**Intended Purpose**: 
- Wrapper around VisionEngine
- Map 400 Kinetics classes to 5 simplified categories:
  - Moving
  - Eating
  - Resting
  - Grooming
  - Interaction

---

#### 3. **Budget Logic** (`src/budget_logic.py`)

**Status**: Empty/placeholder

**Intended Purpose**: 
- Analyze behavior patterns over time
- Track duration of consecutive actions
- Apply biological thresholds per animal species
- Determine Healthy (1) vs Unhealthy (0) status

**Planned Logic**:
```python
THRESHOLDS = {
    "rabbit": {
        "sleeping_max_min": 240,  # 4 hours max
        "pacing_max_min": 20,     # 20 mins max (stress indicator)
    },
    "macaque": {
        "sleeping_max_min": 120,
        "pacing_max_min": 45,
    }
}
```

**Key Concept**: 
- **Healthy**: Animal switches between behaviors within normal time limits
- **Unhealthy**: Animal gets stuck in repetitive behavior (e.g., pacing >2 hours, sleeping >12 hours)

---

#### 4. **Vet Reporter** (`src/vet_reporter.py`)

**Status**: Empty/placeholder

**Intended Purpose**:
- Generate veterinary reports using Google Gemini AI
- Take unhealthy behavior alerts and create readable explanations
- Provide medical context and enrichment suggestions

**Planned Workflow**:
1. Receive status code (0 = unhealthy) and reason (e.g., "Excessive Pacing")
2. Query knowledge base (animal care manual)
3. Send prompt to Gemini API with context
4. Return formatted veterinary report

**Technology**:
- Google Generative AI (Gemini API)
- RAG-lite approach (text file knowledge base)

---

### 🤖 **MODEL: Deep Learning Components**

#### 1. **VideoMAE Model** (Currently Used)

**Location**: Loaded from Hugging Face at runtime

**Model Details**:
- **Name**: `MCG-NJU/videomae-base-finetuned-kinetics`
- **Architecture**: Video Masked Autoencoder (VideoMAE)
- **Training Dataset**: Kinetics-400 (400 action classes)
- **Input**: 16 frames sampled from video
- **Output**: 400 action class probabilities

**Advantages**:
- Easy to use (Hugging Face integration)
- Pre-trained, no training required
- Good general-purpose action recognition

**Limitations**:
- Not specifically trained on animal behaviors
- 400 classes may include irrelevant actions
- Needs mapping to animal-specific behaviors

---

#### 2. **SlowFast Model** (Downloaded but Not Used)

**Location**: `models/weights/SLOWFAST_8x8_R50.pkl`

**Model Details**:
- **Architecture**: SlowFast (Facebook Research)
- **Training Dataset**: Kinetics-400
- **Config**: `models/configs/SLOWFAST_8x8_R50.yaml`

**Status**: 
- Weights downloaded via `models/download.py`
- Not currently integrated into the codebase
- Intended as alternative/upgrade option

**Download Script**: `models/download.py`
- Downloads SlowFast weights from Facebook Research
- Downloads configuration YAML
- Includes progress bar for downloads

---

## Data Flow

```
1. Video Upload
   ↓
2. Vision Engine (vision_engine.py)
   - Extracts frames
   - Classifies actions
   ↓
3. Vision Classifier (vision_classifier.py) [TODO]
   - Maps to 5 categories
   - Creates timestamped CSV
   ↓
4. Budget Logic (budget_logic.py) [TODO]
   - Analyzes time patterns
   - Applies thresholds
   - Determines health status
   ↓
5. Vet Reporter (vet_reporter.py) [TODO]
   - Generates Gemini report (if unhealthy)
   ↓
6. Dashboard (dashboard/app.py) [TODO]
   - Displays results
   - Shows alerts
```

---

## File Structure

```
Faunavision/
├── dashboard/
│   └── app.py                    # Frontend UI (Streamlit) [EMPTY]
│
├── src/                          # Backend Logic
│   ├── vision_engine.py          # ✅ Video classification (IMPLEMENTED)
│   ├── vision_classifier.py      # ⏳ Class mapping [EMPTY]
│   ├── budget_logic.py           # ⏳ Time-budget analysis [EMPTY]
│   └── vet_reporter.py           # ⏳ Gemini report generation [EMPTY]
│
├── models/
│   ├── weights/
│   │   └── SLOWFAST_8x8_R50.pkl  # SlowFast weights (downloaded)
│   ├── configs/
│   │   └── SLOWFAST_8x8_R50.yaml # SlowFast config
│   └── download.py               # Model download script
│
├── data/
│   ├── raw_videos/               # Input videos
│   │   ├── Healthy/
│   │   └── Not Healthy/
│   ├── annotations/              # Manual annotations
│   └── logs/                     # Processing logs
│
├── Main.py                       # Main entry point [EMPTY]
├── config.yaml                   # Configuration [EMPTY]
├── requirements.txt              # Python dependencies
└── test_vision_engine.py         # Test script for vision engine
```

---

## Current Implementation Status

### ✅ **Fully Implemented**:
- **Vision Engine**: Complete video classification pipeline
- **Model Download**: Script to download SlowFast weights
- **Testing**: Test script for batch video processing

### ⏳ **Partially Implemented**:
- **Main Entry Point**: `Main.py` exists but is empty
- **Configuration**: `config.yaml` exists but is empty

### ❌ **Not Implemented**:
- **Frontend Dashboard**: Empty placeholder
- **Vision Classifier**: Class mapping logic
- **Budget Logic**: Time-budget analysis
- **Vet Reporter**: Gemini integration

---

## Dependencies

**Core ML & Video Processing**:
- `torch>=2.0.0` - PyTorch deep learning framework
- `transformers>=4.30.0` - Hugging Face transformers
- `opencv-python>=4.8.0` - Video processing
- `pillow>=10.0.0` - Image processing
- `numpy>=1.24.0` - Numerical operations

**Data Processing**:
- `pandas>=2.0.0` - Data manipulation
- `openpyxl>=3.1.0` - Excel file handling

**Generative AI**:
- `google-generativeai>=0.3.0` - Gemini API

**Utilities**:
- `python-dotenv>=1.0.0` - Environment variables

**Missing (for planned features)**:
- `streamlit` - Frontend framework (not in requirements.txt yet)

---

## Key Concepts

### Time-Budget Analysis
The core innovation is not just detecting "sick" movements, but monitoring **behavioral time budgets**:
- Healthy animals switch between activities (sleep → eat → walk → groom)
- Unhealthy animals get stuck in repetitive loops (e.g., pacing for hours)
- Thresholds are species-specific and biologically informed

### Two-Stage Classification
1. **Action Recognition**: What is the animal doing? (Vision Engine)
2. **Pattern Analysis**: Is this pattern healthy? (Budget Logic)

---

## Next Steps for Completion

1. **Implement Vision Classifier**: Map 400 classes → 5 categories
2. **Implement Budget Logic**: Time-budget analysis with thresholds
3. **Implement Vet Reporter**: Gemini API integration
4. **Build Dashboard**: Streamlit UI with video player and stats
5. **Create Main Pipeline**: Connect all components in `Main.py`
6. **Add Configuration**: Populate `config.yaml` with thresholds and API keys

---

## Testing

The project includes `test_vision_engine.py` which:
- Tests VisionEngine on all videos in `data/raw_videos/`
- Processes both "Healthy" and "Not Healthy" categories
- Displays top-3 predictions for each video
- Provides summary statistics

**Usage**:
```bash
python test_vision_engine.py
```

---

## Summary

**FaunaVision** is a sophisticated animal welfare monitoring system that combines:
- **Computer Vision** (VideoMAE/SlowFast models)
- **Behavioral Analysis** (Time-budget logic)
- **Generative AI** (Gemini for reports)
- **Web Interface** (Streamlit dashboard)

Currently, only the **Vision Engine** is fully implemented. The remaining components (classifier, logic, reporter, dashboard) are placeholders waiting for implementation.

