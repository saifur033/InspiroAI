#!/usr/bin/env python
"""Test script to debug model loading issues"""
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

print("=" * 60)
print("MODEL LOADING DEBUG TEST")
print("=" * 60)

print("\n1️⃣ Testing model registry load...")
try:
    from utils.model_loader import get_model_registry
    registry = get_model_registry()
    print("✓ Registry loaded successfully")
    print(f"  - status_xgb: {registry.status_xgb is not None}")
    print(f"  - status_rf: {registry.status_rf is not None}")
    print(f"  - status_lgb: {registry.status_lgb is not None}")
    print(f"  - status_style_features: {len(registry.status_style_features) if registry.status_style_features else 0} features")
except Exception as e:
    import traceback
    print(f"✗ FAILED: {e}")
    print(traceback.format_exc())
    sys.exit(1)

print("\n2️⃣ Testing embedder load...")
try:
    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Embedder loaded successfully")
except Exception as e:
    import traceback
    print(f"✗ FAILED: {e}")
    print(traceback.format_exc())
    sys.exit(1)

print("\n3️⃣ Testing StatusPredictor...")
try:
    from utils.inference import StatusPredictor
    test_caption = "Great product! Highly recommended for everyone."
    result = StatusPredictor.predict(test_caption, embedder=embedder, model_registry=registry)
    print(f"✓ Prediction successful: {result}")
except Exception as e:
    import traceback
    print(f"✗ FAILED: {e}")
    print(traceback.format_exc())
    sys.exit(1)

print("\n4️⃣ Testing EmotionPredictor...")
try:
    from utils.inference import EmotionPredictor
    result = EmotionPredictor.predict(test_caption)
    print(f"✓ Prediction successful: {result}")
except Exception as e:
    import traceback
    print(f"✗ FAILED: {e}")
    print(traceback.format_exc())
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
