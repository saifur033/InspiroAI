"""
master_caption_processor.py — Master Caption Processor v1.0
Advanced caption analysis & rewriting system with human-quality structured output

Features:
✔ Language auto-detect (Bangla ↔ English)
✔ Dynamic SEO scoring (0-100, caption-specific)
✔ Emotion detection with real word citations
✔ Authenticity analysis (Real % vs AI-Like %)
✔ Human-quality caption optimization (2 versions)
✔ Context-aware hashtag generation (12-20 tags)
✔ Reach & timing insights (dynamic, not fixed)
✔ Caption idea generation (5 short + 3 emotional/alert)
✔ Zero repetition, structured output, clean formatting
"""

import re
from typing import Dict, List, Tuple
from langdetect import detect
import json

# =====================================================================
# LANGUAGE DETECTION & UTILITIES
# =====================================================================

def detect_language(text: str) -> str:
    """Auto-detect language (bn/en)"""
    try:
        lang = detect(text)
        return "bn" if lang == "bn" else "en"
    except:
        # Fallback: check for Bangla characters
        if re.search(r"[\u0980-\u09FF]", text):
            return "bn"
        return "en"


def has_bangla(text: str) -> bool:
    """Check if text contains Bangla characters"""
    return bool(re.search(r"[\u0980-\u09FF]", text))


def count_sentences(text: str) -> int:
    """Count number of sentences"""
    return len(re.split(r'[।\.!?]+', text.strip()))


def extract_keywords(text: str, language: str, top_n: int = 10) -> List[str]:
    """Extract top keywords from caption"""
    words = text.lower().split()
    
    # Stop words
    stop_words_en = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "is", "are", "was", "be", "i", "you", "we", "it"}
    stop_words_bn = {"এবং", "এর", "যা", "হয়", "আছে", "থেকে", "এ", "তে", "দ্বারা", "সে", "আমার", "তাদের"}
    
    stop_words = stop_words_en if language == "en" else stop_words_bn
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Count frequency
    from collections import Counter
    freq = Counter(keywords)
    return [word for word, _ in freq.most_common(top_n)]


# =====================================================================
# 1. CAPTION ANALYSIS (SEO, Emotion, Authenticity)
# =====================================================================

def calculate_seo_score(caption: str, language: str) -> Tuple[int, List[str]]:
    """
    Calculate SEO score (0-100) based on:
    - Clarity & structure
    - Keywords & length
    - Readability & engagement signals
    """
    score = 50  # Base score
    suggestions = []
    
    # Length analysis (ideal: 50-250 chars)
    length = len(caption)
    if 50 <= length <= 250:
        score += 20
    elif length < 30:
        score -= 15
        suggestions.append("Caption too short - add more context")
    elif length > 300:
        score -= 10
        suggestions.append("Consider shortening for better readability")
    else:
        score += 10
    
    # Punctuation & clarity
    if "!" in caption or "?" in caption:
        score += 8
    
    # Repeated punctuation check (negative)
    if "!!!" in caption or "???" in caption:
        score -= 10
        suggestions.append("Avoid repeated punctuation (! ? .)")
    
    # Emoji presence
    if re.search(r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF]", caption):
        score += 10
    else:
        suggestions.append("Add 1-2 relevant emojis for engagement")
    
    # Capitalization check
    if caption and caption[0].isupper():
        score += 5
    
    # Keyword density
    words = caption.split()
    if len(set(words)) / max(len(words), 1) > 0.7:
        score += 5
    
    # Structure (line breaks improve readability)
    if "\n" in caption:
        score += 10
    else:
        suggestions.append("Use line breaks for better readability")
    
    # Engagement markers
    cta_words = ["please", "share", "comment", "like", "follow", "join", "priya", "upay", "deklte", "শেয়ার", "মন্তব্য", "যোগাযোগ"]
    if any(word.lower() in caption.lower() for word in cta_words):
        score += 8
    
    score = max(0, min(100, score))
    
    # Ensure at least 2 suggestions
    if not suggestions:
        suggestions.append("Caption has good structure and clarity")
    if len(suggestions) == 1:
        suggestions.append("Maintain consistent engagement tone")
    
    return score, suggestions[:4]  # Return top 4 suggestions


