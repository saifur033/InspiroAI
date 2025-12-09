#!/usr/bin/env python
"""Debug status feature mismatch"""
import sys
import os
import joblib
import numpy as np

sys.path.insert(0, 'utils')

from utils.feature_engineering import engineer_status_features
from utils.model_loader import get_model_registry

print("Loading style features from model...")
registry = get_model_registry()
print(f"Style features from model: {registry.status_style_features}")
print(f"Number of features: {len(registry.status_style_features)}")

print("\nGenerating features for test caption...")
caption = "This is a test caption"
test_features = engineer_status_features(caption)
print(f"All features generated: {list(test_features.keys())}")
print(f"Number of features: {len(test_features)}")

print("\nFeatures from model in test caption:")
for feat in registry.status_style_features:
    val = test_features.get(feat, "MISSING")
    print(f"  {feat}: {val}")

print("\nMissing features:")
for feat in test_features.keys():
    if feat not in registry.status_style_features:
        print(f"  {feat}: {test_features[feat]}")
