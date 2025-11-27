#!/usr/bin/env python3
"""
WSGI entry point for Gunicorn (Render deployment)
Handles app initialization with proper error handling.
"""
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the project root is in Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

logger.info(f"[WSGI] Project root: {PROJECT_ROOT}")
logger.info(f"[WSGI] Python version: {sys.version}")
logger.info(f"[WSGI] Loading Flask app from main.py...")

# Import the Flask app from main.py
try:
    from main import app
    logger.info(f"[WSGI] ✓ Flask app imported successfully")
    logger.info(f"[WSGI] ✓ App name: {app.name}")
    logger.info(f"[WSGI] ✓ WSGI entry point ready for Gunicorn")
    
except ModuleNotFoundError as e:
    logger.error(f"[WSGI] ModuleNotFoundError: {e}")
    logger.error(f"[WSGI] Project root not found or main.py import failed")
    logger.error(f"[WSGI] sys.path: {sys.path}")
    raise
    
except ImportError as e:
    logger.error(f"[WSGI] ImportError: {e}")
    logger.error(f"[WSGI] Dependencies missing or broken")
    import traceback
    traceback.print_exc()
    raise
    
except Exception as e:
    logger.error(f"[WSGI] Unexpected error during app import: {e}")
    logger.error(f"[WSGI] Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    raise

# Expose app for Gunicorn
__all__ = ['app']




