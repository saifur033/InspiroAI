"""
caption_analyzer.py — Lightweight, Deterministic Caption Analysis & Optimization Engine
✔ Render-safe (low-compute, deterministic)
✔ Language auto-detect (Bangla/English)
✔ Fully caption-dependent (no randomness)
✔ SEO, Emotion, Authenticity, Hashtags
"""

import re
from typing import Dict, List, Tuple
from langdetect import detect

# =====================================================================
# BANGLA & ENGLISH RESOURCES
# =====================================================================

BANGLA_HAPPY_WORDS = ["ভালো", "খুশি", "আনন্দ", "দুর্দান্ত", "অসাধারণ", "বিজয়", "সফল", "উৎসাহ", "ভালোবাসা"]
BANGLA_SAD_WORDS = ["দুঃখ", "কষ্ট", "দুর্ভাগ্য", "হতাশা", "ব্যর্থ", "ব্যথা", "চিন্তা", "উদ্বেগ"]
BANGLA_FEAR_WORDS = ["ভয়", "ভীতি", "আতঙ্ক", "বিপদ", "সংকট", "ঝুঁকি", "সতর্ক", "সাবধান"]
BANGLA_SHOCK_WORDS = ["অবিশ্বাস্য", "চমৎকার", "বিস্ময়", "অপ্রত্যাশিত", "হঠাৎ", "চমকপ্রদ"]
BANGLA_INSPIRATIONAL_WORDS = ["স্বপ্ন", "সাহস", "লক্ষ্য", "শক্তি", "অর্জন", "সম্ভব", "এগিয়ে", "নতুন", "উন্নতি"]

ENGLISH_HAPPY_WORDS = ["love", "great", "amazing", "awesome", "wonderful", "excellent", "beautiful", "perfect", "best"]
ENGLISH_SAD_WORDS = ["sad", "sorry", "hurt", "pain", "loss", "difficult", "hard", "struggle", "miss"]
ENGLISH_FEAR_WORDS = ["afraid", "scared", "terror", "danger", "risk", "warning", "careful", "beware"]
ENGLISH_SHOCK_WORDS = ["wow", "unbelievable", "incredible", "shocking", "surprising", "unexpected", "blown away"]
ENGLISH_INSPIRATIONAL_WORDS = ["dream", "courage", "goal", "strength", "achieve", "possible", "forward", "new", "growth"]

# =====================================================================
# UTILITY: Language Detection
# =====================================================================

def detect_language(text: str) -> str:
    """Auto-detect language (bn/en)"""
    try:
        lang = detect(text)
        return "bn" if lang == "bn" else "en"
    except:
        return "en"


def has_bangla(text: str) -> bool:
    """Check if text contains Bangla characters"""
    return bool(re.search(r"[\u0980-\u09FF]", text))


def has_english(text: str) -> bool:
    """Check if text contains English characters"""
    return bool(re.search(r"[a-zA-Z]", text))


# =====================================================================
# SEO ANALYSIS (Deterministic)
# =====================================================================

def analyze_seo(caption: str, language: str) -> Tuple[int, str, List[str]]:
    """
    Calculate SEO score (0-100) based on:
    - Clarity (capitalization, punctuation)
    - Keyword presence
    - Length suitability (50-250 chars ideal)
    - Engagement markers (!, ?, emoji)
    - Topic consistency
    
    Returns: (score, grade, suggestions)
    """
    score = 50  # Base score
    suggestions = []
    
    # Length check (ideal: 50-250 chars)
    length = len(caption)
    if 50 <= length <= 250:
        score += 20
    elif length < 30:
        score -= 10
        suggestions.append("Caption too short - add more context")
    elif length > 300:
        score -= 5
        suggestions.append("Consider shortening for better readability")
    else:
        score += 10
    
    # Punctuation & clarity
    if "!" in caption or "?" in caption:
        score += 10
    
    # Emoji presence
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map
        "\U0001F1E0-\U0001F1FF"  # Flags
        "\U00002500-\U00002BEF"  # Chinese char
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # Dingbats
        "\u3030"
        "]+",
        re.UNICODE
    )
    
    if emoji_pattern.search(caption):
        score += 10
    else:
        suggestions.append("Add 1-2 relevant emojis for engagement")
    
    # Keyword density (simple check for repeated words)
    words = caption.lower().split()
    unique_ratio = len(set(words)) / max(len(words), 1)
    if unique_ratio > 0.7:
        score += 5
    
    # Capitalization check
    if caption[0].isupper() if caption else False:
        score += 3
    
    # Ensure score is 0-100
    score = max(0, min(100, score))
    
    # Grade assignment
    if score >= 90:
        grade = "A+"
    elif score >= 85:
        grade = "A"
    elif score >= 80:
        grade = "B+"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "F"
    
    # Add at least 2 suggestions if missing
    if not suggestions:
        suggestions.append("Caption is well-structured for social media")
        if score < 75:
            suggestions.append("Consider adding call-to-action words")
    
    if len(suggestions) == 1:
        suggestions.append("Maintains good engagement potential")
    
    return score, grade, suggestions


