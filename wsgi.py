#!/usr/bin/env python3
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import Flask app from main.py
    from main import app
except ImportError as e:
    print(f"ERROR: Could not import app from main.py: {e}")
    raise


