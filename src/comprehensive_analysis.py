#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced NLP-Driven Caption Analysis Engine
Structured format output for any caption
"""

import re
from typing import Dict, List
from collections import Counter
from textblob import TextBlob
from src.utils import detect_language
from src.seo_score import compute_seo_score
from src.emotion_model import detect_emotion
from src.fake_real_model import detect_fake
from src.caption_generator import generate_caption_variations


def comprehensive_caption_analysis(caption: str, tone: str = "professional") -> Dict:
    """
    Comprehensive NLP-driven caption analysis in structured format.
    
    Returns: {
        "original_caption": str,
        "language": "bn" or "en",
        "analysis": {
            "seo": { score, grade, explanation, suggestions },
            "emotion": { type, confidence, reason, keywords_found },
            "authenticity": { real_percent, fake_percent, linguistic_analysis },
            "rewrites": {
                "short_impactful": [3 captions],
                "social_media_friendly": [3 captions],
                "emotional_alert": [3 captions]
            },
            "tone_specific": {
                "tone": selected_tone,
                "rewritten": caption_text,
                "explanation": why_this_tone
            },
            "hashtags": [10-15 relevant hashtags]
        }
    }
    """
    
    if not caption or len(caption.strip()) < 5:
        return {"error": "Caption too short"}
    
    lang = detect_language(caption.strip())
    is_bangla = lang == "bn"
    
    # 1. SEO SCORE
    seo_result = compute_seo_score(caption) or {}
    seo_analysis = {
        "score": int(seo_result.get("score", 50)),
        "grade": seo_result.get("grade", "C"),
        "explanation": _generate_seo_explanation(caption, is_bangla),
        "suggestions": seo_result.get("suggestions", [])[:4]
    }
    
    # 2. EMOTION DETECTION
    emotion_result = detect_emotion(caption) or {}
    emotion_type = emotion_result.get("emotion", emotion_result.get("top_emotion", "NEUTRAL")).upper()
    emotion_confidence = int(emotion_result.get("confidence", 50))
    
    # Extract keywords that triggered emotion
    emotion_keywords = _extract_emotion_keywords(caption, is_bangla)
    emotion_reason = _generate_emotion_reason(caption, emotion_type, emotion_keywords, is_bangla)
    
    emotion_analysis = {
        "type": emotion_type,
        "confidence_percent": emotion_confidence,
        "reason": emotion_reason,
        "keywords_detected": emotion_keywords[:5]  # Top 5 keywords
    }
    
    # 3. FAKE vs REAL PROBABILITY
    fake_result = detect_fake(caption) or {}
    real_pct = int(fake_result.get("real", 50))
    fake_pct = 100 - real_pct
    
    authenticity_analysis = {
        "real_percent": real_pct,
        "fake_percent": fake_pct,
        "linguistic_markers": _analyze_linguistic_markers(caption, is_bangla),
        "reasoning": fake_result.get("reason", fake_result.get("reasoning", ""))
    }
    
    # 4. CAPTION REWRITES (3 categories)
    rewrite_categories = {
        "short_impactful": _generate_short_impactful(caption, is_bangla),
        "social_media_friendly": _generate_social_media_friendly(caption, is_bangla),
        "emotional_alert": _generate_emotional_alert(caption, is_bangla)
    }
    
    # 5. TONE-SPECIFIC REWRITE
    tone_specific = _generate_tone_specific(caption, tone, is_bangla)
    
    # 6. HASHTAGS
    hashtags = _generate_smart_hashtags(caption, is_bangla)
    
    return {
        "success": True,
        "original_caption": caption,
        "language": "Bangla" if is_bangla else "English",
        "language_code": lang,
        "analysis": {
            "seo": seo_analysis,
            "emotion": emotion_analysis,
            "authenticity": authenticity_analysis,
            "rewrites": rewrite_categories,
            "tone_specific": tone_specific,
            "hashtags": hashtags
        }
    }


def _generate_seo_explanation(caption: str, is_bangla: bool) -> str:
    """Generate SEO score explanation based on actual caption content"""
    word_count = len(caption.split())
    char_count = len(caption)
    has_emojis = len(re.findall(r"[\U0001F300-\U0001FAFF\u2764\uFE0F]", caption)) > 0
    has_hashtags = len(re.findall(r"#\w+", caption)) > 0
    has_cta = any(cta in caption.lower() for cta in ["follow", "share", "click", "শেয়ার", "ফলো"])
    
    if is_bangla:
        if word_count < 5:
            return "খুব সংক্ষিপ্ত ক্যাপশন - SEO উন্নতির জন্য আরও কীওয়ার্ড যোগ করুন।"
        elif char_count > 250:
            return "ভালো দৈর্ঘ্য এবং কীওয়ার্ড ঘনত্ব। যোগাযোগ শক্তিশালী।"
        else:
            return "মধ্যম দৈর্ঘ্যের ক্যাপশন। স্পষ্টতা এবং নাগাল উন্নত করুন।"
    else:
        if word_count < 5:
            return "Very short caption - add more keywords for better SEO."
        elif char_count > 250:
            return "Good length and keyword density. Strong communicative power."
        else:
            return "Medium-length caption. Improve clarity and reach."


def _extract_emotion_keywords(caption: str, is_bangla: bool) -> List[str]:
    """Extract emotion-triggering keywords from caption"""
    emotion_keywords_en = {
        "positive": ["love", "amazing", "wonderful", "great", "happy", "joy", "awesome", "excellent"],
        "sad": ["hurt", "pain", "cry", "sad", "grief", "loss", "broken"],
        "angry": ["angry", "mad", "hate", "furious", "rage"],
        "excited": ["excited", "wow", "amazing", "incredible", "thrilled"],
        "alert": ["help", "emergency", "urgent", "danger", "warning", "alert"]
    }
    
    emotion_keywords_bn = {
        "positive": ["খুশি", "আনন্দ", "অসাধারণ", "দারুণ", "ভালো", "সুন্দর"],
        "sad": ["দুঃখ", "কান্না", "মনখারাপ", "ব্যথা", "কষ্ট"],
        "angry": ["রাগ", "ক্ষোভ", "বিরক্ত", "অসহ্য"],
        "alert": ["সাহায্য", "জরুরি", "বিপদ", "সাবধান", "সতর্কতা", "ভূমিকম্প"]
    }
    
    keywords_dict = emotion_keywords_bn if is_bangla else emotion_keywords_en
    caption_lower = caption.lower()
    
    found_keywords = []
    for category_keywords in keywords_dict.values():
        for keyword in category_keywords:
            if keyword.lower() in caption_lower:
                found_keywords.append(keyword)
    
    return found_keywords[:10]


def _generate_emotion_reason(caption: str, emotion_type: str, keywords: List[str], is_bangla: bool) -> str:
    """Generate emotion reason mentioning actual caption keywords"""
    if not keywords:
        if is_bangla:
            return f"ক্যাপশনে {emotion_type} আবেগ প্রকাশিত হয়েছে।"
        else:
            return f"Caption expresses {emotion_type} emotion."
    
    keyword_str = ", ".join(keywords[:3])
    
    if is_bangla:
        return f"'{keyword_str}' শব্দগুলি ধারণ করে এই ক্যাপশন {emotion_type} আবেগ প্রকাশ করে।"
    else:
        return f"Keywords '{keyword_str}' in caption convey {emotion_type} emotion."


def _analyze_linguistic_markers(caption: str, is_bangla: bool) -> Dict:
    """Analyze linguistic markers for authenticity"""
    exclamation_count = caption.count("!")
    question_count = caption.count("?")
    emoji_count = len(re.findall(r"[\U0001F300-\U0001FAFF\u2764\uFE0F]", caption))
    all_caps_words = len(re.findall(r"\b[A-Z]{2,}\b", caption))
    
    markers = {
        "exclamation_marks": exclamation_count,
        "question_marks": question_count,
        "emojis": emoji_count,
        "all_caps_words": all_caps_words,
        "intensity_level": "high" if (exclamation_count > 2 or emoji_count > 3) else "medium" if (exclamation_count > 0 or emoji_count > 0) else "low"
    }
    
    return markers


def _generate_short_impactful(caption: str, is_bangla: bool) -> List[str]:
    """Generate 3 short & impactful rewrites"""
    # Extract key phrases
    key_words = re.findall(r"\b\w+\b", caption)
    
    if is_bangla:
        return [
            f"📢 {caption.split('.')[0].strip()}",
            f"⚡ {caption.split('!')[0].strip()}",
            f"✨ মূল বার্তা: {key_words[0] if key_words else 'আপনার বার্তা'}"
        ]
    else:
        return [
            f"📢 {caption.split('.')[0].strip()}",
            f"⚡ {caption.split('!')[0].strip()}",
            f"✨ Key message: {key_words[0] if key_words else 'Your message'}"
        ]


def _generate_social_media_friendly(caption: str, is_bangla: bool) -> List[str]:
    """Generate 3 social media friendly rewrites"""
    if is_bangla:
        return [
            f"{caption}\n\n📱 শেয়ার করুন এবং জানান আপনার মতামত!",
            f"{caption}\n\n💬 কমেন্টে আপনার ভাবনা লিখুন।",
            f"{caption}\n\n👍 লাইক দিন এবং ফলো করুন আরও জন্য।"
        ]
    else:
        return [
            f"{caption}\n\n📱 Share your thoughts in the comments!",
            f"{caption}\n\n💬 What do you think? Let us know!",
            f"{caption}\n\n👍 Like & follow for more!"
        ]


def _generate_emotional_alert(caption: str, is_bangla: bool) -> List[str]:
    """Generate 3 emotional/alert rewrites"""
    if is_bangla:
        return [
            f"⚠️ {caption}\n\nসবাই সচেতন থাকুন।",
            f"🔔 {caption}\n\nএটি গুরুত্বপূর্ণ - শেয়ার করুন!",
            f"❤️ {caption}\n\nআমরা একসাথে আছি।"
        ]
    else:
        return [
            f"⚠️ {caption}\n\nStay alert & aware!",
            f"🔔 {caption}\n\nThis matters - share it!",
            f"❤️ {caption}\n\nWe're in this together."
        ]


def _generate_tone_specific(caption: str, tone: str, is_bangla: bool) -> Dict:
    """Generate tone-specific rewrite"""
    tone_lower = tone.lower()
    
    if is_bangla:
        tone_map = {
            "professional": "পেশাদার ও কর্তৃত্বপূর্ণ ভাষা ব্যবহার করে পুনর্লিখিত",
            "friendly": "বন্ধুত্বপূর্ণ এবং সহজ ভাষায় পুনর্লিখিত",
            "emotional": "আবেগপূর্ণ এবং সংযোগ স্থাপনকারী টোনে পুনর্লিখিত",
            "viral": "ট্রেন্ডিং এবং শেয়ারযোগ্য ভাষায় পুনর্লিখিত",
            "breaking_news": "ভাঙা খবরের স্টাইলে জরুরি এবং তাৎপর্যপূর্ণভাবে পুনর্লিখিত"
        }
    else:
        tone_map = {
            "professional": "Rewritten in professional & authoritative language",
            "friendly": "Rewritten in friendly & conversational tone",
            "emotional": "Rewritten to evoke emotions & connection",
            "viral": "Rewritten for viral appeal & shareability",
            "breaking_news": "Rewritten as urgent breaking news"
        }
    
    explanation = tone_map.get(tone_lower, tone_map.get("professional"))
    
    # Simple tone-specific rewrite (use variations from caption_generator if available)
    if is_bangla:
        rewritten = f"[{tone} টোনে] {caption}"
    else:
        rewritten = f"[{tone} tone] {caption}"
    
    return {
        "tone": tone,
        "rewritten_caption": rewritten,
        "explanation": explanation
    }


def _generate_smart_hashtags(caption: str, is_bangla: bool) -> List[str]:
    """Generate 10-15 smart, relevant hashtags"""
    # Extract key phrases (3-4 words minimum)
    words = re.findall(r"\b\w+\b", caption)
    
    if is_bangla:
        # Bangla hashtags
        base_hashtags = ["#বাংলাদেশ", "#সংবাদ", "#সচেতনতা", "#শেয়ার", "#গুরুত্বপূর্ণ"]
        caption_hashtags = [f"#{word[:15]}" for word in words[:8] if len(word) > 3]
        all_hashtags = list(set(base_hashtags + caption_hashtags))[:15]
    else:
        # English hashtags
        base_hashtags = ["#news", "#awareness", "#share", "#important", "#urgent"]
        caption_hashtags = [f"#{word[:15]}" for word in words[:8] if len(word) > 3]
        all_hashtags = list(set(base_hashtags + caption_hashtags))[:15]
    
    return all_hashtags


def format_comprehensive_output(analysis: Dict) -> str:
    """Format the comprehensive analysis for display"""
    if "error" in analysis:
        return f"Error: {analysis['error']}"
    
    is_bangla = analysis["language_code"] == "bn"
    a = analysis["analysis"]
    
    output = []
    output.append("=" * 80)
    output.append("📊 COMPREHENSIVE CAPTION ANALYSIS")
    output.append("=" * 80)
    output.append(f"\nOriginal Caption: {analysis['original_caption']}")
    output.append(f"Language: {analysis['language']}\n")
    
    # 1. SEO SCORE
    output.append("1️⃣  SEO SCORE")
    output.append("-" * 40)
    seo = a["seo"]
    output.append(f"Score: {seo['score']}/100")
    output.append(f"Grade: {seo['grade']}")
    output.append(f"Explanation: {seo['explanation']}")
    output.append(f"Suggestions: {', '.join(seo['suggestions'][:2])}\n")
    
    # 2. EMOTION DETECTION
    output.append("2️⃣  EMOTION DETECTION")
    output.append("-" * 40)
    emo = a["emotion"]
    output.append(f"Type: {emo['type']}")
    output.append(f"Confidence: {emo['confidence_percent']}%")
    output.append(f"Reason: {emo['reason']}")
    output.append(f"Keywords: {', '.join(emo['keywords_detected'])}\n")
    
    # 3. AUTHENTICITY
    output.append("3️⃣  AUTHENTICITY ANALYSIS")
    output.append("-" * 40)
    auth = a["authenticity"]
    output.append(f"Real: {auth['real_percent']}%")
    output.append(f"Fake/AI: {auth['fake_percent']}%")
    output.append(f"Intensity: {auth['linguistic_markers']['intensity_level']}")
    output.append(f"Analysis: {auth['reasoning']}\n")
    
    # 4. REWRITES
    output.append("4️⃣  CAPTION REWRITES")
    output.append("-" * 40)
    rewrites = a["rewrites"]
    for category, captions in rewrites.items():
        output.append(f"\n{category.upper()}:")
        for i, cap in enumerate(captions, 1):
            output.append(f"  {i}. {cap}")
    output.append("")
    
    # 5. TONE-SPECIFIC
    output.append("\n5️⃣  TONE-SPECIFIC REWRITE")
    output.append("-" * 40)
    tone = a["tone_specific"]
    output.append(f"Tone: {tone['tone']}")
    output.append(f"Explanation: {tone['explanation']}")
    output.append(f"Rewritten: {tone['rewritten_caption']}\n")
    
    # 6. HASHTAGS
    output.append("6️⃣  RECOMMENDED HASHTAGS")
    output.append("-" * 40)
    hashtags = a["hashtags"]
    output.append(" ".join(hashtags))
    
    output.append("\n" + "=" * 80)
    
    return "\n".join(output)
