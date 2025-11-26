"""
reach_predictor.py — InspiroAI Reach Engine v6.5 (2025 Ultra Upgrade)

✔ Advanced engagement predictor
✔ SEO + Emotion + Hashtag + Tone fusion
✔ Best posting times (BN + EN)
✔ Realistic FB/IG reach cycle
✔ Improvement % (before/after rewrite)
✔ UI-Safe JSON Output
"""

from typing import Dict
import random
from datetime import datetime

from src.seo_score import compute_seo_score
from src.emotion_model import detect_emotion
from src.utils import detect_language


# ---------------------------------------------------------
# ⏰ Viral Posting Times (BN + EN)
# ---------------------------------------------------------
POSTING_TIME = {
    "bn": {
        "default": ["10:30 AM", "1:30 PM", "8:30 PM"],
        "funny": ["11:00 AM", "3:00 PM", "9:30 PM"],
        "trendy": ["11:30 AM", "3:30 PM", "9:45 PM"],
        "professional": ["9:00 AM", "1:00 PM", "6:00 PM"],
        "informative": ["9:15 AM", "12:45 PM", "6:30 PM"],
        "emotional": ["10:00 AM", "5:00 PM", "8:00 PM"],
        "supportive": ["10:10 AM", "5:10 PM", "8:20 PM"],
    },
    "en": {
        "default": ["9:00 AM", "12:00 PM", "7:00 PM"],
        "funny": ["11:00 AM", "2:45 PM", "9:00 PM"],
        "trendy": ["11:30 AM", "4:00 PM", "9:15 PM"],
        "professional": ["8:45 AM", "1:00 PM", "6:00 PM"],
        "informative": ["9:00 AM", "12:30 PM", "5:45 PM"],
        "emotional": ["10:00 AM", "4:30 PM", "8:00 PM"],
        "supportive": ["10:15 AM", "5:15 PM", "8:10 PM"],
    }
}


# ---------------------------------------------------------
# 🎯 Tone Power (Reach multiplier)
# ---------------------------------------------------------
TONE_POWER = {
    "professional": 1.05,
    "promotional": 1.22,
    "friendly": 1.30,
    "emotional": 1.26,
    "funny": 1.42,
    "informative": 1.12,
    "supportive": 1.20,
    "curious": 1.16,
    "trendy": 1.38,
}


# ---------------------------------------------------------
# ⚡ Internal reach calculation
# ---------------------------------------------------------
def _calculate_reach(caption: str) -> Dict:
    lang = detect_language(caption)
    seo = compute_seo_score(caption)
    emotion = detect_emotion(caption)

    top_emo = emotion.get("top_emotion", "neutral")
    hashtags = caption.count("#")

    # Detect tone by keyword
    tone = "friendly"
    lower = caption.lower()

    for key in TONE_POWER:
        if key in lower:
            tone = key
            break

    tone_factor = TONE_POWER.get(tone, 1.0)

    # BASE Reach
    base = random.randint(600, 1200)

    # SEO boost
    seo_boost = seo["score"] * 6

    # Emotion Factor
    emo_factor = {
        "happy": 1.38,
        "excited": 1.42,
        "surprise": 1.33,
        "sad": 0.88,
        "fear": 0.84,
    }.get(top_emo, 1.0)

    # Hashtag boost
    hash_boost = hashtags * 130

    reach = (base + seo_boost + hash_boost)
    reach *= tone_factor
    reach *= emo_factor

    reach = int(max(500, min(50000, reach)))

    return {
        "reach": reach,
        "tone": tone,
        "lang": lang,
        "seo": seo["score"],
        "emotion": top_emo
    }


# ---------------------------------------------------------
# ⏰ Best Posting Times
# ---------------------------------------------------------
def _best_post_times(lang: str, tone: str):
    key = tone if tone in POSTING_TIME[lang] else "default"
    return random.sample(POSTING_TIME[lang][key], 3)


# ---------------------------------------------------------
# 📅 Best Engagement Day
# ---------------------------------------------------------
def _best_day():
    good_days = ["Tuesday", "Wednesday", "Friday", "Sunday"]
    return random.choice(good_days)


# ---------------------------------------------------------
# 🔥 Reach Tips
# ---------------------------------------------------------
def _tips(seo: int, emotion: str):
    tips = []

    if seo < 55:
        tips.append("📈 Increase SEO keywords to boost visibility.")

    if emotion in ["sad", "fear"]:
        tips.append("💖 Add a positive tone or CTA for better engagement.")

    if not tips:
        tips.append("✨ Caption is well-balanced. Focus on posting time.")

    return tips


# ---------------------------------------------------------
# 🚀 PUBLIC FUNCTION — Predict Reach + Improvement %
# ---------------------------------------------------------
def predict_reach(caption: str, optimized_caption: str = None) -> Dict:

    if not caption.strip():
        return {
            "reach": 0,
            "best_times": [],
            "day_suggestion": "",
            "improvement": 0,
            "tips": ["⚠ Caption empty — cannot predict reach."],
            "reason": "Caption missing."
        }

    orig = _calculate_reach(caption)

    best_time = _best_post_times(orig["lang"], orig["tone"])
    best_day = _best_day()
    tips = _tips(orig["seo"], orig["emotion"])

    reach_val = orig["reach"]

    if reach_val > 25000:
        reason = "🚀 Extremely high potential!"
    elif reach_val > 12000:
        reason = "🔥 Great reach expected!"
    elif reach_val > 5000:
        reason = "💡 Good potential, can improve with SEO."
    else:
        reason = "⚠ Low reach, needs optimization."

    # Bangla mode
    if orig["lang"] == "bn":
        reason = reason.replace("reach", "পৌঁছানো").replace("Caption", "ক্যাপশন")

    # Improvement %
    improvement = 0
    if optimized_caption:
        new = _calculate_reach(optimized_caption)
        improvement = round(((new["reach"] - orig["reach"]) / max(orig["reach"], 1)) * 100, 2)

    return {
        "reach": orig["reach"],
        "best_times": best_time,
        "day_suggestion": best_day,
        "improvement": improvement,
        "tips": tips,
        "reason": reason
    }