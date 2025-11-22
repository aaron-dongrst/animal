"""
Backend API for FaunaVision
Accepts video and animal parameters, processes with vision model,
and uses OpenAI to determine health status.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import tempfile
import shutil
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Import vision components (placeholder for future model)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.vision_engine import VisionEngine

# OpenAI integration
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library not available. Install with: pip install openai")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configuration
UPLOAD_FOLDER = "temp"
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize vision engine (placeholder - will be replaced with chosen model)
vision_engine = None
try:
    vision_engine = VisionEngine()
    logger.info("Vision engine initialized successfully")
except Exception as e:
    logger.warning(f"Vision engine initialization failed: {e}. Will use placeholder.")


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_video_with_model(video_path: str) -> Dict:
    """
    Process video with vision model to detect activity and behavior length.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Dictionary with:
        - activity: str - Observed activity/behavior
        - length_seconds: float - Duration of behavior
        - is_repeating: bool - Whether behavior is repetitive
        - confidence: float - Confidence score
    """
    try:
        if vision_engine is None:
            # Placeholder response when model is not available
            logger.warning("Vision engine not available, using placeholder")
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            cap.release()
            
            return {
                "activity": "unknown",
                "length_seconds": duration,
                "is_repeating": False,
                "confidence": 0.0
            }
        
        # Use vision engine to classify video
        predictions = vision_engine.classify_video(video_path, top_k=1)
        top_prediction = predictions[0] if predictions else {"label": "unknown", "confidence": 0.0}
        
        # Get video duration
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        cap.release()
        
        # Simple heuristic for repeating behavior
        # If same activity detected throughout video, it's likely repeating
        is_repeating = duration > 30  # If behavior lasts more than 30 seconds, consider it repeating
        
        return {
            "activity": top_prediction.get("label", "unknown"),
            "length_seconds": duration,
            "is_repeating": is_repeating,
            "confidence": top_prediction.get("confidence", 0.0)
        }
        
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        return {
            "activity": "error",
            "length_seconds": 0.0,
            "is_repeating": False,
            "confidence": 0.0,
            "error": str(e)
        }


def determine_health_with_openai(
    species: str,
    age: Optional[str],
    diet: Optional[str],
    health_conditions: Optional[str],
    activity: str,
    length_seconds: float,
    is_repeating: bool
) -> Dict:
    """
    Use OpenAI API to determine if animal is healthy based on behavior and parameters.
    
    Args:
        species: Animal species
        age: Animal age
        diet: Animal diet
        health_conditions: Existing health conditions
        activity: Observed activity/behavior
        length_seconds: Duration of behavior in seconds
        is_repeating: Whether behavior is repetitive
        
    Returns:
        Dictionary with health assessment
    """
    if not OPENAI_AVAILABLE:
        logger.error("OpenAI not available")
        return {
            "is_healthy": None,
            "reasoning": "OpenAI API not configured",
            "recommendations": "Please configure OpenAI API key"
        }
    
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Build context for OpenAI
        length_minutes = length_seconds / 60.0
        repeating_status = "repetitive" if is_repeating else "non-repetitive"
        
        prompt = f"""You are an expert zoo veterinarian analyzing animal behavior and health.

Animal Information:
- Species: {species}
- Age: {age if age else 'Unknown'}
- Diet: {diet if diet else 'Unknown'}
- Existing Health Conditions: {health_conditions if health_conditions else 'None reported'}

Observed Behavior:
- Activity: {activity}
- Duration: {length_minutes:.2f} minutes ({length_seconds:.2f} seconds)
- Pattern: {repeating_status}

Based on this information, determine if the animal is healthy or unhealthy.

Consider:
1. Is the observed behavior normal for this species?
2. Is the duration of the behavior concerning?
3. Is repetitive behavior a sign of stress or health issues?
4. How do the animal's age, diet, and existing conditions affect the assessment?

