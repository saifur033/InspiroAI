#!/usr/bin/env python3
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Lazy import to handle environment issues
def create_app():
    from main import app
    return app

# Create app instance
app = create_app()


