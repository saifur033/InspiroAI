import re
import random
from collections import Counter
from typing import List

def detect_language(text: str) -> str:
    bn = sum(1 for c in text if 2432 <= ord(c) <= 2559)
    return "bn" if bn > 8 else "en"

def extract_keywords(caption: str, lang: str, top_n: int = 10) -> List[str]:
    if not caption:
        return []
    txt = re.sub(r"[#@!$%^&*()\-_=+{}\[\]|\\:;\"''<>,.?/]", " ", caption)
    words = re.findall(r"\b[\w\u0980-\u09FF]{3,}\b", txt.lower())
    
    stopwords_en = {"the", "and", "is", "are", "to", "of", "in", "for", "with", "a", "an", "on", "by", "it", "this", "that", "from", "as", "was", "were", "be", "but", "not", "or", "about", "share", "post", "follow"}
    stopwords_bn = {"এবং", "এটি", "যে", "থেকে", "করে", "হয়", "না", "জন্য", "এই", "আমি", "আমরা", "তুমি", "আপনি"}
    
    stop = stopwords_bn if lang == "bn" else stopwords_en
    filtered = [w for w in words if w not in stop]
    freq = Counter(filtered)
    return [w for w, _ in freq.most_common(top_n)]

def generate_hashtags(caption: str, tone: str = "general", top_n: int = 15) -> List[str]:
    if not caption or not caption.strip():
        return []

    lang = detect_language(caption)
    keywords = extract_keywords(caption, lang, top_n=10)
    hashtags = [f"#{kw}" for kw in keywords]
    
    tone_tags = {
        "professional": ["#business", "#professional", "#growth", "#strategy", "#insights"],
        "friendly": ["#goodvibes", "#friends", "#community", "#love", "#grateful"],
        "emotional": ["#inspiration", "#motivation", "#heartfelt", "#real", "#authentic"],
        "trendy": ["#trending", "#viral", "#reels", "#foryou", "#viral"],
        "funny": ["#comedy", "#humor", "#funny", "#laughs", "#memes"],
    }
    
    tone_specific = tone_tags.get(tone, [])
    hashtags.extend(tone_specific[:5])
    hashtags = list(dict.fromkeys(hashtags))[:top_n]
    
    if len(hashtags) < 10:
        general_tags = ["#instagood", "#explorepage", "#socialmedia", "#content", "#creative", "#digital", "#online", "#web", "#marketing", "#engagement"]
        hashtags.extend(general_tags[:10 - len(hashtags)])
    
    return hashtags[:top_n]
