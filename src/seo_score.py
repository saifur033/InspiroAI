import re
from typing import Dict
from src.utils import detect_language
from collections import Counter

EN_STOPWORDS = set(["the","and","is","in","to","of","a","for","on","with","that","this","it","as","are","be","by","an","or","from","at","was","were","has","have","do","does","did","will","would","could","should","can","may","might","must","shall","how","what","when","where","why","which"]) 
BN_STOPWORDS = set(["এবং","কিন্তু","এটি","যে","থেকে","করে","হয়","না","জন্য","এই","আমি","আমরা","তুমি","আপনি","তিনি","তারা","হয়েছে","ছিল","আছে","হবে","হচ্ছে","যাবে","নিয়ে","দিয়ে","সাথে","মধ্যে","মতো","সব","কিছু"])


def compute_seo_score(caption: str) -> Dict:
    if not caption or not caption.strip():
        return {
            "score": 0,
            "grade": "F",
            "explanation": "Empty caption",
            "suggestions": ["Write a caption to optimize SEO"]
        }

    text = caption.strip()
    lang = detect_language(text)

    words = re.findall(r"[\w\u0980-\u09FF]+", text)
    word_count = len(words)
    char_count = len(text)
    
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    sentence_count = len(sentences)

    stopset = BN_STOPWORDS if lang == "bn" else EN_STOPWORDS
    content_words = [w.lower() for w in words if w.lower() not in stopset and len(w) > 3]
    
    kw_freq = Counter(content_words)
    top_keywords = kw_freq.most_common(5)
    keyword_density = (sum(count for _, count in top_keywords) / max(1, word_count)) * 100 if top_keywords else 0

    avg_word_length = sum(len(w) for w in words) / max(1, word_count)
    avg_words_per_sentence = word_count / max(1, sentence_count)

    emojis = re.findall(r"[\U0001F300-\U0001FAFF\u2764\uFE0F✨🌟💫🌸🔥☺️❤️😍🤩😇🌿🎉👍🙌💪]", text)
    emoji_count = len(emojis)

    hashtags = re.findall(r"#\w+", text)
    hashtag_count = len(hashtags)

    power_words = ["viral", "amazing", "incredible", "trending", "exclusive", "limited", "shocking", "breaking", "must", "new", "best", "premium", "ultimate", "revolutionary", "game-changing", "insane", "epic", "legendary"]
    power_word_count = sum(1 for pw in power_words if pw.lower() in text.lower())

    cta_keywords = ["follow", "share", "comment", "like", "subscribe", "click", "watch", "learn", "discover", "join", "explore", "check", "visit", "book", "download", "ফলো", "শেয়ার", "কমেন্ট", "দেখুন", "যোগ দিন"]
    has_cta = any(cta.lower() in text.lower() for cta in cta_keywords)

    pos_words = ["good", "great", "amazing", "awesome", "love", "happy", "excellent", "fantastic", "wonderful", "best", "perfect", "incredible", "superb"]
    positive_count = sum(1 for pw in pos_words if pw.lower() in text.lower())

    clarity_score = 0
    if 8 <= avg_words_per_sentence <= 18:
        clarity_score += 25
    elif 5 <= avg_words_per_sentence <= 22:
        clarity_score += 18
    else:
        clarity_score += 10

    keyword_score = min(25, keyword_density * 5)

    length_score = 0
    if 50 <= char_count <= 250:
        length_score = 20
    elif 30 <= char_count < 50 or 250 < char_count <= 350:
        length_score = 12
    elif char_count > 350:
        length_score = 8
    else:
        length_score = 4

    engagement_score = 0
    if emoji_count >= 2:
        engagement_score += 12
    elif emoji_count == 1:
        engagement_score += 6
    
    if 2 <= hashtag_count <= 6:
        engagement_score += 10
    elif hashtag_count > 6:
        engagement_score += 6
    
    engagement_score += min(15, power_word_count * 4)
    
    if has_cta:
        engagement_score += 10
    
    if positive_count >= 2:
        engagement_score += 8

    readability_score = min(10, content_words.__len__() / max(1, word_count) * 100 / 10)

    total_score = clarity_score + keyword_score + length_score + engagement_score + readability_score
    total_score = min(100, max(0, round(total_score)))

    if total_score >= 90:
        grade = "A+"
    elif total_score >= 80:
        grade = "A"
    elif total_score >= 70:
        grade = "B"
    elif total_score >= 60:
        grade = "C"
    elif total_score >= 50:
        grade = "D"
    else:
        grade = "F"

    suggestions = []
    if clarity_score < 15:
        suggestions.append("Optimize sentence structure for better readability")
    if keyword_score < 15:
        suggestions.append("Add more relevant keywords to improve SEO")
    if engagement_score < 20:
        suggestions.append("Add emojis, CTAs, or power words to boost engagement")
    if emoji_count == 0:
        suggestions.append("Include 2-3 strategic emojis for visual appeal")
    if not has_cta:
        suggestions.append("Add a clear call-to-action (follow, share, comment, etc)")
    if char_count < 30:
        suggestions.append("Expand caption length for better context")

    return {
        "score": total_score,
        "grade": grade,
        "explanation": f"Score based on clarity, keywords, length, engagement & readability",
        "suggestions": suggestions
    }
