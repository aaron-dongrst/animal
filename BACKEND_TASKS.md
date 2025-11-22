# Backend Tasks You Can Work On

Since your friends are handling:
- **Friend 1**: CV/AI model improvements (Vision Engine)
- **Friend 2**: Frontend (Dashboard)

Here are the **backend components** you can work on (non-CV/AI, non-frontend):

---

## 🎯 Priority 1: Budget Logic (CRITICAL - Core Feature)

**File:** `src/budget_logic.py` (currently **EMPTY**)

**What it does:**
This is the **core innovation** of the project - time-budget analysis. It determines if an animal is healthy or unhealthy based on behavior duration.

**Your tasks:**
1. Create `BudgetLogic` class
2. Implement behavior tracking algorithm:
   - Read CSV with timestamped behaviors
   - Group consecutive behaviors (e.g., "pacing" for 5 minutes straight)
   - Calculate duration of each behavior segment
3. Implement threshold checking:
   - Load species-specific thresholds from config
   - Compare behavior durations against thresholds
   - Detect violations (e.g., "pacing > 30 min = unhealthy")
4. Return health status:
   - Status: 0 (unhealthy) or 1 (healthy)
   - Reason: Detailed explanation (e.g., "Pacing for 35 minutes exceeds 30 min threshold")
   - Details: Full analysis breakdown

**Key Methods Needed:**
```python
class BudgetLogic:
    def __init__(self, thresholds)
    def analyze_csv(csv_path, species) -> (status, reason, details)
    def analyze_dataframe(df, species) -> (status, reason, details)
    def analyze_consecutive_behaviors(df) -> List[segments]
    def check_thresholds(segments, species) -> (status, reason, details)
    def map_action_to_behavior(action_label) -> behavior_category
```

**Example Logic:**
```python
# If bear has been pacing for 35 minutes
if consecutive_pacing_duration > 30 minutes:
    return status=0, reason="Excessive pacing: 35 min (threshold: 30 min)"
```

**Why this is important:**
- This is the **unique feature** that makes the project special
- Without this, you just have action classification (not health monitoring)
- It's pure data processing/logic (no CV/AI needed)

---

## 🎯 Priority 2: Main Pipeline Orchestrator

**File:** `Main.py` (currently just `#main`)

**What it does:**
Connects all components together in the correct sequence. This is the "glue" that makes everything work.

**Your tasks:**
1. Create pipeline orchestrator class
2. Load configuration from `config.yaml`
3. Initialize all components:
   - Vision Engine (your friend will improve this)
   - Vision Classifier
   - Budget Logic (you'll build this)
   - Vet Reporter
4. Implement video processing flow:
   - Process single video or directory
   - Call components in sequence
   - Handle errors gracefully
   - Generate summary reports
5. Add command-line interface:
   ```bash
   python Main.py --video path/to/video.mp4 --species bear
   python Main.py  # Process all videos from config
   ```

**Key Features:**
- Error handling and logging
- Progress tracking
- Summary report generation
- Configuration management

**Why this is important:**
- Makes the project actually runnable end-to-end
- Your friends' components need this to work together
- Essential for testing and demonstration

---

## 🎯 Priority 3: Enhanced Configuration

**File:** `config.yaml` (currently very basic)

**What it does:**
Stores all settings, thresholds, and paths in one place.

**Your tasks:**
1. Add species-specific thresholds:
   ```yaml
   thresholds:
     bear:
       pacing: 30      # minutes
       sleeping: 480   # 8 hours
       resting: 360    # 6 hours
     gorilla:
       pacing: 45
       sleeping: 360
     rabbit:
       pacing: 20     # high stress indicator
       sleeping: 240
   ```
2. Add processing settings:
   - Vision processing interval (how often to classify)
   - Output paths (logs, reports)
   - Model settings
3. Add API keys section (for Gemini):
   ```yaml
   gemini:
     api_key: ""  # or use environment variable
   ```
4. Add behavior mappings (action labels → categories)

**Why this is important:**
- Makes the system configurable without code changes
- Allows easy threshold adjustments
- Your Budget Logic will read from this

---

## 🎯 Priority 4: Vision Classifier Enhancement

**File:** `src/vision_classifier.py` (currently has basic mapping only)

**What it does:**
Processes videos over time and generates timestamped CSV logs.

**Your tasks:**
1. Implement time-series processing:
   - Process video at regular intervals (every 1 second)
   - Extract frames around each time point
   - Classify each time segment
2. Generate timestamped CSV:
   - Columns: `timestamp, action_label, confidence, category`
   - One row per time point
   - This feeds into Budget Logic
3. Map actions to categories:
   - 400 Kinetics classes → 5 categories (Moving, Eating, Resting, Grooming, Interaction)
   - Use keyword matching for unknown actions

**Key Methods:**
```python
def process_video_over_time(video_path, output_csv) -> DataFrame
def map_action_to_category(action_label) -> category
```

**Why this is important:**
- Budget Logic needs timestamped data
- Creates the time-series data for analysis
- Bridges Vision Engine and Budget Logic

**Note:** You'll need to use the Vision Engine (your friend's component) but you're just calling it, not modifying it.

