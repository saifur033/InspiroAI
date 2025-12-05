"""
Best posting time prediction engine
"""
import numpy as np
from scipy import sparse
from utils.feature_engineering import generate_temporal_features


def find_best_posting_hour(caption, model_registry, embedder, scaler, ohe):
    """
    Find optimal posting hour (0-23) for maximum reach
    
    Args:
        caption: Post caption text
        model_registry: Loaded models
        embedder: Sentence transformer for embeddings
        scaler: Feature scaler
        ohe: One-hot encoder for categorical features
    
    Returns:
        dict with best hour, reach probability, and hourly predictions
    """
    results = {}
    reach_probs = []
    
    # Get caption embedding (constant across hours)
    caption_embedding = embedder.encode([caption], convert_to_numpy=True)
    caption_emb_sparse = sparse.csr_matrix(caption_embedding)
    
    # Loop through each hour (0-23)
    for hour in range(24):
        # Generate temporal features for this hour
        hour_features = generate_temporal_features(hour)
        
        # Extract numeric features in correct order (from reach_meta)
        num_cols = model_registry.reach_meta.get("num_cols", [
            "char_count", "word_count", "avg_word_len", "emoji_count", 
            "has_hashtag", "fk_grade", "hour", "dow", "is_weekend",
            "hour_sin", "hour_cos", "dow_sin", "dow_cos"
        ])
        
        # Build numeric feature array
        num_values = np.array([[
            len(caption),
            len(caption.split()),
            np.mean([len(w) for w in caption.split()]) if len(caption.split()) > 0 else 0,
            caption.count("🙂") + caption.count("😊"),  # approximation
            1 if "#" in caption else 0,
            0.0,  # fk_grade
            hour,
            2,  # dow (Wednesday)
            0,  # is_weekend
            hour_features["hour_sin"],
            hour_features["hour_cos"],
            hour_features["dow_sin"],
            hour_features["dow_cos"],
        ]])
        
        # Scale numeric features
        num_scaled = scaler.transform(num_values)
        num_sparse = sparse.csr_matrix(num_scaled)
        
        # Empty categorical (no category/language for new posts)
        cat_sparse = sparse.csr_matrix((1, 0))
        
        # Combine features
        X_hour = sparse.hstack([caption_emb_sparse, cat_sparse, num_sparse], format="csr")
        
        # Predict reach probability
        if hasattr(model_registry.reach_model, "predict_proba"):
            prob = float(model_registry.reach_model.predict_proba(X_hour)[:, 1][0])
        else:
            prob = float(model_registry.reach_model.predict(X_hour)[0])
        
        reach_probs.append({
            "hour": hour,
            "probability": prob,
            "label": "High" if prob >= model_registry.reach_threshold else "Low"
        })
    
    # Find best hour
    best_hour_data = max(reach_probs, key=lambda x: x["probability"])
    
    return {
        "best_hour": best_hour_data["hour"],
        "best_probability": best_hour_data["probability"],
        "hourly_predictions": reach_probs,
        "recommendation": f"Best time to post: {best_hour_data['hour']:02d}:00 with {best_hour_data['probability']:.1%} reach probability"
    }
