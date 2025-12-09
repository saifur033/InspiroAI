#!/usr/bin/env python
"""Test Status Predictor with various captions"""
import sys
import os
sys.path.insert(0, 'utils')

from utils.model_loader import get_model_registry
from utils.inference import StatusPredictor
from sentence_transformers import SentenceTransformer

print("Loading models...")
registry = get_model_registry()
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Test captions
test_cases = [
    ("This product is amazing! Buy now and get 50% discount!", "Should be FAKE"),
    ("Just a regular day at the office, had coffee and worked.", "Should be REAL"),
    ("FREE MONEY!!! Click here now!!!!", "Should be FAKE"),
    ("Today I went to the market and bought some vegetables.", "Should be REAL"),
    ("Congratulations! You won a prize! Claim now!", "Should be FAKE"),
    ("Having a nice time with family and friends.", "Should be REAL"),
]

print("\n" + "="*70)
print("TESTING STATUS PREDICTOR")
print("="*70)

for caption, expected in test_cases:
    result = StatusPredictor.predict(caption, embedder=embedder, model_registry=registry)
    
    if "error" in result:
        print(f"\n❌ ERROR: {result['error']}")
    else:
        suspicion = result['suspicion_score']
        status = result['status']
        print(f"\nCaption: {caption[:50]}...")
        print(f"Expected: {expected}")
        print(f"Result: {status} (suspicion_score: {suspicion:.4f})")
        print(f"Confidence: {result['confidence']:.4f}")
        
        # Check if prediction matches expected
        if "FAKE" in expected and "Fake" in status:
            print("✓ CORRECT")
        elif "REAL" in expected and "Real" in status:
            print("✓ CORRECT")
        else:
            print("✗ WRONG")

print("\n" + "="*70)
