#!/bin/bash

# Rubik's Cube Solver - Setup Script
# ==================================

echo "🎲 RUBIK'S CUBE SOLVER - SETUP"
echo "=============================="
echo ""

# Check Python version
python3 --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Run tests
echo ""
echo "🧪 Running tests..."
python test_solver.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SETUP COMPLETED SUCCESSFULLY!"
    echo ""
    echo "You can now run the application in these ways:"
    echo "1. ./run_solver.sh           (Recommended)"
    echo "2. python main.py            (Manual)"
    echo "3. python demo.py            (Demo without webcam)"
    echo "4. python test_solver.py     (Run tests)"
    echo ""
    echo "Make sure your webcam is connected before running!"
else
    echo "❌ Setup completed but tests failed. Check the installation."
fi
