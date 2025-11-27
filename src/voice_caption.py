# ==========================================================
# voice_caption.py — InspiroAI Voice Engine v5.1 (Stable)
# ==========================================================

import re
import random
import tempfile
import os

try:
    import speech_recognition as sr
    HAS_SPEECH_RECOGNITION = True
except ImportError:
    HAS_SPEECH_RECOGNITION = False
    sr = None

from src.utils import detect_language


def get_caption_from_video(video_path: str) -> dict:
    """Fallback: Video processing not available on Render"""
    return {
        "caption": "Video processing is being upgraded. Please try again soon!",
        "hashtags": [],
        "duration": 0
    }


def _beautify_text(text: str, lang: str) -> str:
    """Clean and beautify text"""
    if not text:
        return "Amazing moment captured! ✨"
    
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    
    if text and not text[0].isupper():
        text = text[0].upper() + text[1:]
    
    if not text.endswith((".", "!", "?", "…", "।")):
        text += random.choice([".", "!", "…"])
    
    return text.strip()


def convert_voice(audio_bytes: bytes) -> str:
    """
    Converts audio to caption text.
    Falls back gracefully if speech_recognition unavailable.
    """
    
    if not HAS_SPEECH_RECOGNITION or sr is None:
        return "Voice processing temporarily unavailable. Try again soon!"
    
    recognizer = sr.Recognizer()
    temp_path = None
    
    try:
        # Save bytes to temp WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        
        # Recognize speech
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)
        
        # Try Bangla then English
        try:
            text = recognizer.recognize_google(audio, language="bn-BD")
        except:
            try:
                text = recognizer.recognize_google(audio, language="en-US")
            except:
                text = ""
        
        if isinstance(text, (list, tuple)):
            text = " ".join(map(str, text))
        else:
            text = "" if text is None else str(text)
        
        lang = detect_language(text)
        return _beautify_text(text, lang)
    
    except Exception:
        return "Voice processing encountered an issue. Try again."
    finally:
        try:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass
