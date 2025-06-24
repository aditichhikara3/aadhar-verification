#!/bin/bash

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ensure logs folder exists
mkdir -p logs

# Launch app
python app.py