Respond in JSON format with:
{{
    "is_healthy": true or false,
    "reasoning": "Detailed explanation of your assessment",
    "recommendations": "Specific recommendations for the animal's care"
}}"""

        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo" for faster/cheaper
            messages=[
                {"role": "system", "content": "You are an expert zoo veterinarian. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        # Parse response
        response_text = response.choices[0].message.content.strip()
        
        # Try to extract JSON from response
        import json
        import re
        
        # Remove markdown code blocks if present
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        response_text = response_text.strip()
        
        try:
            health_assessment = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            logger.warning("Failed to parse OpenAI response as JSON, using fallback")
            health_assessment = {
                "is_healthy": None,
                "reasoning": response_text,
                "recommendations": "Please review the reasoning above"
            }
        
        return health_assessment
        
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return {
            "is_healthy": None,
            "reasoning": f"Error assessing health: {str(e)}",
            "recommendations": "Please check API configuration"
        }


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "vision_engine": vision_engine is not None,
        "openai_available": OPENAI_AVAILABLE
    })


@app.route("/analyze", methods=["POST"])
def analyze_animal():
    """
    Main endpoint to analyze animal health from video and parameters.
    
    Expected request:
    - Form data with 'video' file
    - JSON or form data with parameters:
      - species: str (required)
      - age: str (optional)
      - diet: str (optional)
      - health_conditions: str (optional)
    
    Returns:
    {
        "species": str,
        "behavior_observed": str,
        "length_seconds": float,
        "is_healthy": bool,
        "reasoning": str,
        "recommendations": str,
        "confidence": float
    }
    """
    # Check for video file
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400
    
    video_file = request.files["video"]
    
    if video_file.filename == "":
        return jsonify({"error": "No video file selected"}), 400
    
    if not allowed_file(video_file.filename):
        return jsonify({"error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}), 400
    
    # Get parameters
    species = request.form.get("species") or request.json.get("species") if request.is_json else None
    if not species:
        return jsonify({"error": "Species parameter is required"}), 400
    
    age = request.form.get("age") or (request.json.get("age") if request.is_json else None)
    diet = request.form.get("diet") or (request.json.get("diet") if request.is_json else None)
    health_conditions = request.form.get("health_conditions") or (request.json.get("health_conditions") if request.is_json else None)
    
    # Save video to temporary file
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, video_file.filename)
    
    try:
        video_file.save(video_path)
        
        # Check file size
        file_size = os.path.getsize(video_path)
        if file_size > MAX_VIDEO_SIZE:
            return jsonify({"error": f"Video file too large. Max size: {MAX_VIDEO_SIZE / 1024 / 1024}MB"}), 400
        
        logger.info(f"Processing video: {video_file.filename} for species: {species}")
        
        # Step 1: Process video with vision model
        logger.info("Step 1: Processing video with vision model...")
        vision_result = process_video_with_model(video_path)
        
        if "error" in vision_result:
            return jsonify({"error": f"Video processing failed: {vision_result['error']}"}), 500
        
        activity = vision_result["activity"]
        length_seconds = vision_result["length_seconds"]
        is_repeating = vision_result["is_repeating"]
        confidence = vision_result["confidence"]
        
        logger.info(f"Detected activity: {activity}, Duration: {length_seconds}s, Repeating: {is_repeating}")
        
        # Step 2: Determine health status with OpenAI
        logger.info("Step 2: Assessing health with OpenAI...")
        health_assessment = determine_health_with_openai(
            species=species,
            age=age,
            diet=diet,
            health_conditions=health_conditions,
            activity=activity,
            length_seconds=length_seconds,
            is_repeating=is_repeating
        )
        
        # Step 3: Build response
        response = {
            "species": species,
            "behavior_observed": activity,
            "length_seconds": round(length_seconds, 2),
            "length_minutes": round(length_seconds / 60.0, 2),
            "is_repeating": is_repeating,
            "is_healthy": health_assessment.get("is_healthy"),
            "reasoning": health_assessment.get("reasoning", ""),
            "recommendations": health_assessment.get("recommendations", ""),
            "confidence": round(confidence, 4)
        }
        
        logger.info(f"Analysis complete. Health status: {response['is_healthy']}")
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {e}", exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
        
    finally:
        # Clean up temporary files
        try:
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except Exception as e:
            logger.warning(f"Error cleaning up temp files: {e}")


@app.route("/analyze/batch", methods=["POST"])
def analyze_batch():
    """
    Analyze multiple videos in batch.
    
    Expected request:
    - JSON with array of analysis requests
    - Each request should have video file path and parameters
    
    Note: This is a placeholder for future batch processing.
    """
    return jsonify({"error": "Batch processing not yet implemented"}), 501


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY not set. Health assessment will not work.")
        logger.warning("Set it with: export OPENAI_API_KEY='your-key-here'")
    
    # Run Flask app
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting FaunaVision backend on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host="0.0.0.0", port=port, debug=debug)
