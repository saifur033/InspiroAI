import re
from typing import Dict
from textblob import TextBlob

EMOTION_KEYWORDS = {
    "positive": ["joy", "happy", "smile", "love", "awesome", "great", "wonderful", "fantastic", "amazing", "excellent", "perfect", "beautiful", "gorgeous", "lovely", "blessed", "grateful", "thankful", "thrilled", "delighted", "খুশি", "ভালো", "আনন্দ", "হাসি", "উত্তেজিত", "অসাধারণ"],
    "sad": ["cry", "hurt", "pain", "alone", "broken", "grief", "loss", "tears", "sad", "depressed", "unhappy", "miserable", "heartbreak", "heartbroken", "devastated", "gloomy", "sorrowful", "weep", "দুঃখ", "কান্না", "মনখারাপ", "একাকী", "কষ্ট", "ভাঙা"],
    "angry": ["angry", "mad", "furious", "rage", "hate", "annoyed", "irritated", "livid", "outraged", "pissed", "furious", "irate", "enraged", "resentment", "রাগ", "ক্ষোভ", "বিরক্ত", "অসহ্য"],
    "excited": ["excited", "thrilled", "energetic", "amazing", "wow", "incredible", "stoked", "hyped", "pumped", "exhilarated", "ecstatic", "elated", "uproar", "উত্তেজিত", "মজা", "দারুণ"],
    "motivational": ["inspire", "motivate", "achieve", "goal", "dream", "success", "believe", "powerful", "unstoppable", "champion", "determined", "focused", "প্রেরণা", "উদ্দীপক", "সাফল্য"],
    "romantic": ["love", "romance", "heart", "kiss", "passion", "darling", "sweetheart", "romantic", "adore", "cherish", "beloved", "sweetheart", "ভালোবাসা", "প্রেম", "হৃদয়"],
    "sarcastic": ["yeah right", "sure", "obviously", "totally", "as if", "whatever", "lol", "right", "সত্যিই", "অবশ্যই"],
    "neutral": ["the", "is", "and", "or", "এবং", "কিন্তু"]
}

def detect_language(text: str) -> str:
    bn = sum(1 for ch in text if 2432 <= ord(ch) <= 2559)
    en = sum(1 for ch in text if ch.isascii())
    return "bn" if bn > en else "en"

def normalize_text(text: str) -> str:
    clean = re.sub(r"[^\w\s\u0980-\u09FF]", "", text)
    clean = clean.replace("\n", " ")
    return clean.lower().strip()

def detect_emotion(text: str) -> Dict:
    """
    Detect emotion with caption-dependent analysis.
    Returns: {
        "emotion": "HAPPY|SAD|ANGRY|NEUTRAL|EXCITED|CALM",
        "top_emotion": same as emotion,
        "confidence": 0-100 int,
        "reason": detailed caption-based reasoning,
        "distribution": dict (optional)
    }
    """
    if not text or not text.strip():
        return {
            "emotion": "NEUTRAL",
            "top_emotion": "NEUTRAL",
            "confidence": 100,
            "reason": "No content to analyze",
            "distribution": {"NEUTRAL": 100.0}
        }

    text_normalized = normalize_text(text)
    text_original = text.strip()
    scores = {emotion: 0 for emotion in EMOTION_KEYWORDS}

    # Keyword matching with tracking
    matched_keywords = {emotion: [] for emotion in EMOTION_KEYWORDS}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_normalized:
                scores[emotion] += 2
                matched_keywords[emotion].append(keyword)

    sentiment_obj = TextBlob(text)
    polarity = float(getattr(sentiment_obj, "polarity", 0.0))
    subjectivity = float(getattr(sentiment_obj, "subjectivity", 0.0))

    if polarity > 0.5:
        scores["positive"] += 5
        scores["excited"] += 3
    elif polarity < -0.5:
        scores["sad"] += 5
        scores["angry"] += 3
    else:
        scores["neutral"] += 2
    
    if subjectivity > 0.7:
        scores["emotional"] = scores.get("emotional", 0) + 3

    total = sum(scores.values())
    
    if total > 0:
        distribution = {emotion: (score / total) * 100 for emotion, score in scores.items()}
    else:
        distribution = {emotion: 0.0 for emotion in scores}
        distribution["neutral"] = 100.0

    top_emotion_raw = max(distribution.items(), key=lambda x: x[1])[0]
    confidence = int(round(distribution[top_emotion_raw]))
    confidence = max(0, min(100, confidence))

    # Map to standard emotion labels
    emotion_mapping = {
        "positive": "HAPPY",
        "sad": "SAD",
        "angry": "ANGRY",
        "excited": "EXCITED",
        "motivational": "EXCITED",
        "romantic": "HAPPY",
        "sarcastic": "NEUTRAL",
        "neutral": "NEUTRAL"
    }
    
    top_emotion = emotion_mapping.get(top_emotion_raw, "NEUTRAL").upper()

    # Generate caption-dependent reasoning
    reason = _generate_emotion_reason(text_original, top_emotion, polarity, subjectivity, matched_keywords.get(top_emotion_raw, []))

    return {
        "emotion": top_emotion,
        "top_emotion": top_emotion,
        "confidence": confidence,
        "reason": reason,
        "distribution": distribution
    }

