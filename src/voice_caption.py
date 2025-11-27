# ==========================================================
# voice_caption.py — InspiroAI Voice Engine v5.0 (2025 Stable)
# ==========================================================

import re
import random
import tempfile

try:
    import speech_recognition as sr
    HAS_SPEECH_RECOGNITION = True
except ImportError:
    HAS_SPEECH_RECOGNITION = False
    sr = None

from src.utils import detect_language


# ---------------------------------------------------------
# 🎬 Video → Caption Engine (Fallback Mode)
# ---------------------------------------------------------
def get_caption_from_video(video_path: str) -> dict:
    """
    Extracts audio from video and converts to caption.
    Falls back gracefully if speech_recognition unavailable.
    """
    if not HAS_SPEECH_RECOGNITION:
        return {
            "caption": "Video processing unavailable (speech recognition not installed)",
            "hashtags": [],
            "duration": 0
        }
    
    try:
        import importlib
        import os

        # Try to use moviepy first
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

            # Recognize speech from the extracted audio
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
                if os.path.exists(audio_path):
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

        except ImportError:
            # Fallback: use FFmpeg extraction
            import subprocess

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
                audio_path = tmp_audio.name

            cmd = [
                "ffmpeg", "-i", video_path, "-q:a", "9", "-n",
                "-acodec", "libmp3lame", "-ac", "2", "-ar", "44100",
                audio_path
            ]

            try:
                subprocess.run(cmd, capture_output=True, timeout=60, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                except Exception:
                    pass
                return {
                    "caption": "Unable to extract audio from video. FFmpeg not installed or failed.",
                    "hashtags": [],
                    "duration": 0
                }

            # Use speech_recognition to convert extracted audio to text
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
                if os.path.exists(audio_path):
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
                "duration": 0
            }

    except Exception as e:
        return {
            "caption": f"Error processing video: {str(e)}",
            "hashtags": [],
            "duration": 0
        }



def _clean_voice_text(text: str) -> str:
    if not text:
        return ""

    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"([.!?…])\1+", r"\1", text)
    text = re.sub(r"\s+([.!?…])", r"\1", text)

    return text


# ---------------------------------------------------------
# ✨ Beautify / Make human
# ---------------------------------------------------------
def _beautify_text(text: str, lang: str) -> str:
    text = _clean_voice_text(text)

    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]

    # Auto add punctuation
    if not text.endswith((".", "!", "?", "…", "।")):
        text += random.choice([".", "!", "…"])

    # Emoji sets
    endings_en = ["✨", "🔥", "❤️", "💬", "🚀", "🎯", ""]
    endings_bn = ["✨", "🔥", "❤️", "😊", "🌸", "💫", ""]

    endings = endings_bn if lang == "bn" else endings_en

    # 40–50% chance
    if random.random() > 0.55:
        emo = random.choice(endings)
        if emo:
            text += " " + emo

    return text.strip()


# ---------------------------------------------------------
# 🎤 Voice → Text Engine
# ---------------------------------------------------------
def convert_voice(audio_bytes: bytes) -> str:
    """
    Converts audio (bytes) to readable caption text.
    Supports:
        - Mobile audio (WAV)
        - Browser audio (WEBM/OGG)
        - Desktop mic input
    """

    recognizer = sr.Recognizer()
    temp_path = None
    try:
        import os
        # Save incoming bytes to a temporary WAV file so sr.AudioFile can read it
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        # Read audio from the temp file
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)

        # Try both Bangla then English (auto failover)
        try:
            text = recognizer.recognize_google(audio, language="bn-BD")
        except sr.UnknownValueError:
            text = recognizer.recognize_google(audio, language="en-US")

        # Ensure recognized result is a string
        if isinstance(text, (list, tuple)):
            text = " ".join(map(str, text))
        else:
            text = "" if text is None else str(text)

        # Detect actual language and beautify
        lang = detect_language(text)
        final_caption = _beautify_text(text, lang)

        return final_caption

    # ---------------------------------------------------------
    # ❌ Error Handling
    # ---------------------------------------------------------
    except sr.UnknownValueError:
        return "Sorry, I could not understand the speech."

    except sr.RequestError:
        return "Speech service is unavailable right now."

    except Exception as e:
        return f"Unexpected Error: {e}"

    finally:
        # Clean up the temporary file if it was created
        try:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass
