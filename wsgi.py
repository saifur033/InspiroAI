#!/usr/bin/env python3
"""
WSGI entry point for Gunicorn (Render deployment)
This module is loaded by Gunicorn: gunicorn wsgi:app
"""
import sys
import os

# Ensure the project root is in Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import the Flask app from main.py
# This must work or deployment will fail
try:
    from main import app
    print(f"[OK] Flask app successfully imported from main.py")
    print(f"[OK] App name: {app.name}")
    print(f"[OK] WSGI ready for Gunicorn")
except Exception as e:
    print(f"[FATAL] Failed to import app: {e}")
    import traceback
    traceback.print_exc()
    raise

# Expose app for Gunicorn
__all__ = ['app']



