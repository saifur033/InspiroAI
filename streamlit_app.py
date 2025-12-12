"""
InspiroAI - Streamlit Cloud Entry Point
Wrapper that runs the main app from production folder
"""

import sys
import os

# Add production folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'production'))

# Import and run the app
from app import *
