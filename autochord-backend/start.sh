#!/bin/bash

echo "🎸 Starting Chord Extractor Backend..."
echo "=================================="

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate venv
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Start the server
echo "🚀 Starting Flask server on http://localhost:5000"
echo "=================================="
python app.py
