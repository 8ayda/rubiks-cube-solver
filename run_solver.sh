#!/bin/bash

# Rubik's Cube Solver - Launch Script
# ===================================

echo "🎲 Rubik's Cube Solver"
echo "====================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found."
    echo "Please run the setup first or install dependencies manually."
    exit 1
fi

# Activate virtual environment and run
echo "🚀 Starting Rubik's Cube Solver..."
echo "Make sure your webcam is connected and working!"
echo ""

.venv/bin/python main.py