def detect_emotion_advanced(caption: str, language: str) -> Tuple[str, int, str]:
    """
    Detect emotion from caption with real word citations.
    Returns: (emotion, score, reason)
    """
    caption_lower = caption.lower()
    
    # Emotion keywords
    emotions = {
        "happy": {
            "bn": ["খুশি", "দুর্দান্ত", "অসাধারণ", "ভালো", "সুন্দর", "ভালোবাসি", "চমৎকার"],
            "en": ["love", "great", "amazing", "awesome", "wonderful", "excellent", "beautiful", "perfect"]
        },
        "sad": {
            "bn": ["দুঃখ", "কষ্ট", "দুর্ভাগ্য", "হতাশা", "ব্যর্থ", "ব্যথা", "চিন্তা"],
            "en": ["sad", "sorry", "hurt", "pain", "loss", "difficult", "hard", "struggle"]
        },
        "motivational": {
            "bn": ["স্বপ্ন", "সাহস", "লক্ষ্য", "শক্তি", "অর্জন", "এগিয়ে", "নতুন", "উন্নতি"],
            "en": ["dream", "courage", "goal", "strength", "achieve", "possible", "forward", "growth"]
        },
        "alert": {
            "bn": ["সাবধান", "ভয়", "বিপদ", "সংকট", "ঝুঁকি", "সতর্ক", "আবার", "জরুরী"],
            "en": ["alert", "danger", "warning", "urgent", "crisis", "risk", "careful", "beware"]
        },
        "excited": {
            "bn": ["উত্তেজিত", "আনন্দ", "রোমাঞ্চ", "বিস্ময়", "অবিশ্বাস্য", "দারুণ"],
            "en": ["excited", "thrilled", "amazing", "wow", "incredible", "awesome", "fantastic"]
        }
    }
    
    emotion_scores = {
        "happy": 0, "sad": 0, "emotional": 0, "motivational": 0,
        "alert": 0, "serious": 0, "excited": 0, "calm": 0, "fearful": 0
    }
    
    # Get keywords for language
    words_list = emotions.get(language, {})
    if not words_list:
        words_list = emotions
    
    # Count emotion word matches
    for emotion, word_dict in emotions.items():
        words = word_dict.get(language, word_dict.get("en", []))
        matched = [w for w in words if w.lower() in caption_lower]
        emotion_scores[emotion] = len(matched) * 15
    
    # Punctuation intensity
    exclamation = caption.count("!")
    question = caption.count("?")
    
    if exclamation > 2:
        emotion_scores["excited"] += exclamation * 5
        emotion_scores["alert"] += exclamation * 3
    
    if question > 1:
        emotion_scores["serious"] += 10
    
    # Find dominant emotion
    emotion = max(emotion_scores, key=emotion_scores.get)
    score = min(100, emotion_scores[emotion])
    
    # Generate reason with real words
    reason = ""
    emotion_words = emotions.get(emotion, {}).get(language, [])
    if emotion_words:
        matched = [w for w in emotion_words if w.lower() in caption_lower]
        if matched:
            reason = f"Words like '{matched[0]}' reflect {emotion} emotion"
        else:
            reason = f"Tone and structure suggest {emotion} emotion"
    
    return emotion, max(0, score), reason


