# FaunaVision Backend API

Backend API that accepts video and animal parameters, processes with vision model, and uses OpenAI to determine health status.

## Features

- ✅ Accepts video file uploads
- ✅ Accepts animal parameters (species, age, diet, health conditions)
- ✅ Processes video with vision model (currently using VisionEngine, placeholder for future model)
- ✅ Tracks behavior length and repetition
- ✅ Uses OpenAI API to determine health status
- ✅ Returns comprehensive health assessment

## Setup

### 1. Install Dependencies

```bash
pip install -r ../requirements.txt
```

### 2. Set Environment Variables

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
export PORT=5000  # Optional, defaults to 5000
export FLASK_DEBUG=True  # Optional, for development
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-openai-api-key-here
PORT=5000
FLASK_DEBUG=True
```

### 3. Run the Server

```bash
python backend/app.py
```

The server will start on `http://0.0.0.0:5000`

## API Endpoints

### POST `/analyze`

Main endpoint to analyze animal health from video and parameters.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data` or `application/json`
- Body:
  - `video`: Video file (required)
  - `species`: Animal species (required)
  - `age`: Animal age (optional)
  - `diet`: Animal diet (optional)
  - `health_conditions`: Existing health conditions (optional)

**Example using curl:**
```bash
curl -X POST http://localhost:5000/analyze \
  -F "video=@path/to/video.mp4" \
  -F "species=bear" \
  -F "age=5 years" \
  -F "diet=omnivore" \
  -F "health_conditions=none"
```

**Example using JavaScript (fetch):**
```javascript
const formData = new FormData();
formData.append('video', videoFile);
formData.append('species', 'bear');
formData.append('age', '5 years');
formData.append('diet', 'omnivore');
formData.append('health_conditions', 'none');

const response = await fetch('http://localhost:5000/analyze', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

**Response:**
```json
{
  "species": "bear",
  "behavior_observed": "walking the dog",
  "length_seconds": 93.09,
  "length_minutes": 1.55,
  "is_repeating": true,
  "is_healthy": false,
  "reasoning": "The bear has been pacing repetitively for over 1.5 minutes, which is a sign of stress or zoochosis. Combined with the repetitive pattern, this indicates potential welfare concerns.",
  "recommendations": "1. Provide environmental enrichment (puzzle feeders, new scents, climbing structures). 2. Increase enclosure size if possible. 3. Monitor for other stress behaviors. 4. Consider veterinary consultation if behavior persists.",
  "confidence": 0.7172
}
```

### GET `/health`

Health check endpoint to verify server status.

**Response:**
```json
{
  "status": "healthy",
  "vision_engine": true,
  "openai_available": true
}
```

## Response Fields

- `species`: Animal species (from input)
- `behavior_observed`: Activity/behavior detected by vision model
- `length_seconds`: Duration of behavior in seconds
- `length_minutes`: Duration of behavior in minutes
- `is_repeating`: Whether behavior is repetitive (true if > 30 seconds)
- `is_healthy`: Health status determined by OpenAI (true/false/null)
- `reasoning`: Detailed explanation of health assessment
- `recommendations`: Specific care recommendations
- `confidence`: Confidence score from vision model (0.0-1.0)

## Vision Model Integration

Currently uses `VisionEngine` from `src/vision_engine.py` as a placeholder. 

**To integrate a different model:**

1. Replace the `process_video_with_model()` function in `backend/app.py`
2. Ensure it returns a dictionary with:
   - `activity`: str - Observed activity/behavior
   - `length_seconds`: float - Duration
   - `is_repeating`: bool - Whether repetitive
   - `confidence`: float - Confidence score

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing parameters, invalid file)
- `500`: Internal server error
- `501`: Not implemented (batch endpoint)

Error responses include a JSON object with an `error` field:
```json
{
  "error": "No video file provided"
}
```

## File Upload Limits

- Maximum file size: 100MB
- Allowed formats: mp4, avi, mov, mkv

## CORS

CORS is enabled to allow frontend requests from different origins.

## Logging

The backend logs all requests and processing steps. Check console output for debugging.

## Future Enhancements

- [ ] Batch processing endpoint
- [ ] Video preprocessing and optimization
- [ ] Caching for repeated analyses
- [ ] Support for live video streams
- [ ] Integration with specific animal behavior models
- [ ] Database storage for analysis history

