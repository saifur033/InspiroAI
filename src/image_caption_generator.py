"""
image_caption_generator.py — InspiroAI v10.0 (Lightweight)
Simplified template-based captions for Render compatibility
"""

from typing import Optional, Dict, List, Any
import random


def generate_caption_for_image(image_bytes: bytes, filename: Optional[str] = "") -> Dict:
    """Generate image caption using templates"""
    
    templates = [
        "This moment is absolutely magical! ✨ Perfectly captured!",
        "Pure beauty in every frame! 📸✨ Stunning composition!",
        "Breathtaking and inspiring! 🌟✨ Love this shot!",
        "Absolutely mesmerizing! 💫✨ Incredible capture!",
        "Stunning visual storytelling! 🎨✨ Well done!",
        "This deserves all the attention! 🔥✨ Amazing work!",
        "Perfectly beautiful moment! 😍✨ Timeless capture!",
        "Absolutely gorgeous! 🌈✨ Love the composition!",
    ]
    
    hashtags = ["photography", "momentcapture", "visualart", "instagram", 
               "instaworthy", "artistic", "beautiful", "stunning",
               "amazing", "photooftheday", "viral", "trending"]
    
    try:
        caption = random.choice(templates)
    except:
        caption = "Beautiful moment captured! 📸✨ Pure artistry!"
    
    return {
        "caption": caption,
        "hashtags": hashtags[:12],
        "image_type": "general",
        "tone": "bright"
    }
