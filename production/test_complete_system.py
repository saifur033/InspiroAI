#!/usr/bin/env python
"""Complete system test before running"""
import sys
import os

sys.path.insert(0, 'utils')

print("=" * 70)
print("INSPIROAI - COMPLETE SYSTEM TEST")
print("=" * 70)

# Test 1: Model Loading
print("\n[1/4] Testing Model Loading...")
try:
    from utils.model_loader import get_model_registry
    registry = get_model_registry()
    assert registry.status_rf is not None, "status_rf not loaded"
    assert registry.reach_model is not None, "reach_model not loaded"
    print("  [OK] All models loaded successfully")
except Exception as e:
    print(f"  [FAILED] {e}")
    sys.exit(1)

# Test 2: Embedder Loading
print("\n[2/4] Testing Embedder Loading...")
try:
    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    print("  [OK] Embedder loaded successfully")
except Exception as e:
    print(f"  [FAILED] {e}")
    sys.exit(1)

# Test 3: Status Prediction
print("\n[3/4] Testing Status Prediction...")
try:
    from utils.inference import StatusPredictor
    test_caption = "This is a test caption"
    result = StatusPredictor.predict(test_caption, embedder=embedder, model_registry=registry)
    assert "error" not in result, f"Prediction error: {result.get('error')}"
    assert "status" in result, "No status in result"
    assert "suspicion_score" in result, "No suspicion_score in result"
    print(f"  [OK] Status: {result['status']}, Score: {result['suspicion_score']:.2f}")
except Exception as e:
    print(f"  [FAILED] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Emotion Prediction
print("\n[4/4] Testing Emotion Prediction...")
try:
    from utils.inference import EmotionPredictor
    result = EmotionPredictor.predict(test_caption)
    assert "error" not in result, f"Prediction error: {result.get('error')}"
    assert "emotion" in result, "No emotion in result"
    assert "all_emotions" in result, "No all_emotions in result"
    print(f"  [OK] Emotion: {result['emotion']}")
    print(f"       All emotions: {result['all_emotions']}")
except Exception as e:
    print(f"  [FAILED] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("SUCCESS! All tests passed. You can now run: streamlit run app.py")
print("=" * 70)
