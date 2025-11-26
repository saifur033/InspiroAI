import re
from .ai_core import ask_ai
from .utils import detect_language
from .emotion_model import detect_emotion
from .fake_real_model import detect_fake
from .seo_score import compute_seo_score
from .hashtag_ranker import generate_hashtags


def clean_caption(text: str) -> str:
    """Clean caption text"""
    if not text:
        return ""
    text = text.replace("\r", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"([!?.])\1+", r"\1", text)
    return text.strip()


def rewrite_caption(caption: str, tone: str = "friendly", rewrite_type: str = "standard"):
    """
    Rewrite caption to be VIRAL, EMOTIONAL, ENGAGING, and PROFESSIONAL
    Returns only the optimized caption (no fallbacks)
    """
    if not caption or not caption.strip():
        return {"error": "Caption is empty"}

    lang = detect_language(caption)
    base = clean_caption(caption)

    # Dynamic prompt based on tone
    tone_guidance = {
        "professional": "Use corporate authority, credibility, expertise. Include actionable insights. Professional but engaging tone. Suitable for business posts.",
        "friendly": "Use warm, conversational, relatable tone with personality. Engaging and approachable. Make people feel like a friend is talking to them.",
        "emotional": "Evoke deep feelings, create emotional connection, inspire action. Use storytelling. Make it resonate with hearts.",
        "trendy": "Use viral language, trending phrases, modern slang, FOMO tactics. Make it shareable. Latest trends and zeitgeist.",
        "funny": "Use humor, wit, playful tone, relatable comedy. Make people smile and want to share.",
    }

    tone_text = tone_guidance.get(tone, tone_guidance["professional"])

    # Conservative refinement prompt - preserve meaning, fix grammar/clarity only
    user_prompt = f"""Refine the user's caption to make it clearer, smoother, and more engaging while keeping the exact meaning.

Do NOT rewrite the caption creatively.
Do NOT shorten or expand the caption.
Do NOT add new ideas, explanations, or meta-text.
Do NOT add labels like 'professional message' or 'powerful message'.
Do NOT change the language (Bangla stays Bangla, English stays English).
Do NOT change the user's tone.

Allowed:
- Fix grammar and clarity
- Improve readability and formatting
- Add clean line breaks for social media
- Add ONE small CTA at the end (same language)

Output ONLY the refined caption. No explanations. No prefix.

User Caption:
{caption}"""

    # Use ask_ai to get a refined caption
    rewritten_raw = ask_ai(user_prompt=user_prompt)

    # If ask_ai returns the prompt itself (fallback mode), generate a local rewrite
    if not rewritten_raw or rewritten_raw == user_prompt or len(rewritten_raw) > 500:
        # Use local refinement fallback - preserve original caption
        if tone == "professional":
            optimized = f"{base}\n\nLearn more today!"
        elif tone == "friendly":
            optimized = f"{base}\n\nShare your thoughts!"
        elif tone == "emotional":
            optimized = f"{base}\n\nFeel the connection!"
        elif tone == "trendy":
            optimized = f"{base}\n\nJoin the conversation!"
        elif tone == "funny":
            optimized = f"{base}\n\nMake me laugh!"
        else:
            optimized = f"{base}\n\nCheck it out!"
    else:
        # Clean the response - remove any meta-text
        rewritten_clean = rewritten_raw.strip()
        # Remove common prefixes
        rewritten_clean = re.sub(r"(?i)^(here's|here is|caption:|rewritten:|optimized:|improved:|refined:)[\s:]*", "", rewritten_clean)
        rewritten_clean = re.sub(r"(?i)^(write only|final caption|here it is|result:)[\s:]*", "", rewritten_clean)
        # Remove trailing meta
        rewritten_clean = re.sub(r"(?i)(NO HASHTAGS|no hashtags|#.*)?$", "", rewritten_clean).strip()
        # Remove system-style instructions
        rewritten_clean = re.sub(r"(?i)^(you are|write only|caption to rewrite).*?\n+", "", rewritten_clean, flags=re.DOTALL).strip()
        # Remove the full prompt if it somehow got included
        rewritten_clean = re.sub(r"(?i)RESPONSE:.*", "", rewritten_clean).strip()
        
        optimized = clean_caption(rewritten_clean)
        if not optimized or len(optimized) < 5:
            optimized = base  # Fall back to original if refinement failed

    # Score everything
    seo_org = compute_seo_score(base) or {}
    seo_new = compute_seo_score(optimized) or {}

    emo_original = detect_emotion(base) or {}
    emo_new = detect_emotion(optimized) or {}

    fr_original = detect_fake(base) or {}
    fr_new = detect_fake(optimized) or {}

    hashtags = generate_hashtags(optimized, tone=tone, top_n=20) or []

    # Generate emotion change reason - fully caption-dependent
    old_emo = emo_original.get("emotion", emo_original.get("top_emotion", "NEUTRAL")).upper()
    new_emo = emo_new.get("emotion", emo_new.get("top_emotion", "NEUTRAL")).upper()
    old_conf = int(emo_original.get("confidence", 50))
    new_conf = int(emo_new.get("confidence", 50))
    old_reason = emo_original.get("reason", "")
    new_reason = emo_new.get("reason", "")
    
    # Build emotion change text based on both original and optimized caption analysis
    if old_emo != new_emo:
        if lang == "bn":
            emotion_change = f"আবেগ {old_emo} থেকে {new_emo}-তে পরিবর্তিত। মূল: {old_reason[:30]}... → অপ্টিমাইজড: {new_reason[:30]}..."
        else:
            emotion_change = f"Emotion shifted from {old_emo} to {new_emo}. Original: {old_reason[:40]}... → Optimized: {new_reason[:40]}..."
    else:
        new_conf_int = int(new_conf) if new_conf else 50
        if lang == "bn":
            emotion_change = f"{new_emo} আবেগ {new_conf_int}% আস্থায় শক্তিশালী। {new_reason[:50]}..."
        else:
            emotion_change = f"{new_emo} emotion strengthened to {new_conf_int}% confidence. {new_reason[:60]}..."
    
    # Generate fake/real change reason - caption-dependent
    old_fake = int(fr_original.get("fake", 50))
    new_fake = int(fr_new.get("fake", 50))
    fake_change_pct = abs(new_fake - old_fake)
    
    # Include reasoning based on caption content
    old_fr_reason = fr_original.get("reasoning", fr_original.get("reason", ""))
    new_fr_reason = fr_new.get("reasoning", fr_new.get("reason", ""))
    
    if old_fake > 50 and new_fake <= 50:
        if lang == "bn":
            fake_real_change = f"সত্যতা উল্লেখযোগ্যভাবে উন্নত। বিশ্লেষণ: {new_fr_reason[:50]}..."
        else:
            fake_real_change = f"Authenticity improved significantly. Analysis: {new_fr_reason[:60]}..."
    elif old_fake <= 50 and new_fake > 50:
        if lang == "bn":
            fake_real_change = f"সতর্কতা: সত্যতা হ্রাস পেয়েছে। কারণ: {new_fr_reason[:50]}..."
        else:
            fake_real_change = f"Caution: authenticity decreased. Reason: {new_fr_reason[:60]}..."
    else:
        if lang == "bn":
            fake_real_change = f"সত্যতা স্কোর {fake_change_pct}% পরিবর্তিত। {new_fr_reason[:50]}..."
        else:
            fake_real_change = f"Authenticity score changed by {fake_change_pct}%. {new_fr_reason[:60]}..."

    return {
        "optimized_caption": optimized,
        "hashtags": hashtags,
        "old_seo_score": int(seo_org.get("score", 50)),
        "new_seo_score": int(seo_new.get("score", 50)),
        "updated_emotion": new_emo,
        "emotion_change": emotion_change,
        "updated_fake_percent": int(fr_new.get("fake", 50)),
        "updated_real_percent": int(fr_new.get("real", 50)),
        "fake_real_change": fake_real_change
    }

