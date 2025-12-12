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
        # Fix path for Streamlit Cloud - use absolute path if relative path doesn't work
        if not os.path.isabs(models_dir):
            # Try relative path first
            if not os.path.exists(models_dir):
                # Try from production folder
                alt_dir = os.path.join(os.path.dirname(__file__), '..', models_dir)
                if os.path.exists(alt_dir):
                    models_dir = alt_dir
                else:
                    # Last resort: assume we're in production folder
                    models_dir = os.path.join(os.path.dirname(__file__), 'models')
        
        self.models_dir = models_dir
        print(f"[INFO] Models directory set to: {self.models_dir}")
        print(f"[INFO] Models directory exists: {os.path.exists(self.models_dir)}")
        
        self.emotion_model = None
        self.emotion_le = None
        self.reach_model = None
        self.reach_ohe = None
        self.reach_scaler = None
        self.reach_threshold = 0.40
        self.status_xgb = None
        self.status_rf = None
        self.status_lgb = None
        self.status_threshold = 0.55
        
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
            status_xgb_path = os.path.join(self.models_dir, "status_xgb.joblib")
            status_rf_path = os.path.join(self.models_dir, "status_rf.joblib")
            status_lgb_path = os.path.join(self.models_dir, "status_lgb.joblib")
            status_meta_path = os.path.join(self.models_dir, "status_meta.json")
            status_style_path = os.path.join(self.models_dir, "status_style_features.joblib")
            
            print(f"[DEBUG] Loading status_xgb from: {status_xgb_path} (exists: {os.path.exists(status_xgb_path)})")
            print(f"[DEBUG] Loading status_rf from: {status_rf_path} (exists: {os.path.exists(status_rf_path)})")
            print(f"[DEBUG] Loading status_lgb from: {status_lgb_path} (exists: {os.path.exists(status_lgb_path)})")
            
            self.status_xgb = joblib.load(status_xgb_path)
            self.status_rf = joblib.load(status_rf_path)
            self.status_lgb = joblib.load(status_lgb_path)
            
            # Load metadata
            with open(status_meta_path, "r") as f:
                meta = json.load(f)
                self.status_threshold = meta.get("best_threshold", 0.55)
            
            # Load style features
            self.status_style_features = joblib.load(status_style_path)
            
            print(f"[OK] Status models loaded successfully!")
            return True
        except Exception as e:
            print(f"[ERROR] Error loading status model: {e}")
            import traceback
            traceback.print_exc()
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