def _generate_emotion_reason(caption: str, emotion: str, polarity: float, subjectivity: float, matched_keywords: list) -> str:
    """
    Generate caption-dependent reasoning for detected emotion.
    CRITICAL: Must extract and mention specific words from caption - NOT GENERIC!
    """
    # Detect language
    lang = detect_language(caption)
    is_bangla = lang == "bn"
    
    # Extract key topic words from caption (4+ chars, meaningful)
    stop_words = {'that', 'this', 'with', 'from', 'about', 'have', 'been', 'their', 'they', 'would', 'which', 'these', 'those', 'your', 'your', 'what', 'your'}
    caption_lower = caption.lower()
    words = [w for w in re.findall(r'\b\w+\b', caption_lower) if len(w) >= 4 and w not in stop_words]
    key_words = list(dict.fromkeys(words))[:3]  # Top 3 unique words
    topic_phrase = ' '.join(key_words[:2]) if len(key_words) >= 2 else (key_words[0] if key_words else 'content')
    
    # Build caption-specific reasoning using actual words from caption
    if is_bangla:
        emotion_reasons = {
            "HAPPY": f"'{topic_phrase}' সম্পর্কে ইতিবাচক অনুভূতি প্রকাশিত। এখানে আনন্দময় এবং উৎসাহী মনোভাব রয়েছে। সেন্টিমেন্ট স্কোর: {polarity:.2f}।",
            "SAD": f"'{topic_phrase}' সম্পর্কে দুঃখ এবং কষ্ট প্রকাশিত। গভীর নেতিবাচক অনুভূতি রয়েছে। সেন্টিমেন্ট স্কোর: {polarity:.2f}।",
            "ANGRY": f"'{topic_phrase}' সম্পর্কে রাগ এবং বিরক্তি প্রকাশিত। তীব্র নেতিবাচক অনুভূতি রয়েছে। সেন্টিমেন্ট স্কোর: {polarity:.2f}।",
            "EXCITED": f"'{topic_phrase}' সম্পর্কে উত্তেজনা এবং উৎসাহ প্রকাশিত। শক্তিশালী ইতিবাচক অনুভূতি রয়েছে। সেন্টিমেন্ট স্কোর: {polarity:.2f}।",
            "CALM": f"'{topic_phrase}' সম্পর্কে শান্ত এবং সংযত মনোভাব রয়েছে। পরিমাপিত এবং পেশাদার ভাষা ব্যবহৃত হয়েছে।",
            "NEUTRAL": f"'{topic_phrase}' সম্পর্কে বর্ণনামূলক এবং নিরপেক্ষ অনুভূতি। কোনো শক্তিশালী আবেগ প্রকাশিত নয়।"
        }
    else:
        emotion_reasons = {
            "HAPPY": f"About '{topic_phrase}': Positive and joyful sentiment expressed. Enthusiastic tone throughout. Sentiment: {polarity:.2f}.",
            "SAD": f"About '{topic_phrase}': Sadness and melancholy are conveyed. Deep emotional distress expressed. Sentiment: {polarity:.2f}.",
            "ANGRY": f"About '{topic_phrase}': Anger and frustration clearly evident. Strong negative emotion. Sentiment: {polarity:.2f}.",
            "EXCITED": f"About '{topic_phrase}': High energy and excitement expressed. Enthusiastic and positive tone. Sentiment: {polarity:.2f}.",
            "CALM": f"About '{topic_phrase}': Calm and composed tone maintained. Measured and professional language used.",
            "NEUTRAL": f"About '{topic_phrase}': Descriptive and neutral sentiment. No strong emotional indicators detected."
        }
    
    return emotion_reasons.get(emotion, "Emotion detected based on caption content.")


def optimize_emotion(emotion_data: Dict, tone: str) -> Dict:
    dist = emotion_data.get("distribution", {}).copy()
    for k in EMOTION_KEYWORDS.keys():
        dist.setdefault(k, 0)

    tone_map = {
        "friendly": {"positive": 15, "excited": 8},
        "professional": {"neutral": 12},
        "emotional": {"positive": 10, "sad": 5},
        "funny": {"excited": 15},
        "supportive": {"positive": 12, "motivational": 8},
    }

    tone_adjustments = tone_map.get(tone, {})
    for emotion, boost in tone_adjustments.items():
        dist[emotion] = dist.get(emotion, 0) + boost

    total = sum(dist.values())
    if total > 0:
        for k in dist:
            dist[k] = round((dist[k] / total) * 100, 1)
    else:
        dist["neutral"] = 100.0

    top = max((k, v) for k, v in dist.items() if k != "neutral") if any(v > 0 for k, v in dist.items() if k != "neutral") else ("neutral", 100.0)
    top_emotion = top[0]

    reason_map = {
        "positive": "Tone optimized to positive energy",
        "excited": "Tone optimized to excitement",
        "neutral": "Tone optimized to professionalism",
        "friendly": "Tone optimized to friendliness"
    }

    return {
        "emotion": top_emotion,
        "top_emotion": top_emotion,
        "distribution": dist,
        "reason": reason_map.get(top_emotion, f"Optimized {top_emotion}")
    }
