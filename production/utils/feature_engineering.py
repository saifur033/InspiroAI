"""
Feature engineering utilities - EXACT logic from notebooks
"""
import numpy as np
import pandas as pd
import emoji
import textstat
import re
from datetime import datetime
from utils.preprocess import get_sentiment, count_emojis


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
    features["emoji_count"] = emoji.emoji_count(caption)
    
    # Hashtag presence
    features["has_hashtag"] = 1 if "#" in caption else 0
    
    # Flesch-Kincaid grade
    try:
        features["fk_grade"] = textstat.flesch_kincaid_grade(caption) if len(words) > 0 else 0.0
    except:
        features["fk_grade"] = 0.0
    
    # Time features
    features["hour"] = timestamp.hour
    features["dow"] = timestamp.dayofweek
    features["is_weekend"] = 1 if timestamp.dayofweek in [5, 6] else 0
    
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
