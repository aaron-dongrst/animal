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
    echo "OPENAI_API_KEY=your-key-here" > .env
    echo "PORT=5000" >> .env
    echo "FLASK_DEBUG=True" >> .env
    echo ""
    echo "Please edit .env file and add your OpenAI API key"
    echo ""
fi

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs)
    fi
fi

if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your-key-here" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set"
    echo "Health assessment will not work without OpenAI API key"
    echo ""
fi

# Create temp directory if it doesn't exist
mkdir -p temp

# Start the server
echo "Starting server..."
echo "API will be available at: http://localhost:${PORT:-5000}"
echo "Health check: http://localhost:${PORT:-5000}/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python app.py

