#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI Entry Point for Gunicorn
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app from main
from main import app

# Gunicorn will use this 'app' variable

