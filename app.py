#!/usr/bin/env python3
"""
app.py - Render-compatible Flask entry point
This file is used by Gunicorn on Render: gunicorn app:app
"""
import sys
import os

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

print(f"[APP] Project root: {PROJECT_ROOT}")
print(f"[APP] Python version: {sys.version}")

try:
    # Import and expose the Flask app from main.py
    print("[APP] Importing Flask app from main.py...")
    from main import app
    print(f"[APP] ✓ Flask app imported successfully: {app.name}")
    print(f"[APP] ✓ Ready for Gunicorn (gunicorn app:app)")
    
except Exception as e:
    print(f"[APP] ✗ FATAL ERROR during import: {e}")
    import traceback
    traceback.print_exc()
    raise

# This is what Gunicorn looks for: the 'app' variable
__all__ = ['app']
