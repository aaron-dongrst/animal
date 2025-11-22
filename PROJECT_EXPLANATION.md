# FaunaVision Project Explanation

## What Is This Project?

**FaunaVision** (also called ZooGuardian) is an **AI-powered zoo animal surveillance and welfare monitoring system**. It watches videos of zoo animals, analyzes their behavior patterns, and determines if they're healthy or unhealthy based on **time-budget analysis**.

---

## The Core Innovation: Time-Budget Analysis

### Traditional Approach (What We're NOT Doing):
- ❌ Looking for "sick" movements (hard to find data for)
- ❌ Detecting specific diseases from video
- ❌ One-time classification

### Our Approach (Time-Budget Analysis):
- ✅ **Monitor how long behaviors persist**
- ✅ **Track behavior patterns over time**
- ✅ **Detect when animals get "stuck" in repetitive loops**

### The Key Insight:
- **Healthy animals** switch between behaviors: Sleep → Eat → Walk → Groom (within normal time limits)
- **Unhealthy animals** get stuck in one behavior: Pacing for 2+ hours, or sleeping for 12+ hours straight

**Example:**
- A bear pacing back and forth for 30 minutes = **Healthy** (normal exploration)
- A bear pacing for 3 hours straight = **Unhealthy** (stress/zoochosis indicator)

---

## System Architecture: The 4-Stage Pipeline

The system follows a linear pipeline with 4 main components:

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT: Video File                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: The Eye (Vision AI)                               │
│  ────────────────────────────────────────────────────────   │
│  • Watches video                                            │
│  • Extracts frames                                          │
│  • Classifies actions (e.g., "walking", "eating")          │
│  • Outputs: Action labels every second                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: The Brain (Logic Engine)                         │
│  ────────────────────────────────────────────────────────   │
│  • Tracks duration of consecutive actions                   │
│  • Applies biological thresholds                            │
│  • Example: "Rabbits shouldn't pace for >20 minutes"       │
│  • Outputs: Health status (0=unhealthy, 1=healthy) + reason │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: The Vet (GenAI)                                  │
│  ────────────────────────────────────────────────────────   │
│  • If unhealthy detected, queries knowledge base            │
│  • Uses Google Gemini to generate veterinary report         │
│  • Explains why the behavior is concerning                 │
│  • Suggests enrichment activities                           │
│  • Outputs: Readable veterinary report                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 4: The Dashboard (UI)                               │
│  ────────────────────────────────────────────────────────   │
│  • Displays video player                                    │
│  • Shows health status (Green/Red)                         │
│  • Displays Gemini veterinary advice                        │
│  • Visualizes behavior patterns                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Vision Engine (`src/vision_engine.py`) ✅ **FULLY IMPLEMENTED**

**What it does:**
- Uses a pre-trained deep learning model (VideoMAE) to classify actions in videos
- Extracts 16 frames uniformly from a video
- Classifies what action is happening (e.g., "walking the dog", "climbing ladder", "eating carrots")
- Returns top predictions with confidence scores

**How it works:**
1. Takes a video file path as input
2. Extracts 16 frames uniformly spaced throughout the video
3. Preprocesses frames for the VideoMAE model
4. Runs inference through the neural network
5. Returns top-k action predictions (e.g., "walking the dog: 71.72% confidence")

**Current Status:** ✅ Working perfectly
- Model: `MCG-NJU/videomae-base-finetuned-kinetics` (Hugging Face)
- Pre-trained on Kinetics-400 dataset (400 human action classes)
- Can classify videos successfully

**Limitation:** 
- Model was trained on human actions, not animal-specific behaviors
- Some predictions may not perfectly match animal behaviors (e.g., "walking the dog" for a bear pacing)

---

### 2. Vision Classifier (`src/vision_classifier.py`) ⚠️ **PARTIALLY IMPLEMENTED**

**What it should do:**
- Process video frame-by-frame over time (every second)
- Generate timestamped CSV logs with action labels
- Map 400 Kinetics classes → 5 simple categories: Moving, Eating, Resting, Grooming, Interaction

**What it currently does:**
- Has a simple mapping dictionary
- Can classify individual actions as "Healthy" or "Not Healthy"
- **Missing:** Time-series processing, CSV generation

**What's needed:**
- Process video at regular intervals (every 1 second)
- Generate CSV with columns: `timestamp, action_label, confidence, category`
- This CSV feeds into the Budget Logic component

---

### 3. Budget Logic (`src/budget_logic.py`) ❌ **EMPTY**

**What it should do:**
- Read timestamped CSV from Vision Classifier
- Track consecutive behavior durations
- Apply species-specific thresholds
- Detect unhealthy patterns
- Return health status (0=unhealthy, 1=healthy) with detailed reasoning

**Example Logic:**
```python
# If bear has been pacing for 35 minutes
if consecutive_pacing_duration > 30 minutes:
    return status=0, reason="Excessive pacing: 35 min (threshold: 30 min)"
```

**What's needed:**
- Algorithm to group consecutive behaviors
- Threshold dictionary (e.g., bear: pacing_max=30min, sleeping_max=8hours)
- Logic to detect threshold violations
- Generate health status and reason

**This is the CORE missing piece** - it's the "brain" that determines healthy vs unhealthy.

---

### 4. Vet Reporter (`src/vet_reporter.py`) ⚠️ **PARTIALLY IMPLEMENTED**

**What it should do:**
- Take unhealthy behavior alerts from Budget Logic
- Query knowledge base (animal care manuals)
- Use Google Gemini API to generate readable veterinary reports
- Explain medical risks and suggest enrichment activities

**What it currently does:**
- Can save results to Excel
- **Missing:** Gemini API integration, knowledge base querying

**What's needed:**
- Google Gemini API integration
- Knowledge base files (e.g., `rabbit_care_manual.txt`)
- Prompt engineering to generate veterinary reports

---

### 5. Dashboard (`dashboard/app.py`) ⚠️ **BASIC IMPLEMENTATION**

**What it should do:**
- Display video player on left
- Show health status (Green/Red) on right
- Display Gemini veterinary advice
- Visualize behavior patterns over time
- Real-time processing integration

**What it currently does:**
- Basic Streamlit UI
- Can load Excel reports
- **Missing:** Video player, real-time processing, pipeline integration

---

### 6. Main Pipeline (`Main.py`) ❌ **EMPTY**

**What it should do:**
- Orchestrate the entire pipeline
- Connect all components in sequence
- Process videos from config
- Handle errors gracefully
- Generate summary reports

**What's needed:**
- Script that calls: Vision Engine → Vision Classifier → Budget Logic → Vet Reporter
- Configuration loading
- Error handling
- Logging

---

## How It All Comes Together (Ideal Flow)

### Step-by-Step Example:

**Input:** Video of a polar bear pacing for 5 minutes

1. **Vision Engine** processes the video:
   - Extracts frames
   - Classifies: "walking the dog" (71.72% confidence)

2. **Vision Classifier** processes over time:
   - Every 1 second, classifies the action
   - Generates CSV:
     ```
     timestamp,action_label,confidence,category
     0.0,walking the dog,0.72,Moving
     1.0,walking the dog,0.68,Moving
     2.0,walking the dog,0.75,Moving
     ...
     300.0,walking the dog,0.70,Moving
     ```

3. **Budget Logic** analyzes the CSV:
   - Detects: "Moving" behavior for 5 minutes (300 seconds)
   - Checks threshold: Bear pacing max = 30 minutes
   - Result: 5 min < 30 min → **Status: 1 (Healthy)**
   - Reason: "Healthy behavior pattern: Moving: 5.0min"

4. **Vet Reporter** (if unhealthy):
   - If status was 0, would generate Gemini report
   - Explains why pacing is concerning
   - Suggests enrichment activities

5. **Dashboard** displays:
   - Video player showing the bear
   - Green status indicator (healthy)
   - Behavior timeline
   - Summary statistics

---

## Current Implementation Status

### ✅ **Fully Working:**
- **Vision Engine**: Can classify videos successfully
- **Test Script**: `test_vision_engine.py` works perfectly

### ⚠️ **Partially Implemented:**
- **Vision Classifier**: Has basic mapping, needs time-series processing
- **Vet Reporter**: Can save to Excel, needs Gemini integration
- **Dashboard**: Basic UI, needs pipeline integration

### ❌ **Missing:**
- **Budget Logic**: Empty file - this is the critical missing piece
- **Main Pipeline**: Empty file - needs orchestration
- **Configuration**: Basic, needs thresholds

---

## The Missing Link: Budget Logic

The **Budget Logic** component is the most critical missing piece. It's what makes this project unique - it's not just classifying actions, but analyzing **behavior patterns over time**.

**What it needs to do:**
1. Read CSV with timestamped behaviors
2. Group consecutive behaviors (e.g., "Moving" for 5 minutes straight)
3. Check against thresholds (e.g., "Bear pacing > 30 min = unhealthy")
4. Return health status with reasoning

**Example Thresholds:**
```python
thresholds = {
    "bear": {
        "pacing": 30,      # 30 minutes max
        "sleeping": 480,    # 8 hours max
    },
    "rabbit": {
        "pacing": 20,       # 20 minutes (high stress indicator)
        "sleeping": 240,    # 4 hours max
    }
}
```

---

## Why This Approach Works

### Advantages:
1. **No need for "sick animal" training data** - we use pre-trained models
2. **Biologically informed** - based on time-budget research
3. **Scalable** - works for any animal species (just adjust thresholds)
4. **Explainable** - clear reasoning (e.g., "pacing for 3 hours exceeds 30 min threshold")

### Challenges:
1. **Model mismatch**: VideoMAE trained on human actions, not animals
2. **Threshold definition**: Need biological research to set accurate thresholds
3. **Real-time processing**: Currently processes whole videos, not live streams

---

## Next Steps to Complete the Project

1. **Implement Budget Logic** (`src/budget_logic.py`)
   - Track consecutive behaviors
   - Apply thresholds
   - Generate health status

2. **Enhance Vision Classifier** (`src/vision_classifier.py`)
   - Process video over time
   - Generate timestamped CSV

3. **Create Main Pipeline** (`Main.py`)
   - Connect all components
   - Process videos end-to-end

4. **Integrate Gemini** (`src/vet_reporter.py`)
   - Add API integration
   - Generate veterinary reports

5. **Enhance Dashboard** (`dashboard/app.py`)
   - Add video player
   - Real-time processing
   - Better visualizations

---

## Summary

**FaunaVision** is a time-budget analysis system that:
- ✅ Uses AI to classify animal behaviors in videos
- ⚠️ Needs logic to analyze behavior patterns over time
- ⚠️ Needs integration to connect all components
- ❌ Missing the core "Budget Logic" that determines healthy vs unhealthy

The **Vision Engine** is working perfectly and can classify videos. The missing piece is the **Budget Logic** that analyzes these classifications over time to determine health status based on behavior duration thresholds.

