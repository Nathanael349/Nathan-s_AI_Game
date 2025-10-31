#!/bin/bash

# Setup script for The Evolving Kingdom

echo "🏰 Setting up The Evolving Kingdom..."

# Check Python version
python3 --version || { echo "Python 3 is required!"; exit 1; }

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your OpenAI API key!"
    echo ""
else
    echo "✅ .env file already exists"
fi

echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Run: python main.py"