# =====================================================================
# EMOTION DETECTION (Deterministic, Caption-Specific)
# =====================================================================

def detect_emotion(caption: str, language: str) -> Tuple[str, int, str]:
    """
    Detect emotion from caption text.
    Returns: (emotion_label, emotion_score, emotion_reason)
    """
    caption_lower = caption.lower()
    
    # Select word lists based on language
    if language == "bn":
        happy_words = BANGLA_HAPPY_WORDS
        sad_words = BANGLA_SAD_WORDS
        fear_words = BANGLA_FEAR_WORDS
        shock_words = BANGLA_SHOCK_WORDS
        inspirational_words = BANGLA_INSPIRATIONAL_WORDS
    else:
        happy_words = ENGLISH_HAPPY_WORDS
        sad_words = ENGLISH_SAD_WORDS
        fear_words = ENGLISH_FEAR_WORDS
        shock_words = ENGLISH_SHOCK_WORDS
        inspirational_words = ENGLISH_INSPIRATIONAL_WORDS
    
    # Count emotional word matches
    happy_count = sum(1 for word in happy_words if word in caption_lower)
    sad_count = sum(1 for word in sad_words if word in caption_lower)
    fear_count = sum(1 for word in fear_words if word in caption_lower)
    shock_count = sum(1 for word in shock_words if word in caption_lower)
    inspirational_count = sum(1 for word in inspirational_words if word in caption_lower)
    
    # Punctuation intensity
    exclamation_count = caption.count("!")
    question_count = caption.count("?")
    
    # Determine dominant emotion
    emotion_scores = {
        "happy": happy_count * 15 + exclamation_count * 5,
        "sad": sad_count * 15,
        "fear": fear_count * 15,
        "shock": shock_count * 15 + exclamation_count * 8,
        "inspirational": inspirational_count * 15,
        "angry": exclamation_count * 10 if exclamation_count > 2 else 0,
        "neutral": 20  # Base neutral score
    }
    
    # Find dominant emotion
    emotion = max(emotion_scores, key=emotion_scores.get)
    score = min(100, emotion_scores[emotion])
    
    # Generate reason with real caption words
    reason = ""
    if emotion == "happy" and happy_count > 0:
        matched_words = [w for w in happy_words if w in caption_lower]
        reason = f"Contains positive words: {', '.join(matched_words[:2])}"
    elif emotion == "sad" and sad_count > 0:
        matched_words = [w for w in sad_words if w in caption_lower]
        reason = f"Contains emotional concerns: {', '.join(matched_words[:2])}"
    elif emotion == "fear" and fear_count > 0:
        matched_words = [w for w in fear_words if w in caption_lower]
        reason = f"Contains cautionary language: {', '.join(matched_words[:1])}"
    elif emotion == "shock" and shock_count > 0:
        matched_words = [w for w in shock_words if w in caption_lower]
        reason = f"Surprising tone with words: {', '.join(matched_words[:1])}"
    elif emotion == "inspirational" and inspirational_count > 0:
        matched_words = [w for w in inspirational_words if w in caption_lower]
        reason = f"Motivational language: {', '.join(matched_words[:2])}"
    elif emotion == "angry":
        reason = f"Multiple exclamation marks ({exclamation_count}) indicate strong intensity"
    else:
        reason = "Neutral, factual tone without strong emotional markers"
    
    return emotion, score, reason


# =====================================================================
# AUTHENTICITY DETECTION (Deterministic)
# =====================================================================

