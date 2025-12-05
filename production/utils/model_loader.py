"""
Model loading utilities - handles all model artifacts
"""
import os
import json
import joblib
import numpy as np
from pathlib import Path


class ModelRegistry:
    """Central registry for all trained models"""
    
    def __init__(self, models_dir="models"):
        self.models_dir = models_dir
        self.emotion_model = None
        self.emotion_le = None
        self.reach_model = None
        self.reach_ohe = None
        self.reach_scaler = None
        self.reach_threshold = 0.40
        self.status_xgb = None
        self.status_rf = None
        self.status_lgb = None
        self.status_threshold = 0.50
        
        # Feature metadata
        self.reach_meta = {}
        self.status_meta = {}
        self.status_style_features = []
        
    def load_emotion_model(self):
        """Load emotion detection pipeline (TF-IDF + LinearSVC)"""
        try:
            self.emotion_model = joblib.load(
                os.path.join(self.models_dir, "emotion_svm_pipeline.joblib")
            )
            self.emotion_le = joblib.load(
                os.path.join(self.models_dir, "emotion_label_encoder.joblib")
            )
            return True
        except Exception as e:
            print(f"Error loading emotion model: {e}")
            return False
    
    def load_reach_model(self):
        """Load reach prediction ensemble (VotingClassifier)"""
        try:
            self.reach_model = joblib.load(
                os.path.join(self.models_dir, "reach_voting.joblib")
            )
            self.reach_ohe = joblib.load(
                os.path.join(self.models_dir, "reach_ohe.joblib")
            )
            self.reach_scaler = joblib.load(
                os.path.join(self.models_dir, "reach_scaler.joblib")
            )
            
            # Load metadata
            with open(os.path.join(self.models_dir, "reach_meta.json"), "r") as f:
                self.reach_meta = json.load(f)
            
            # Load threshold
            thresh_data = joblib.load(
                os.path.join(self.models_dir, "reach_thresh.joblib")
            )
            self.reach_threshold = thresh_data.get("best_thresh", 0.40)
            
            return True
        except Exception as e:
            print(f"Error loading reach model: {e}")
            return False
    
    def load_status_model(self):
        """Load status (fake/real) detection ensemble"""
        try:
            self.status_xgb = joblib.load(
                os.path.join(self.models_dir, "status_xgb.joblib")
            )
            self.status_rf = joblib.load(
                os.path.join(self.models_dir, "status_rf.joblib")
            )
            self.status_lgb = joblib.load(
                os.path.join(self.models_dir, "status_lgb.joblib")
            )
            
            # Load metadata
            with open(os.path.join(self.models_dir, "status_meta.json"), "r") as f:
                meta = json.load(f)
                self.status_threshold = meta.get("best_threshold", 0.50)
            
            # Load style features
            self.status_style_features = joblib.load(
                os.path.join(self.models_dir, "status_style_features.joblib")
            )
            
            return True
        except Exception as e:
            print(f"Error loading status model: {e}")
            return False
    
    def load_all(self):
        """Load all models"""
        results = {
            "emotion": self.load_emotion_model(),
            "reach": self.load_reach_model(),
            "status": self.load_status_model(),
        }
        return results


def get_model_registry(models_dir="models"):
    """Factory function to get loaded model registry"""
    registry = ModelRegistry(models_dir)
    registry.load_all()
    return registry
