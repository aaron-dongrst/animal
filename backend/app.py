from flask import Flask, request, jsonify
from src.vision_engine import VisionEngine
from src.vision_classifier import VisionClassifier
import openai
import os

app = Flask(__name__)

# Initialize components
engine = VisionEngine()
classifier = VisionClassifier()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/classify", methods=["POST"])
def classify_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files["video"]
    video_path = f"temp/{video.filename}"
    video.save(video_path)

    try:
        # Classify video
        predictions = engine.classify_video(video_path, top_k=1)
        top_label = predictions[0]["label"]
        health_status = classifier.classify_action(top_label)

        # Get recommendations from LLM
        prompt = f"The animal is performing the action '{top_label}', which is classified as '{health_status}'. What steps should be taken to maintain or improve the animal's health?"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        recommendations = response.choices[0].text.strip()

        return jsonify({
            "action": top_label,
            "health_status": health_status,
            "recommendations": recommendations
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
