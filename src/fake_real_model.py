import re
from typing import Dict

def detect_fake(text: str) -> Dict:
    """
    Detect authenticity with caption-specific reasoning (NOT GENERIC!)
    Returns: {
        "real": 0-100 int (% authentic),
        "fake": 0-100 int (% AI-generated),
        "reason": text (specific to caption content)
    }
    Guarantee: real + fake = 100
    """
    if not text or not text.strip():
        return {
            "real": 0,
            "fake": 100,
            "reason": "No content to analyze."
        }

    text_original = text.strip()
    text_lower = text.lower()
    word_count = len(re.findall(r"\w+", text_lower))
    emoji_count = len(re.findall(r"[\U0001F300-\U0001FAFF\u2764\uFE0F✨🌟💫🌸🔥☺️❤️😍🤩😇🌿🎉👍🙌💪]", text))
    punctuation_count = len(re.findall(r"[.!?]", text))

    real_score = 50.0
    fake_score = 50.0

    # Extract key topics from text for specific reasoning
    stop_words = {'that', 'this', 'with', 'from', 'about', 'have', 'been', 'their', 'they', 'would', 'which', 'these', 'those'}
    words = [w for w in re.findall(r'\b\w+\b', text_lower) if len(w) >= 4 and w not in stop_words]
    key_words = list(dict.fromkeys(words))[:3]  # Top 3 unique words
    main_topic = ' '.join(key_words[:2]) if len(key_words) >= 2 else (key_words[0] if key_words else 'content')

    technical_keywords = ["data", "analysis", "algorithm", "research", "study", "test", "experiment", "method", "result", "conclusion"]
    emotional_intensity_words = ["amazing", "incredible", "unbelievable", "shocking", "mind-blowing", "transformative", "revolutionary"]
    exaggerated_phrases = ["best ever", "once in a lifetime", "guaranteed", "100% effective", "life-changing", "absolutely perfect"]
    general_phrases = ["everyone knows", "it is said", "people believe", "supposedly", "allegedly", "they say"]
    personal_storytelling = ["i", "me", "my", "we", "our", "our journey", "my experience"]

    real_score += sum(5 for word in technical_keywords if word in text_lower)
    has_intensity = sum(3 for word in emotional_intensity_words if word in text_lower)
    real_score += has_intensity
    fake_score += sum(5 for phrase in exaggerated_phrases if phrase in text_lower)
    fake_score += sum(3 for phrase in general_phrases if phrase in text_lower)
    real_score += sum(5 for word in personal_storytelling if word in text_lower)

    if emoji_count > 3:
        fake_score += 8
    elif emoji_count >= 1:
        real_score += 3

    if punctuation_count >= 3:
        real_score += 5
    elif punctuation_count == 0:
        fake_score += 3

    real_score = min(100.0, max(0.0, real_score))
    fake_score = 100.0 - real_score

    # Generate CAPTION-SPECIFIC reason (not generic!)
    reason = _generate_authenticity_reason(main_topic, real_score, fake_score, has_intensity > 0, personal_storytelling, text_lower, emoji_count)

    return {
        "real": int(round(real_score)),
        "fake": int(round(fake_score)),
        "reason": reason
    }


def _generate_authenticity_reason(topic: str, real_score: float, fake_score: float, has_intensity: bool, personal_words: list, text_lower: str, emoji_count: int) -> str:
    """
    Generate caption-specific authenticity reasoning.
    CRITICAL: Must mention specific aspects of the caption - NOT GENERIC!
    """
    # Check for specific patterns in the caption
    has_personal = any(word in text_lower for word in personal_words)
    has_specific_details = emoji_count > 0 or len(re.findall(r'\b\d+\b', text_lower)) > 0
    
    if real_score > 75:
        if has_personal:
            return f"'{topic}' discussed with personal experiences and authentic storytelling. Natural language and genuine emotions detected."
        else:
            return f"'{topic}' presented with specific details and measured tone. Shows authentic human expression without artificial patterns."
    elif real_score > 50:
        if has_intensity:
            return f"'{topic}' described with emotional language. Mix of authentic expression and some intensity words. Generally human-like content."
        else:
            return f"'{topic}' expressed with natural language patterns. Balanced tone with authentic human perspective."
    else:
        if has_intensity and emoji_count > 2:
            return f"'{topic}' contains multiple superlatives and excessive emojis. Pattern suggests AI-generated or heavily styled content."
        elif has_intensity:
            return f"'{topic}' uses intense emotional language repeatedly. May be AI-generated or artificially enhanced content."
        else:
            return f"'{topic}' shows patterns consistent with AI generation. Lacks personal details and natural conversation markers."
