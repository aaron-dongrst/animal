#!/bin/bash
# Startup script for FaunaVision Backend API

echo "=========================================="
echo "FaunaVision Backend API"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env template..."
    echo "GEMINI_API_KEY=your-key-here" > .env
    echo "PORT=5001" >> .env
    echo "FLASK_DEBUG=False" >> .env
    echo "YOLO_MODEL_PATH=models/best.pt" >> .env
    echo "USE_GEMINI=true" >> .env
    echo ""
    echo "Please edit .env file and add your Gemini API key"
    echo ""
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if Gemini API key is set
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your-key-here" ]; then
    echo "⚠️  Warning: GEMINI_API_KEY not set"
    echo "Health assessment will not work without Gemini API key"
    echo ""
fi

# Create temp directory if it doesn't exist
mkdir -p temp

# Start the server
echo "Starting server..."
echo "API will be available at: http://localhost:${PORT:-5001}"
echo "Health check: http://localhost:${PORT:-5001}/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python3 app.py

