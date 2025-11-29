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


def _beautify_text(text: str, lang: str) -> str:
    """
    Basic text beautifier: normalizes whitespace, trims surrounding quotes,
    capitalizes the first character for Latin scripts, and ensures terminal punctuation.
    This is a simple safe fallback if no advanced NLP beautifier is available.
    """
    if not text:
        return ""

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Trim surrounding quotes and extra punctuation
    text = text.strip(" \t\n\r\"'")

    # Capitalize first character for languages that use Latin script
    try:
        if lang and lang.lower().startswith("en"):
            text = text[:1].upper() + text[1:]
        else:
            # For other languages, just safeguard non-empty text
            text = text[:1].upper() + text[1:] if text else text
    except Exception:
        pass

    # Ensure sentence ends with punctuation
    if text and text[-1] not in ".!?।":
        text = text + "."

    return text


def get_caption_from_video(video_path: str) -> dict:
    """
    Extracts audio from video and converts to caption.
    Falls back gracefully if speech_recognition unavailable.
    This implementation ensures a dict is returned on every code path.
    """
    if not HAS_SPEECH_RECOGNITION:
        return {
            "caption": "Video processing unavailable (speech recognition not installed)",
            "hashtags": [],
            "duration": 0
        }

    import importlib
    import os
    import subprocess

    duration = 0
    audio_path = None

    try:
        # Try moviepy first (preferred)
        try:
            moviepy_editor = importlib.import_module("moviepy.editor")
            VideoFileClip = getattr(moviepy_editor, "VideoFileClip")

            clip = VideoFileClip(video_path)
            duration = int(getattr(clip, "duration", 0))

            if clip.audio is None:
                clip.close()
                return {
                    "caption": "No audio detected in video. Please add audio to the video.",
                    "hashtags": [],
                    "duration": duration
                }

            # Extract audio to a temp wav file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
                audio_path = tmp_audio.name

            clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
            clip.close()

        except Exception:
            # Fallback: use FFmpeg to extract audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
                audio_path = tmp_audio.name

            cmd = [
                "ffmpeg", "-y", "-i", video_path, "-vn",
                "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000",
                audio_path
            ]

            try:
                subprocess.run(cmd, capture_output=True, timeout=60, check=True)
            except Exception:
                # Cleanup and return a clear failure if extraction failed
                try:
                    if audio_path and os.path.exists(audio_path):
                        os.remove(audio_path)
                except Exception:
                    pass
                return {
                    "caption": "Unable to extract audio from video. FFmpeg not installed or failed.",
                    "hashtags": [],
                    "duration": duration
                }

        # Recognize speech from the extracted audio (if any)
        text = ""
        if sr is not None and audio_path:
            recognizer = sr.Recognizer()
            try:
                with sr.AudioFile(audio_path) as source:
                    audio = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio, language="bn-BD")
                except sr.UnknownValueError:
                    try:
                        text = recognizer.recognize_google(audio, language="en-US")
                    except Exception:
                        text = ""
                except sr.RequestError:
                    text = ""
            except Exception:
                text = ""

        # Clean up temp file
        try:
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
        except Exception:
            pass

        if isinstance(text, (list, tuple)):
            text = " ".join(map(str, text))
        else:
            text = "" if text is None else str(text)

        lang = detect_language(text)
        caption = _beautify_text(text, lang)
        hashtags = [f"#{word.lower()}" for word in caption.split() if len(word) > 3][:10]

        return {
            "caption": caption,
            "hashtags": hashtags,
            "duration": duration
        }

    except Exception as e:
        # Ensure any temporary audio is removed and return an error dict
        try:
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
        except Exception:
            pass
        return {
            "caption": f"Error processing video: {str(e)}",
            "hashtags": [],
            "duration": 0
        }