---

## 🎯 Priority 5: Vet Reporter Gemini Integration

**File:** `src/vet_reporter.py` (currently just saves to Excel)

**What it does:**
Generates readable veterinary reports using Google Gemini when unhealthy behavior is detected.

**Your tasks:**
1. Add Gemini API integration:
   - Install `google-generativeai` (already in requirements)
   - Initialize Gemini client
   - Handle API errors
2. Create knowledge base system:
   - Create `data/knowledge_base/` directory
   - Add animal care manuals (e.g., `bear_care.txt`, `rabbit_care.txt`)
   - Load relevant knowledge base for species
3. Implement report generation:
   - Take health status and reason from Budget Logic
   - Query knowledge base
   - Create prompt for Gemini
   - Generate readable veterinary report
   - Explain medical risks
   - Suggest enrichment activities

**Example Prompt:**
```
System: "You are an expert Zoo Veterinarian. Use the provided Knowledge Base 
to explain medical risks and suggest enrichment activities."

User: "Animal: Bear. Issue: Continuous Pacing for 35 minutes (exceeds 30 min threshold)."
```

**Why this is important:**
- Makes the system useful for zookeepers
- Provides actionable advice
- Adds AI-powered insights (but you're just integrating, not building the AI)

---

## 🎯 Priority 6: Data Processing Utilities

**Create new file:** `src/data_utils.py`

**What it does:**
Helper functions for data processing, validation, and file handling.

**Your tasks:**
1. CSV utilities:
   - Validate CSV format
   - Read/write timestamped data
   - Merge multiple CSV files
2. Data validation:
   - Check required columns
   - Validate timestamp format
   - Check data ranges
3. Logging utilities:
   - Centralized logging configuration
   - Progress tracking
   - Error reporting

**Why this is important:**
- Makes other components cleaner
- Reusable utilities
- Better error handling

---

## 🎯 Priority 7: Testing & Validation

**Create new file:** `test_budget_logic.py`

**Your tasks:**
1. Create test CSV files with known behaviors
2. Test Budget Logic with various scenarios:
   - Healthy patterns (switching behaviors)
   - Unhealthy patterns (stuck in one behavior)
   - Edge cases (empty data, invalid data)
3. Validate threshold logic
4. Test integration with other components

**Why this is important:**
- Ensures your code works correctly
- Helps debug issues
- Validates the logic

---

## Recommended Work Order

1. **Start with Budget Logic** (Priority 1)
   - This is the core feature
   - Can be developed and tested independently
   - Most important for the project

2. **Then Configuration** (Priority 3)
   - Needed by Budget Logic
   - Quick to implement
   - Enables threshold-based analysis

3. **Then Main Pipeline** (Priority 2)
   - Connects everything together
   - Makes the project runnable
   - Can test with mock data first

4. **Then Vision Classifier Enhancement** (Priority 4)
   - Generates data for Budget Logic
   - Uses Vision Engine (your friend's component)

5. **Then Vet Reporter** (Priority 5)
   - Adds Gemini integration
   - Enhances the output

6. **Finally Utilities & Testing** (Priorities 6-7)
   - Polish and validation
   - Makes everything robust

---

## What You DON'T Need to Work On

- ❌ **Vision Engine** - Your friend is handling CV/AI model
- ❌ **Dashboard/Frontend** - Your other friend is handling UI
- ❌ **Model training** - Using pre-trained models
- ❌ **Video processing libraries** - Already in requirements

---

## Getting Started

### Step 1: Budget Logic (Recommended First Task)

Create `src/budget_logic.py` with:

```python
"""
Budget Logic for ZooGuardian
Analyzes behavior patterns over time to determine health status.
"""

import pandas as pd
from typing import Dict, List, Tuple

class BudgetLogic:
    def __init__(self, thresholds: Dict = None):
        # Initialize with thresholds
        pass
    
    def analyze_csv(self, csv_path: str, species: str) -> Tuple[int, str, Dict]:
        # Read CSV, analyze, return (status, reason, details)
        pass
    
    # ... implement other methods
```

### Step 2: Test with Sample Data

Create a test CSV:
```csv
timestamp,action_label,confidence,category
0.0,walking the dog,0.72,Moving
1.0,walking the dog,0.68,Moving
...
300.0,walking the dog,0.70,Moving
```

Test your Budget Logic:
```python
logic = BudgetLogic()
status, reason, details = logic.analyze_csv("test.csv", "bear")
print(f"Status: {status}, Reason: {reason}")
```

---

## Summary

**Your main focus areas:**
1. ✅ **Budget Logic** - Core time-budget analysis (CRITICAL)
2. ✅ **Main Pipeline** - Orchestration (ESSENTIAL)
3. ✅ **Configuration** - Settings and thresholds (NEEDED)
4. ✅ **Vision Classifier Enhancement** - CSV generation (IMPORTANT)
5. ✅ **Vet Reporter** - Gemini integration (NICE TO HAVE)

**Start with Budget Logic** - it's the most important and can be developed independently!

