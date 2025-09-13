#!/usr/bin/env python3
"""
CSV Text Converter Tool - Main Entry Point
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from app.main import app
    
    print("Starting CSV Text Converter Tool...")
    print("Open your browser and go to: http://localhost:5001")
    
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
