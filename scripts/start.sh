#!/bin/bash

echo "🚀 Starting Task Manager API Development Server..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source conda activate project1_env
    echo "✅ Virtual environment activated"
fi

# Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


