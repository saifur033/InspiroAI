"""
InspiroAI - Streamlit Cloud Entry Point
This file runs the main application from production folder
"""
import sys
import os
import warnings

warnings.filterwarnings('ignore')

# Add production folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'production'))

# Set environment variables for models
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

try:
    # Import and run the main app
    from app import *
except Exception as e:
    import streamlit as st
    st.error(f"Error loading app: {str(e)}")
    st.info("Please check the deployment logs for details.")
