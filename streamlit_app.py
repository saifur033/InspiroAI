"""
InspiroAI - Context-Aware Facebook Caption Optimization System
Streamlit Cloud Entry Point
"""
import sys
import os
import warnings

warnings.filterwarnings('ignore')

# Add production folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'production'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'production', 'utils'))

# Set environment variables
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

try:
    # Now import the main app
    exec(open(os.path.join(os.path.dirname(__file__), 'production', 'app.py')).read())
except Exception as e:
    import streamlit as st
    st.error(f"Error loading app: {str(e)}")
    st.info("Check GitHub for latest version: https://github.com/saifur033/InspiroAI")
