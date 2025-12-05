"""
InspiroAI - Streamlit Cloud Entry Point
This file redirects to the main application in production folder
"""
import sys
import os

# Add production folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'production'))

# Import and run the main app
from app import *
