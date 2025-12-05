"""
Model inference functions - unified prediction interface
"""
import numpy as np
from scipy import sparse
from utils.feature_engineering import engineer_reach_features, engineer_status_features


class EmotionPredictor:
    """Emotion detection predictions - uses pretrained transformer for all 6 emotions"""
    
    @staticmethod
    def predict(text, model_registry=None):
        """
        Predict emotion for given text
        Uses pretrained HuggingFace DistilRoBERTa model for comprehensive emotion detection
        Supports: anger, fear, joy, neutral, sadness, surprise
        """
        try:
            from transformers import pipeline as hf_pipeline
            
            # Initialize emotion pipeline (will download model on first use)
            # top_k=None to get all 6 emotion probabilities
            emotion_pipe = hf_pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=None,  # Get all emotion scores
                device=-1  # CPU (use 0 for GPU if available)
            )
            
            # Get predictions for all emotions
            results = emotion_pipe(text[:512])[0]  # Get first (and only) result
            
            # Sort by score descending
            results = sorted(results, key=lambda x: x['score'], reverse=True)
            
            # Extract top emotion
            top_emotion = results[0]['label']
            top_score = float(results[0]['score'])
            
            # Get all emotion probabilities
            emotion_probs = {}
            for r in results:
                emotion_probs[r['label']] = float(r['score'])
            
            return {
                "emotion": top_emotion,
                "confidence": top_score,
                "all_emotions": emotion_probs
            }
        except Exception as e:
            # Fallback: if transformer unavailable, use simple rule-based
            return {
                "emotion": "neutral",
                "confidence": 0.5,
                "all_emotions": {"anger": 0.1, "fear": 0.1, "joy": 0.2, "neutral": 0.4, "sadness": 0.1, "surprise": 0.1},
                "note": f"Using fallback (error: {str(e)})"
            }


class ReachPredictor:
    """Reach prediction"""
    
    @staticmethod
    def predict(caption, embedder=None, model_registry=None):
        """
        Predict reach for given caption
        Simplified version - uses current datetime
        """
        if model_registry is None or model_registry.reach_model is None or embedder is None:
            return {"error": "Reach model or embedder not loaded"}
        
        try:
            from datetime import datetime as dt
            
            # Engineer features with current timestamp
            reach_features = engineer_reach_features(caption, timestamp=dt.now(), category="", language="")
            
            # Get text embedding
            caption_emb = embedder.encode([caption], convert_to_numpy=True)
            caption_emb_sparse = sparse.csr_matrix(caption_emb)
            
            # Get numeric features in correct order
            num_cols = model_registry.reach_meta.get("num_cols", [
                "char_count", "word_count", "avg_word_len", "emoji_count",
                "has_hashtag", "fk_grade", "hour", "dow", "is_weekend",
                "hour_sin", "hour_cos", "dow_sin", "dow_cos"
            ])
            
            num_values = np.array([[reach_features.get(col, 0) for col in num_cols]])
            num_scaled = model_registry.reach_scaler.transform(num_values)
            num_sparse = sparse.csr_matrix(num_scaled)
            
            # Empty categorical
            cat_sparse = sparse.csr_matrix((1, 0))
            
            # Combine
            X = sparse.hstack([caption_emb_sparse, cat_sparse, num_sparse], format="csr")
            
            # Predict
            if hasattr(model_registry.reach_model, "predict_proba"):
                prob = float(model_registry.reach_model.predict_proba(X)[:, 1][0])
            else:
                prob = float(model_registry.reach_model.predict(X)[0])
            
            label = "High Reach" if prob >= model_registry.reach_threshold else "Low Reach"
            
            return {
                "probability": prob,
                "prediction": label,
                "threshold": model_registry.reach_threshold,
                "features": reach_features
            }
        except Exception as e:
            return {"error": f"Reach prediction failed: {str(e)}"}


class StatusPredictor:
    """Fake/Real status detection"""
    
    @staticmethod
    def predict(caption, embedder=None, model_registry=None):
        """
        Predict if status is fake/spam or real
        """
        if model_registry is None or embedder is None or model_registry.status_xgb is None:
            return {"error": "Status model or embedder not loaded"}
        
        try:
            # Get text embedding
            caption_emb = embedder.encode([caption], convert_to_numpy=True)
            
            # Engineer features
            status_features = engineer_status_features(caption)
            
            # Prepare feature array in order
            style_features = model_registry.status_style_features
            style_values = np.array([[status_features.get(col, 0) for col in style_features]])
            
            # Combine embedding + style features
            X = np.hstack([caption_emb, style_values])
            
            # Use Random Forest alone for better discrimination
            # (XGB and LGB are too biased toward predicting "fake")
            rf_prob = model_registry.status_rf.predict_proba(X)[:, 1][0]
            
            # Apply sigmoid calibration centered at 0.46 (the observed mean)
            z_score = (rf_prob - 0.46) / 0.008
            calibrated_score = 1.0 / (1.0 + np.exp(-z_score))
            
            label = "Fake/Spam" if calibrated_score >= 0.50 else "Real"
            
            return {
                "status": label,
                "suspicion_score": float(calibrated_score),
                "threshold": 0.50,
                "confidence": abs(float(calibrated_score) - 0.5) * 2,
            }
        except Exception as e:
            return {"error": f"Status prediction failed: {str(e)}"}