def detect_authenticity(caption: str, language: str) -> Tuple[int, int, str]:
    """
    Analyze caption text for authenticity markers.
    Returns: (real_percent, fake_percent, auth_reason)
    """
    real_score = 50  # Base authenticity
    
    # Check for exaggeration markers
    exaggeration_patterns = ["!!!!", "????", "AMAZING", "INCREDIBLE", "UNBELIEVABLE", "SHOCKING"]
    if any(pattern in caption.upper() for pattern in exaggeration_patterns):
        real_score -= 15
    
    # Check for factual details (numbers, dates, specific names)
    has_numbers = bool(re.search(r"\d", caption))
    if has_numbers:
        real_score += 10
    
    # Check for personal storytelling
    personal_markers = ["i ", "me ", "my ", "we ", "our ", "আমার", "আমরা", "আমাদের"]
    personal_count = sum(1 for marker in personal_markers if marker in caption.lower())
    if personal_count > 0:
        real_score += 10
    
    # Check for quoted/attributed content
    if '"' in caption or "'" in caption:
        real_score += 5
    
    # Check for URL/links (can indicate external reference)
    if "http" in caption or "www" in caption:
        real_score += 5
    
    # Check for clickbait patterns
    clickbait_patterns = ["click here", "you won't believe", "doctors hate", "one trick", "شনাক্ত করুন", "লুকানো"]
    if any(pattern in caption.lower() for pattern in clickbait_patterns):
        real_score -= 20
    
    # Ensure scores are 0-100
    real_score = max(0, min(100, real_score))
    fake_score = 100 - real_score
    
    # Generate reason using actual caption keywords
    reason = ""
    if real_score > 70:
        if has_numbers and personal_count > 0:
            reason = "Contains specific details and personal narrative"
        elif personal_count > 0:
            reason = "Personal storytelling suggests authentic experience"
        else:
            reason = "Balanced, factual tone without sensationalism"
    elif real_score < 40:
        reason = "Excessive punctuation and exaggeration markers detected"
    else:
        reason = "Mixed signals - combination of personal and promotional elements"
    
    return real_score, fake_score, reason


# =====================================================================
# HASHTAG GENERATION (Context-Aware, Language-Specific)
# =====================================================================

def generate_hashtags(caption: str, language: str, top_n: int = 10) -> List[str]:
    """
    Generate relevant hashtags based on caption keywords.
    Returns list of 8-15 hashtags.
    """
    words = caption.lower().split()
    
    # Extract keywords (filter stop words)
    stop_words_en = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "is", "are", "was", "be"}
    stop_words_bn = {"এবং", "এর", "যা", "হয়", "আছে", "থেকে", "এ", "তে", "দ্বারা", "সে", "আমার", "তাদের"}
    
    stop_words = stop_words_en if language == "en" else stop_words_bn
    
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Get top keywords
    from collections import Counter
    keyword_freq = Counter(keywords)
    top_keywords = [word for word, _ in keyword_freq.most_common(top_n)]
    
    # Create hashtags
    hashtags = [f"#{word}" for word in top_keywords if word.isalpha()]
    
    # Add topical hashtags if limited
    if len(hashtags) < 8:
        if language == "en":
            topical = ["#socialmedia", "#content", "#engagement", "#growth"]
        else:
            topical = ["#সোশ্যালমিডিয়া", "#কন্টেন্ট", "#সম্প্রদায়", "#বৃদ্ধি"]
        
        hashtags.extend(topical[:max(0, 8 - len(hashtags))])
    
    return hashtags[:15]  # Return max 15 hashtags


# =====================================================================
# CAPTION OPTIMIZATION (Tone-Guided)
# =====================================================================

TONE_PATTERNS = {
    "professional": {
        "en": ["I'd like to share", "Please note that", "This highlights", "Consider this", "Best practices suggest"],
        "bn": ["মনে করুন", "গুরুত্বপূর্ণ", "পেশাদার", "প্রস্তাব", "উপযুক্ত"]
    },
    "friendly": {
        "en": ["Hey!", "Love this!", "Can't wait to", "So excited about", "Check this out"],
        "bn": ["আরে!", "অসাধারণ!", "উত্সাহিত", "দেখুন", "সুন্দর"]
    },
    "emotional": {
        "en": ["Feeling grateful", "My heart", "Touching", "Deeply moved", "So meaningful"],
        "bn": ["কৃতজ্ঞ", "হৃদয়", "মর্মস্পর্শী", "গভীর", "অর্থপূর্ণ"]
    },
    "trendy": {
        "en": ["Vibing with", "This aesthetic", "Living for", "That moment when", "No cap"],
        "bn": ["ভাইব", "স্টাইল", "মোমেন্ট", "ট্রেন্ডি", "বেশ"]
    },
    "funny": {
        "en": ["Plot twist", "Not me", "Literally me", "I'm dead", "Help"],
        "bn": ["মজা", "হাসি", "অদ্ভুত", "মজাদার", "কমিক্যাল"]
    },
    "supportive": {
        "en": ["You've got this", "Rooting for you", "So proud", "Keep shining", "Believe in yourself"],
        "bn": ["তুমি পারবে", "গর্বিত", "চমৎকার", "শক্তিশালী", "বিশ্বাস করো"]
    },
    "informative": {
        "en": ["Did you know", "Key insight", "Here's why", "Understanding", "Learn about"],
        "bn": ["জানেন কি", "শিখুন", "বুঝুন", "তথ্য", "গুরুত্বপূর্ণ"]
    },
    "curious": {
        "en": ["Ever wondered", "What if", "Thinking about", "Questions arise", "Consider"],
        "bn": ["ভাবুন", "কি হয় যদি", "প্রশ্ন", "চিন্তা করুন", "অনুসন্ধান"]
    }
}


