#!/usr/bin/env python3
"""
Debug script to check if InspiroAI app can load models properly
Run this on Streamlit Cloud to diagnose issues
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("INSPIROAI - MODEL LOADING DIAGNOSTIC")
print("=" * 60)

# Check working directory
print(f"\n1. Working Directory: {os.getcwd()}")
print(f"   Python Path: {sys.executable}")

# Check if production folder exists
print(f"\n2. Checking folder structure:")
print(f"   Current dir contents: {os.listdir('.')}")

if os.path.exists('production'):
    print(f"   Production dir exists: YES")
    print(f"   Production contents: {os.listdir('production')}")
    
    if os.path.exists('production/models'):
        print(f"   Models dir exists: YES")
        models = os.listdir('production/models')
        print(f"   Models count: {len(models)}")
        print(f"   Models: {models}")
    else:
        print(f"   Models dir exists: NO (ERROR!)")
else:
    print(f"   Production dir exists: NO (ERROR!)")

# Check if app.py can import utils
print(f"\n3. Testing imports:")
try:
    sys.path.insert(0, 'production')
    from utils.model_loader import get_model_registry
    print(f"   ✓ model_loader imported successfully")
except Exception as e:
    print(f"   ✗ model_loader import FAILED: {e}")

try:
    from utils.inference import StatusPredictor, EmotionPredictor, ReachPredictor
    print(f"   ✓ inference imported successfully")
except Exception as e:
    print(f"   ✗ inference import FAILED: {e}")

try:
    from sentence_transformers import SentenceTransformer
    print(f"   ✓ sentence_transformers available")
except Exception as e:
    print(f"   ✗ sentence_transformers NOT available: {e}")

# Try loading models
print(f"\n4. Testing model loading:")
try:
    from utils.model_loader import get_model_registry
    registry = get_model_registry()
    print(f"   Status RF loaded: {registry.status_rf is not None}")
    print(f"   Reach model loaded: {registry.reach_model is not None}")
    print(f"   ✓ Models loaded successfully!")
except Exception as e:
    print(f"   ✗ Model loading FAILED: {e}")
    import traceback
    traceback.print_exc()

# Try embedding model
print(f"\n5. Testing embedder:")
try:
    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"   ✓ Embedder loaded successfully!")
except Exception as e:
    print(f"   ✗ Embedder loading FAILED: {e}")

# Try emotion prediction
print(f"\n6. Testing emotion prediction:")
try:
    from utils.inference import EmotionPredictor
    result = EmotionPredictor.predict("I love this!")
    if 'error' in result:
        print(f"   ✗ Emotion prediction returned error: {result['error']}")
    else:
        print(f"   ✓ Emotion prediction works: {result['emotion']}")
except Exception as e:
    print(f"   ✗ Emotion prediction FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