def detect_authenticity(caption: str, language: str) -> Tuple[int, int, str]:
    """
    Analyze caption authenticity.
    Returns: (real_percent, ai_like_percent, reason)
    """
    real_score = 50  # Base authenticity
    
    # Check for exaggeration
    if "!!!!" in caption or "????" in caption:
        real_score -= 15
    
    # Numbers & specifics (human-like)
    if re.search(r"\d", caption):
        real_score += 15
    
    # Personal pronouns (human-like)
    personal_markers = ["i ", "me ", "my ", "we ", "our ", "আমার", "আমরা", "আমাদের", "আমি"]
    if sum(1 for m in personal_markers if m in caption.lower()) > 0:
        real_score += 12
    
    # Raw, short sentences (human-like)
    sentences = caption.split(".")
    if len(sentences) > 2 and any(len(s) < 15 for s in sentences):
        real_score += 8
    
    # Quoted content
    if '"' in caption or "'" in caption:
        real_score += 8
    
    # Clickbait patterns (AI-like)
    clickbait = ["click here", "you won't believe", "shocking", "doctors hate", "one trick"]
    if any(pattern in caption.lower() for pattern in clickbait):
        real_score -= 20
    
    real_score = max(0, min(100, real_score))
    ai_score = 100 - real_score
    
    # Reason
    if real_score > 70:
        reason = "Personal wording, specific details, human emotion"
    elif real_score < 40:
        reason = "Excessive punctuation, promotional tone, generic structure"
    else:
        reason = "Mix of authentic and crafted elements"
    
    return real_score, ai_score, reason


# =====================================================================
# 2. CAPTION OPTIMIZATION (Human-Quality Rewrites)
# =====================================================================

def optimize_caption(caption: str, language: str) -> Tuple[str, str]:
    """
    Generate 2 optimized versions: Professional & Social Friendly
    Returns: (version_a, version_b)
    """
    # Version A: Clean & Professional
    professional = caption.strip()
    
    # Clean repeated punctuation
    professional = re.sub(r'([!?.])\1+', r'\1', professional)
    
    # Add period if missing
    if professional and professional[-1] not in ".!?":
        professional += "."
    
    # Version B: Social Media Friendly
    social = professional
    
    # Keep short sentences separate
    sentences = re.split(r'(?<=[.!?])\s+', professional)
    social = "\n\n".join(sentences[:3]) if len(sentences) > 2 else professional
    
    # Add call-to-action if missing
    if "?" not in social:
        if language == "en":
            social += "\n\nWhat do you think? 💭"
        else:
            social += "\n\nআপনার মতামত কি? 💭"
    
    return professional, social


# =====================================================================
# 3. HASHTAG GENERATION (Context-Aware)
# =====================================================================

def generate_hashtags_advanced(caption: str, language: str, emotion: str, top_n: int = 15) -> List[str]:
    """
    Generate 12-20 relevant hashtags based on content, emotion, and language
    """
    keywords = extract_keywords(caption, language, 8)
    hashtags = [f"#{kw}" for kw in keywords if kw.isalpha()]
    
    # Emotion-based tags
    emotion_tags = {
        "happy": ["#Happiness", "#Positivity", "#Joy", "#Blessed"],
        "alert": ["#Alert", "#Breaking", "#Safety", "#Urgent"],
        "motivational": ["#Motivation", "#Inspiration", "#Goals", "#Growth"],
        "excited": ["#Excited", "#Amazing", "#Awesome", "#Thrilled"],
        "sad": ["#Support", "#Care", "#Hope", "#Together"]
    }
    
    if emotion in emotion_tags:
        hashtags.extend(emotion_tags[emotion])
    
    # Language-specific tags
    if language == "bn":
        hashtags.extend(["#বাংলা", "#ঢাকা", "#সংবাদ", "#কমিউনিটি"])
    else:
        hashtags.extend(["#Community", "#Trending", "#Important"])
    
    # Remove duplicates and limit
    hashtags = list(dict.fromkeys(hashtags))[:top_n]
    return hashtags


# =====================================================================
# 4. REACH & TIMING INSIGHTS (Dynamic)
# =====================================================================

