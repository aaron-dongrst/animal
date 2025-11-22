import os
from dotenv import load_dotenv

import google.generativeai as genai

# Load .env if present (create a .env with GENAI_API_KEY=your_key and add .env to .gitignore)
load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("GENAI_API_KEY not set. Set it in the environment or in a .env file.")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

with open("data/raw_videos/Not Healthy/BearWalking.mp4", "rb") as f:
    video_bytes = f.read()

prompt = """
You are a wildlife behavior expert.
Describe everything happening in this video.
Focus on movement patterns, pacing, resting,
and signs of stress.
"""

response = model.generate_content(
    [prompt, {"mime_type": "video/mp4", "data": video_bytes}]
)

print(response.text)
