# ==========================================================
# utils.py — InspiroAI Core Utility Functions (2025 v4.0)
# ==========================================================

import re
import os


# ----------------------------------------------------------
# CLEAN TEXT (remove emojis, symbols)
# ----------------------------------------------------------
def clean_text(text: str) -> str:
    if not text:
        return ""
    # Remove emojis & symbols
    return re.sub(r"[^\w\s\u0980-\u09FF]", " ", text).strip()


# ----------------------------------------------------------
# 🔥 ULTRA ACCURATE LANGUAGE DETECTOR (Bangla vs English)
# ----------------------------------------------------------
def detect_language(text: str) -> str:
    """
    Very accurate Bangla vs English detector.
    Supports mixed text, hashtags, emojis, symbols.
    """

    if not text or not text.strip():
        return "en"

    cleaned = clean_text(text)

    bn_count = sum(1 for ch in cleaned if 2432 <= ord(ch) <= 2559)
    en_count = sum(1 for ch in cleaned if "a" <= ch.lower() <= "z")

    # Fully Bangla
    if bn_count > 0 and en_count == 0:
        return "bn"

    # Fully English
    if en_count > 0 and bn_count == 0:
        return "en"

    # Mixed content → ratio-based
    if bn_count >= en_count:
        return "bn"
    else:
        return "en"


# ----------------------------------------------------------
# EXTENSION → FILE TYPE
# ----------------------------------------------------------
def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[-1].lower()


# ----------------------------------------------------------
# IMAGE CHECKER
# ----------------------------------------------------------
def is_image(filename: str) -> bool:
    ext = get_file_extension(filename)
    return ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]


# ----------------------------------------------------------
# VIDEO CHECKER
# ----------------------------------------------------------
def is_video(filename: str) -> bool:
    ext = get_file_extension(filename)
    return ext in [".mp4", ".mov", ".avi", ".mkv", ".wmv"]