def generate_reach_insights(caption: str, language: str, emotion: str) -> Dict:
    """
    Generate dynamic reach & timing insights based on caption type
    """
    insights = {}
    
    # Determine caption type
    is_alert = "alert" in emotion.lower() or "!" in caption
    is_short = len(caption) < 100
    has_personal = any(p in caption.lower() for p in ["i ", "me ", "my ", "আমার", "আমরা"])
    
    # Best posting times (dynamic based on type)
    if is_alert:
        insights["best_times"] = "10 AM - 12 PM or 6-9 PM (breaking news peak hours)"
        insights["engagement"] = "Very High (alert/breaking news content)"
        insights["audience"] = "Local users, news followers, safety-conscious pages"
    elif has_personal:
        insights["best_times"] = "Evening 6-9 PM or Weekend 10 AM-2 PM (personal engagement peak)"
        insights["engagement"] = "High (personal stories build connection)"
        insights["audience"] = "Friends, followers, community members"
    elif is_short:
        insights["best_times"] = "Lunch 12-1 PM or Evening 7-8 PM (quick-read peaks)"
        insights["engagement"] = "Medium-High (short form performs well)"
        insights["audience"] = "Casual scrollers, trending content followers"
    else:
        insights["best_times"] = "Morning 9-11 AM or Evening 7-9 PM (general audience active)"
        insights["engagement"] = "Medium (well-structured content)"
        insights["audience"] = "Engaged followers, content enthusiasts"
    
    # Format suggestion
    if "http" in caption or "link" in caption.lower():
        insights["format"] = "Link + Short Text (drive clicks)"
    elif len(caption) < 50:
        insights["format"] = "Text + Emoji (quick, punchy)"
    else:
        insights["format"] = "Photo/Video + Caption (visual engagement recommended)"
    
    insights["posting_frequency"] = "Best: Once daily for consistent reach"
    
    return insights


# =====================================================================
# 5. CAPTION IDEA GENERATION
# =====================================================================

def generate_caption_ideas(topic: str, language: str) -> Dict[str, List[str]]:
    """
    Generate caption ideas: 5 short + 3 emotional/alert
    """
    ideas = {
        "short": [],
        "emotional_alert": []
    }
    
    if language == "bn":
        ideas["short"] = [
            f"আজ আমাদের বিশেষ দিন। {topic}",
            f"{topic} সত্যিই অসাধারণ! 🌟",
            f"প্রতিটি মুহূর্ত মূল্যবান। {topic} 💫",
            f"{topic} এর মাধ্যমে নতুন শিখলাম।",
            f"ভালোবাসি এই সময়কে। {topic} ✨"
        ]
        
        ideas["emotional_alert"] = [
            f"⚠️ জরুরী: {topic} সবার জানা দরকার!",
            f"💔 দুর্ভাগ্যবশত {topic} ঘটেছে। সবাই সাবধান থাকুন।",
            f"🆘 এটি গুরুত্বপূর্ণ! {topic} সম্পর্কে সচেতন থাকুন।"
        ]
    else:
        ideas["short"] = [
            f"Amazing day today with {topic}!",
            f"{topic} is absolutely incredible 🌟",
            f"Every moment matters with {topic} 💫",
            f"Learned something new about {topic}",
            f"Love this time with {topic} ✨"
        ]
        
        ideas["emotional_alert"] = [
            f"⚠️ Alert: {topic} - Everyone needs to know!",
            f"💔 Sad news about {topic} - Stay careful!",
            f"🆘 Important: {topic} - Be aware and informed!"
        ]
    
    return ideas


# =====================================================================
# MAIN MASTER PROCESSOR
# =====================================================================

def process_master_caption(
    caption: str,
    generate_ideas: bool = False,
    topic_for_ideas: str = ""
) -> Dict:
    """
    Main processor: Analyzes caption and returns complete structured output
    
    Args:
        caption: User's caption text
        generate_ideas: Whether to generate caption ideas
        topic_for_ideas: Topic for idea generation
    
    Returns:
        Complete analysis dictionary with all sections
    """
    language = detect_language(caption)
    
    # 1. Caption Analysis
    seo_score, seo_suggestions = calculate_seo_score(caption, language)
    emotion, emotion_score, emotion_reason = detect_emotion_advanced(caption, language)
    real_pct, ai_pct, auth_reason = detect_authenticity(caption, language)
    
    # 2. Optimized Captions
    version_a, version_b = optimize_caption(caption, language)
    
    # 3. Hashtags
    hashtags = generate_hashtags_advanced(caption, language, emotion)
    
    # 4. Reach Insights
    reach_insights = generate_reach_insights(caption, language, emotion)
    
    # 5. Caption Ideas (optional)
    caption_ideas = None
    if generate_ideas and topic_for_ideas:
        caption_ideas = generate_caption_ideas(topic_for_ideas, language)
    
    # Build result
    result = {
        "language": language,
        "original_caption": caption,
        "analysis": {
            "seo_score": seo_score,
            "seo_improvements": seo_suggestions,
            "emotion": emotion,
            "emotion_score": emotion_score,
            "emotion_reason": emotion_reason,
            "authenticity": {
                "real_percent": real_pct,
                "ai_like_percent": ai_pct,
                "reason": auth_reason
            }
        },
        "optimized_captions": {
            "version_a_professional": version_a,
            "version_b_social_friendly": version_b
        },
        "hashtags": hashtags,
        "reach_insights": reach_insights
    }
    
    if caption_ideas:
        result["caption_ideas"] = caption_ideas
    
    return result


