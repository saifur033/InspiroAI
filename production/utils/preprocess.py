"""
Preprocessing utilities - EXACT logic from notebooks
"""
import re
import numpy as np
import pandas as pd
from textblob import TextBlob


def clean_text_basic(text):
    """Basic text cleaning"""
    t = re.sub(r'http\S+', '', str(text))
    t = re.sub(r'@\w+', '', t)
    t = re.sub(r'#\w+', '', t)
    t = re.sub(r'[^a-zA-Z\s]', ' ', t)
    return t.lower().strip()


def get_sentiment(text):
    """
    Get sentiment score using TextBlob
    Maps to: negative=-1, neutral=0, positive=1
    """
    try:
        blob = TextBlob(str(text))
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return 1  # positive
        elif polarity < -0.1:
            return -1  # negative
        else:
            return 0  # neutral
    except:
        return 0


def count_emojis(text):
    """Count emojis in text"""
    return len(re.findall(r'[\U00010000-\U0010ffff]', str(text)))


def emotion_preprocessing(text):
    """
    Preprocess for emotion detection model
    """
    # TF-IDF expects lowercase, basic cleaning
    text = str(text).lower().strip()
    return text


def reach_text_preprocessing(text):
    """
    Preprocess text for reach prediction
    No aggressive cleaning - embedder handles it
    """
    return str(text).lower().strip()


def status_text_preprocessing(text):
    """
    Preprocess text for status (fake/real) detection
    No aggressive cleaning - embedder handles it
    """
    return str(text).lower().strip()
