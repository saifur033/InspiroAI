#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI Entry Point for Gunicorn
Handles environment setup and app initialization
"""

import os
import sys
import logging

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Import Flask app
    from main import app
    logger.info("[OK] Flask app imported successfully from main.py")
except Exception as e:
    logger.error(f"[ERROR] Failed to import Flask app: {str(e)}", exc_info=True)
    raise

# Gunicorn will use this 'app' variable
if __name__ == "__main__":
    app.run()