# =====================================================================
# FORMATTING FOR DISPLAY
# =====================================================================

def format_output_for_display(result: Dict, language: str) -> str:
    """
    Format master processor result for clean display
    """
    section_sep = "\n" + "="*60 + "\n"
    
    output = []
    
    if language == "bn":
        output.append("📊 ক্যাপশন বিশ্লেষণ")
        output.append(section_sep)
        output.append(f"SEO স্কোর: {result['analysis']['seo_score']}/100")
        output.append("\nSEO উন্নতি:")
        for suggestion in result['analysis']['seo_improvements']:
            output.append(f"  • {suggestion}")
        output.append(f"\nসনাক্ত আবেগ: {result['analysis']['emotion']}")
        output.append(f"আবেগ কারণ: {result['analysis']['emotion_reason']}")
        output.append(f"\nসত্যতা: {result['analysis']['authenticity']['real_percent']}% বাস্তব, {result['analysis']['authenticity']['ai_like_percent']}% AI-এর মতো")
        output.append(f"কারণ: {result['analysis']['authenticity']['reason']}")
        
        output.append(section_sep)
        output.append("📝 অপ্টিমাইজড ক্যাপশন")
        output.append(section_sep)
        output.append(f"সংস্করণ A (পেশাদার):\n{result['optimized_captions']['version_a_professional']}")
        output.append(f"\nসংস্করণ B (সোশ্যাল মিডিয়া বান্ধব):\n{result['optimized_captions']['version_b_social_friendly']}")
        
        output.append(section_sep)
        output.append("#️⃣ হ্যাশট্যাগ")
        output.append(section_sep)
        output.append(" ".join(result['hashtags']))
        
        output.append(section_sep)
        output.append("📈 পৌঁছানোর অন্তর্দৃষ্টি")
        output.append(section_sep)
        for key, value in result['reach_insights'].items():
            output.append(f"{key.replace('_', ' ').title()}: {value}")
    
    else:
        output.append("📊 Caption Analysis")
        output.append(section_sep)
        output.append(f"SEO Score: {result['analysis']['seo_score']}/100")
        output.append("\nSEO Improvements:")
        for suggestion in result['analysis']['seo_improvements']:
            output.append(f"  • {suggestion}")
        output.append(f"\nEmotion Detected: {result['analysis']['emotion']}")
        output.append(f"Emotion Reason: {result['analysis']['emotion_reason']}")
        output.append(f"\nAuthenticity: {result['analysis']['authenticity']['real_percent']}% Real, {result['analysis']['authenticity']['ai_like_percent']}% AI-Like")
        output.append(f"Reason: {result['analysis']['authenticity']['reason']}")
        
        output.append(section_sep)
        output.append("📝 Optimized Captions")
        output.append(section_sep)
        output.append(f"Version A (Professional):\n{result['optimized_captions']['version_a_professional']}")
        output.append(f"\nVersion B (Social Media Friendly):\n{result['optimized_captions']['version_b_social_friendly']}")
        
        output.append(section_sep)
        output.append("#️⃣ Hashtags")
        output.append(section_sep)
        output.append(" ".join(result['hashtags']))
        
        output.append(section_sep)
        output.append("📈 Reach Insights")
        output.append(section_sep)
        for key, value in result['reach_insights'].items():
            output.append(f"{key.replace('_', ' ').title()}: {value}")
    
    return "\n".join(output)
