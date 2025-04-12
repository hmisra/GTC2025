#!/bin/bash
# GTC Session Extractor - Setup and Run Script

# Exit on error
set -e

echo "NVIDIA GTC Session Extractor - Setup and Run Script"
echo "------------------------------------------------"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "Using existing virtual environment."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers (Chromium)..."
python -m playwright install chromium

# Check if HTML file exists
if [ ! -f "Attendee Portal - Session Catalog.html" ]; then
    echo "Error: 'Attendee Portal - Session Catalog.html' not found."
    echo "Please place the HTML file in the same directory as this script."
    exit 1
fi

# Run the extraction script
echo "Running extraction script..."
python extract_sessions.py

echo "------------------------------------------------"
echo "Process complete! The extracted data is saved in:"
echo "- CSV format: 'gtc_sessions_extracted.csv'"
echo "- Markdown table: 'gtc_sessions_table.md'"
echo ""
echo "To view the CSV data: head -n 10 gtc_sessions_extracted.csv"
echo "To view the Markdown table: head -n 10 gtc_sessions_table.md" 