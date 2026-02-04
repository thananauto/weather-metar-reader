#!/bin/bash

# METAR Weather Reader - Run Script

echo "🌤️  Starting METAR Weather Reader..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the Flask app
echo ""
echo "✈️  METAR Weather Reader is starting..."
echo "🌐 Open your browser to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd src/metar_app
python app.py
