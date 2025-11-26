# ==========================================================
# voice_caption.py — InspiroAI Voice Engine v5.0 (2025 Stable)
# ==========================================================

import re
import random
import tempfile
import speech_recognition as sr

from src.utils import detect_language


# ---------------------------------------------------------
# 🎬 Video → Caption Engine
# ---------------------------------------------------------
def get_caption_from_video(video_path: str) -> dict:
    """
    Extracts audio from video and converts to caption.
    Returns: {caption, hashtags, duration}
    """
    try:
        # Try importing moviepy for audio extraction
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(video_path)
            duration = int(clip.duration)
            
            if clip.audio is None:
                return {
                    "caption": "No audio detected in video. Please add audio to the video.",
                    "hashtags": [],
                    "duration": duration
                }
            
            # Extract audio to temp wav file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
                audio_path = tmp_audio.name
            
            clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
            
            # Convert audio to text
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio, language="bn-BD")
            except sr.UnknownValueError:
                text = recognizer.recognize_google(audio, language="en-US")
            
            clip.close()
            
            # Clean and beautify
            lang = detect_language(text)
            caption = _beautify_text(text, lang)
            
            # Generate hashtags from caption
            words = caption.split()
            hashtags = [f"#{word.lower()}" for word in words if len(word) > 3][:10]
            
            return {
                "caption": caption,
                "hashtags": hashtags,
                "duration": duration
            }
        
        except ImportError:
            # Fallback: use FFmpeg if available
            import subprocess
            import os
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
                audio_path = tmp_audio.name
            
            # Extract audio using ffmpeg
            cmd = [
                "ffmpeg", "-i", video_path, "-q:a", "9", "-n",
                "-acodec", "libmp3lame", "-ac", "2", "-ar", "44100",
                audio_path
            ]
            
            try:
                subprocess.run(cmd, capture_output=True, timeout=60, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                return {
                    "caption": "Unable to extract audio from video. FFmpeg not installed.",
                    "hashtags": [],
                    "duration": 0
                }
            
            # Convert extracted audio to text
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio, language="bn-BD")
            except sr.UnknownValueError:
                text = recognizer.recognize_google(audio, language="en-US")
            
            # Clean up temp file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
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

    try:
        # Save bytes → temp .wav file (SpeechRecognition requires file)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_file:
            temp_file.write(audio_bytes)
            temp_file.flush()

            # Read audio
            with sr.AudioFile(temp_file.name) as source:
                audio = recognizer.record(source)

        # Try both English + Bangla (auto failover)
        try:
            text = recognizer.recognize_google(audio, language="bn-BD")
        except sr.UnknownValueError:
            text = recognizer.recognize_google(audio, language="en-US")

        # Detect actual language
        lang = detect_language(text)

        # Make text beautiful
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