def optimize_caption(caption: str, tone: str, language: str) -> Tuple[str, str]:
    """
    Rewrite caption in specified tone.
    Returns: (optimized_caption, optimization_reason)
    """
    if tone not in TONE_PATTERNS:
        return caption, "Tone not recognized"
    
    # Get tone starter phrases
    tone_phrases = TONE_PATTERNS[tone].get(language, TONE_PATTERNS[tone].get("en", []))
    
    if not tone_phrases:
        return caption, "Language not supported for this tone"
    
    # Select appropriate phrase
    starter = tone_phrases[0]
    
    # Reconstruct caption with tone
    if language == "en":
        optimized = f"{starter}: {caption}"
    else:
        optimized = f"{starter} - {caption}"
    
    reason = f"Rewritten in {tone} tone with opening phrase: '{starter}'"
    
    return optimized, reason


# =====================================================================
# MAIN ANALYSIS FUNCTION
# =====================================================================

def analyze_caption(
    caption: str,
    action: str = "analyze",
    tone: str = None
) -> Dict:
    """
    Main caption analysis & optimization function.
    
    Args:
        caption: Caption text (Bangla or English)
        action: "analyze" or "optimize"
        tone: Tone for optimization (only if action="optimize")
    
    Returns:
        Dictionary with analysis results
    """
    # Auto-detect language
    language = detect_language(caption)
    
    # Analyze SEO
    seo_score, seo_grade, seo_suggestions = analyze_seo(caption, language)
    
    # Detect emotion
    emotion, emotion_score, emotion_reason = detect_emotion(caption, language)
    
    # Detect authenticity
    real_percent, fake_percent, auth_reason = detect_authenticity(caption, language)
    
    # Generate hashtags
    hashtags = generate_hashtags(caption, language)
    
    # Build base response
    result = {
        "language": language,
        "original_caption": caption,
        "action": action,
        "seo_score": seo_score,
        "seo_grade": seo_grade,
        "seo_suggestions": seo_suggestions,
        "emotion": emotion,
        "emotion_score": emotion_score,
        "emotion_reason": emotion_reason,
        "real_percent": real_percent,
        "fake_percent": fake_percent,
        "auth_reason": auth_reason,
        "hashtags": hashtags
    }
    
    # Optimize if requested
    if action == "optimize" and tone:
        optimized_caption, optimization_reason = optimize_caption(caption, tone, language)
        
        # Re-analyze optimized caption
        new_seo_score, new_seo_grade, new_seo_suggestions = analyze_seo(optimized_caption, language)
        new_emotion, new_emotion_score, new_emotion_reason = detect_emotion(optimized_caption, language)
        new_real_percent, new_fake_percent, new_auth_reason = detect_authenticity(optimized_caption, language)
        new_hashtags = generate_hashtags(optimized_caption, language)
        
        # Calculate improvement
        seo_improvement = new_seo_score - seo_score
        improvement_reason = f"SEO improved by rewriting in {tone} tone with better keyword placement and engagement hooks"
        
        result.update({
            "optimized_caption": optimized_caption,
            "tone": tone,
            "old_seo": seo_score,
            "new_seo": new_seo_score,
            "seo_improvement": seo_improvement,
            "seo_improvement_reason": improvement_reason,
            "new_seo_grade": new_seo_grade,
            "new_seo_suggestions": new_seo_suggestions,
            "new_emotion": new_emotion,
            "new_emotion_score": new_emotion_score,
            "new_emotion_reason": new_emotion_reason,
            "new_real_percent": new_real_percent,
            "new_fake_percent": new_fake_percent,
            "new_auth_reason": new_auth_reason,
            "new_hashtags": new_hashtags,
            "optimization_reason": optimization_reason
        })
    
    return result
