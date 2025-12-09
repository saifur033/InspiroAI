"""
Feature engineering utilities - EXACT logic from notebooks
"""
import numpy as np
import pandas as pd
import textstat
import re
from datetime import datetime
from utils.preprocess import get_sentiment, count_emojis

# Simple emoji counter to avoid emoji module dependency
def emoji_count(text):
    """Count emojis in text"""
    return count_emojis(text)


def engineer_reach_features(caption, timestamp=None, category="", language=""):
    """
    Engineer features for REACH PREDICTION model
    EXACT logic from reach_prediction_cap_C_final.ipynb
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    # Handle timestamp conversion
    if isinstance(timestamp, str):
        timestamp = pd.to_datetime(timestamp, errors="coerce")
        if pd.isna(timestamp):
            timestamp = datetime.now()
    elif not isinstance(timestamp, (datetime, pd.Timestamp)):
        timestamp = datetime.now()
    
    features = {}
    
    # Text features
    features["char_count"] = len(caption)
    features["word_count"] = len(caption.split())
    
    # Average word length
    words = caption.split()
    features["avg_word_len"] = np.mean([len(w) for w in words]) if len(words) > 0 else 0.0
    
    # Emoji count
    features["emoji_count"] = emoji_count(caption)
    
    # Hashtag presence
    features["has_hashtag"] = 1 if "#" in caption else 0
    
    # Flesch-Kincaid grade
    try:
        if len(words) > 0:
            fk_fn = getattr(textstat, "flesch_kincaid_grade", None)
            if callable(fk_fn):
                features["fk_grade"] = fk_fn(caption)
            else:
                # fallback to various possible TextStat class locations in different textstat versions
                TextStatClass = (
                    getattr(textstat, "TextStat", None)
                    or getattr(textstat, "Textstat", None)
                    or getattr(textstat, "textstat", None)
                )
                if TextStatClass is None:
                    # try submodule import
                    try:
                        from textstat import textstat as _ttextstat  # type: ignore
                        TextStatClass = getattr(_ttextstat, "TextStat", None) or getattr(_ttextstat, "Textstat", None) or _ttextstat
                    except Exception:
                        TextStatClass = None
                if TextStatClass is not None:
                    inst = TextStatClass() if callable(TextStatClass) else TextStatClass
                    fk_method = getattr(inst, "flesch_kincaid_grade", None)
                    if callable(fk_method):
                        features["fk_grade"] = fk_method(caption)
                    else:
                        features["fk_grade"] = 0.0
                else:
                    features["fk_grade"] = 0.0
        else:
            features["fk_grade"] = 0.0
    except Exception:
        features["fk_grade"] = 0.0
    
    # Time features
    features["hour"] = timestamp.hour
    # determine day-of-week robustly: prefer pandas Timestamp.dayofweek if present, otherwise use datetime.weekday()
    dow_attr = getattr(timestamp, "dayofweek", None)
    if dow_attr is None:
        # datetime.datetime and pandas.Timestamp both implement weekday(), so use it as fallback
        try:
            dow = int(timestamp.weekday())
        except Exception:
            # last-resort fallback to 0 (Monday)
            dow = 0
    else:
        dow = int(dow_attr)
    features["dow"] = dow
    features["is_weekend"] = 1 if dow in [5, 6] else 0
    
    # Cyclical encodings (EXACT from notebook)
    features["hour_sin"] = np.sin(2 * np.pi * features["hour"] / 24)
    features["hour_cos"] = np.cos(2 * np.pi * features["hour"] / 24)
    features["dow_sin"] = np.sin(2 * np.pi * features["dow"] / 7)
    features["dow_cos"] = np.cos(2 * np.pi * features["dow"] / 7)
    
    return features


def engineer_status_features(caption):
    """
    Engineer features for STATUS (Fake/Real) DETECTION model
    EXACT logic from status_final_cap_C.ipynb
    """
    features = {}
    words = caption.split()
    
    # Text length features
    features["text_length"] = len(words)
    
    # Emoji features
    features["num_emojis"] = count_emojis(caption)
    
    # Punctuation
    features["punctuation_count"] = len(re.findall(r'[!?]', caption))
    
    # Link detection
    features["has_links"] = 1 if re.search(r'http|www', caption) else 0
    
    # Sentiment (mapped: -1, 0, 1)
    features["sentiment"] = get_sentiment(caption)
    
    # Engagement metrics (will be set to 0 for new posts)
    features["total_engagement"] = 0
    features["log_engagement"] = 0
    
    # Advanced text features
    features["avg_word_len"] = np.mean([len(w) for w in words]) if len(words) > 0 else 0.0
    features["num_hashtags"] = len(re.findall(r'#', caption))
    features["num_mentions"] = len(re.findall(r'@', caption))
    
    # Uppercase ratio
    features["uppercase_ratio"] = sum(1 for c in caption if c.isupper()) / len(caption) if len(caption) > 0 else 0.0
    
    return features


def generate_temporal_features(hour):
    """
    Generate temporal features for a specific hour (0-23)
    Used by best_time.py
    """
    features = {
        "hour": hour,
        "hour_sin": np.sin(2 * np.pi * hour / 24),
        "hour_cos": np.cos(2 * np.pi * hour / 24),
        "dow": 2,  # Wednesday (middle of week)
        "dow_sin": np.sin(2 * np.pi * 2 / 7),
        "dow_cos": np.cos(2 * np.pi * 2 / 7),
        "is_weekend": 0,
    }
    return features


def predict_reach_for_hours(caption, day_name, embedder, model_registry):
    """
    Predict reach for each hour of a given day using ML model
    
    Args:
        caption: Post caption text
        day_name: Day name (Monday, Tuesday, etc.)
        embedder: Sentence transformer for embeddings
        model_registry: Model registry with reach predictor
    
    Returns:
        List of tuples: (hour_str, reach_probability, hour_int)
    """
    from datetime import datetime
    from scipy import sparse
    import numpy as np
    
    # Map day name to integer (Monday=0, ..., Sunday=6)
    day_map = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
        "Friday": 4, "Saturday": 5, "Sunday": 6
    }
    day_int = day_map.get(day_name, 2)
    
    # Pre-compute day-level features (same for all hours)
    day_sin = np.sin(2 * np.pi * day_int / 7)
    day_cos = np.cos(2 * np.pi * day_int / 7)
    is_weekend = 1 if day_int in [5, 6] else 0
    
    # Get caption embedding (single embedding reused for all hours)
    caption_emb = embedder.encode([caption], convert_to_numpy=True)
    caption_emb_sparse = sparse.csr_matrix(caption_emb)
    
    # Column names for numeric features
    num_cols = model_registry.reach_meta.get("num_cols", [
        "char_count", "word_count", "avg_word_len", "emoji_count",
        "has_hashtag", "fk_grade", "hour", "dow", "is_weekend",
        "hour_sin", "hour_cos", "dow_sin", "dow_cos"
    ])
    
    results = []
    
    # Predict for each hour (0-23)
    for hour in range(24):
        # Hour-specific trigonometric encoding
        hour_sin = np.sin(2 * np.pi * hour / 24)
        hour_cos = np.cos(2 * np.pi * hour / 24)
        
        # Engineer base features for reach
        reach_features = engineer_reach_features(caption, timestamp=datetime.now(), category="", language="")
        
        # Override with specific hour and day
        reach_features["hour"] = hour
        reach_features["dow"] = day_int
        reach_features["is_weekend"] = is_weekend
        reach_features["hour_sin"] = hour_sin
        reach_features["hour_cos"] = hour_cos
        reach_features["dow_sin"] = day_sin
        reach_features["dow_cos"] = day_cos
        
        # Build numeric feature vector
        num_values = np.array([[reach_features.get(col, 0) for col in num_cols]])
        num_scaled = model_registry.reach_scaler.transform(num_values)
        num_sparse = sparse.csr_matrix(num_scaled)
        
        # Empty categorical features
        cat_sparse = sparse.csr_matrix((1, 0))
        
        # Combine embeddings + categories + numeric features
        X = sparse.hstack([caption_emb_sparse, cat_sparse, num_sparse], format="csr")
        
        # Get probability prediction
        try:
            if hasattr(model_registry.reach_model, "predict_proba"):
                prob = float(model_registry.reach_model.predict_proba(X)[:, 1][0])
            else:
                prob = float(model_registry.reach_model.predict(X)[0])
        except Exception:
            prob = 0.0
        
        # Convert hour to 12-hour format for display
        if hour == 0:
            hour_str = "12:00 AM"
        elif hour < 12:
            hour_str = f"{hour}:00 AM"
        elif hour == 12:
            hour_str = "12:00 PM"
        else:
            hour_str = f"{hour-12}:00 PM"
        
        results.append((hour_str, prob, hour))
    
    return results

