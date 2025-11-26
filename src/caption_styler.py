"""
Caption Styling Engine - Auto-format captions for different platforms
Generates beautiful styled captions ready for Facebook, Instagram, TikTok, etc.
"""

import re
from typing import Dict, List

def format_caption_styles(caption: str, is_bangla: bool = False) -> Dict[str, str]:
    """
    Generate multiple styled versions of caption for different platforms
    
    Args:
        caption: Original caption text
        is_bangla: Whether caption is in Bangla
    
    Returns:
        Dictionary with different styled versions
    """
    
    caption = caption.strip()
    
    # Style 1: Minimal Clean (no emojis)
    style_minimal = caption
    
    # Style 2: Emoji Enhanced
    if is_bangla:
        # Bangla caption styling
        style_emoji = f"✨ {caption} ✨\n\n#পণ্য #নতুন #অফার"
    else:
        # English caption styling
        style_emoji = f"✨ {caption} ✨\n\n#NewProduct #Special #Offer"
    
    # Style 3: Call-to-Action Enhanced
    if is_bangla:
        cta_phrases = [
            "এখনই দেখুন! 👇",
            "আরও জানতে ক্লিক করুন 👇",
            "এই অফার মিস করবেন না 🔥",
            "এখনই যোগদান করুন 👇"
        ]
        style_cta = f"{caption}\n\n{cta_phrases[0]}"
    else:
        cta_phrases = [
            "Check it out now! 👇",
            "Click to learn more 👇",
            "Don't miss this offer 🔥",
            "Join now 👇"
        ]
        style_cta = f"{caption}\n\n{cta_phrases[0]}"
    
    # Style 4: Storytelling (multi-line)
    if is_bangla:
        style_story = f"""📢 নতুন ঘোষণা!

{caption}

আপনার পছন্দের জন্য অপেক্ষা করছি 💝

#নতুন #পণ্য #বিশেষ"""
    else:
        style_story = f"""📢 New Announcement!

{caption}

Excited to share this with you! 🎉

#NewProduct #Announcement #Special"""
    
    # Style 5: Hashtag Heavy
    if is_bangla:
        hashtags = " #নতুনপণ্য #বিশেষঅফার #এখনকিনুন #সেরামূল্য #গুণমান #বিশ্বাসযোগ্য"
        style_hashtag = f"{caption}\n\n{hashtags}"
    else:
        hashtags = " #NewProduct #SpecialOffer #BuyNow #BestPrice #Quality #Trusted"
        style_hashtag = f"{caption}\n\n{hashtags}"
    
    # Style 6: Professional/Formal
    if is_bangla:
        style_professional = f"""আমরা আপনাদের জন্য নিয়ে এসেছি:

{caption}

আমাদের সাথে থাকার জন্য ধন্যবাদ। ✨"""
    else:
        style_professional = f"""We are pleased to present:

{caption}

Thank you for your continued support. ✨"""
    
    # Style 7: Casual/Friendly
    if is_bangla:
        style_casual = f"""হেই! 👋

{caption}

এটা খুবই দুর্দান্ত! 🎊"""
    else:
        style_casual = f"""Hey! 👋

{caption}

This is amazing! 🎊"""
    
    # Style 8: Bold/Attention-Grabbing
    if is_bangla:
        style_bold = f"""🔥 এটা দেখুন! 🔥

{caption}

এখনই অ্যাকশন নিন!"""
    else:
        style_bold = f"""🔥 Check This Out! 🔥

{caption}

Take Action Now!"""
    
    return {
        "minimal": style_minimal,
        "emoji": style_emoji,
        "cta": style_cta,
        "story": style_story,
        "hashtag": style_hashtag,
        "professional": style_professional,
        "casual": style_casual,
        "bold": style_bold
    }


def get_best_caption_for_platform(caption: str, platform: str, is_bangla: bool = False) -> str:
    """
    Get the best styled caption for a specific platform
    
    Args:
        caption: Original caption
        platform: 'facebook', 'instagram', 'tiktok', 'twitter', 'default'
        is_bangla: Whether caption is in Bangla
    
    Returns:
        Styled caption for the platform
    """
    
    styles = format_caption_styles(caption, is_bangla)
    
    platform_style_map = {
        "facebook": "story",      # Facebook likes longer, storytelling format
        "instagram": "hashtag",   # Instagram loves hashtags
        "tiktok": "bold",         # TikTok needs attention-grabbing
        "twitter": "cta",         # Twitter is call-to-action focused
        "linkedin": "professional",  # LinkedIn is professional
        "default": "emoji"        # Default with emojis
    }
    
    style_key = platform_style_map.get(platform.lower(), "emoji")
    return styles.get(style_key, caption)


def auto_enhance_caption(caption: str, is_bangla: bool = False) -> Dict:
    """
    Auto-enhance caption with all styles and platform recommendations
    
    Args:
        caption: Original caption
        is_bangla: Whether caption is in Bangla
    
    Returns:
        Dictionary with all styles and platform-specific versions
    """
    
    styles = format_caption_styles(caption, is_bangla)
    
    result = {
        "original": caption,
        "styles": styles,
        "platform_recommendations": {
            "facebook": get_best_caption_for_platform(caption, "facebook", is_bangla),
            "instagram": get_best_caption_for_platform(caption, "instagram", is_bangla),
            "tiktok": get_best_caption_for_platform(caption, "tiktok", is_bangla),
            "twitter": get_best_caption_for_platform(caption, "twitter", is_bangla),
            "linkedin": get_best_caption_for_platform(caption, "linkedin", is_bangla)
        },
        "recommended_for_fb": get_best_caption_for_platform(caption, "facebook", is_bangla)
    }
    
    return result
