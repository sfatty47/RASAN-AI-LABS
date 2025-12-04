#!/bin/bash
# Script to start the backend server with proper virtual environment

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if activation worked
if [ "$VIRTUAL_ENV" != "" ]; then
    echo "✅ Virtual environment activated"
    echo "Python: $(python --version)"
    echo ""
    echo "Starting backend server..."
    echo "Press Ctrl+C to stop"
    echo ""
    uvicorn app.main:app --reload
else
    echo "❌ Failed to activate virtual environment"
    echo "Please run: python3.11 -m venv venv"
    exit 1
fi

