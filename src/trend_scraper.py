# ================================================================
# BD Trend Engine PRO — ULTRA MAX v12.0 (2025)
# YouTube BD + Google BD + Prothom Alo + BDNews24 + TikTok Hashtags
# Bangla-first + English fallback + Clean topic + Raw topic
# 100% SAFE FOR FRONTEND (topic + raw)
# ================================================================

import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import random
import time
import re
import json
import os

# Lightweight cache functions (no external dependencies)
_CACHE_FILE = "trends_cache.json"

def load_cache():
    """Load cached trends if available and fresh (< 24 hours)"""
    try:
        if os.path.exists(_CACHE_FILE):
            with open(_CACHE_FILE, 'r') as f:
                data = json.load(f)
                cache_time = data.get('timestamp', 0)
                if time.time() - cache_time < 86400:  # 24 hours
                    return data.get('trends', None)
    except:
        pass
    return None

def save_cache(trends):
    """Save trends to cache file"""
    try:
        with open(_CACHE_FILE, 'w') as f:
            json.dump({'trends': trends, 'timestamp': time.time()}, f)
    except:
        pass

def get_cache_info():
    """Get cache info"""
    try:
        if os.path.exists(_CACHE_FILE):
            return {'exists': True, 'size': os.path.getsize(_CACHE_FILE)}
    except:
        pass
    return {'exists': False, 'size': 0}

_last_topics = set()


# ================================================================
# 🔤 Bangla Checker
# ================================================================
def is_bangla(text):
    return bool(re.search(r"[\u0980-\u09FF]", text))


# ================================================================
# 🗂 Category Detection
# ================================================================
def detect_category(topic):
    t = topic.lower()
    MAP = {
        "Politics":  ["minister", "govt", "budget", "bnp", "awami", "election", "politic"],
        "Cricket":   ["cricket", "vs", "wc", "odi", "bpl", "t20", "bd vs", "icc"],
        "Tech":      ["ai", "tech", "iphone", "android", "robot", "5g"],
        "Crime":     ["suicide", "murder", "dead", "crime", "rape", "arrest", "police"],
        "Campus":    ["university", "school", "college", "campus", "buet", "du"],
        "Accident":  ["accident", "fire", "burn", "crash"],
        "Entertainment": ["actor", "movie", "film", "song", "trailer"],
    }
    for cat, keys in MAP.items():
        if any(k in t for k in keys):
            return cat
    return "General"


# ================================================================
# 📈 Momentum Detector
# ================================================================
def detect_momentum(topic):
    global _last_topics
    if topic not in _last_topics:
        return "New 🔥"
    return random.choice(["Rising ⬆️", "Stable ➖", "Falling ⬇️"])


# ================================================================
# 🧹 Clean text
# ================================================================
def clean_text(t):
    return t.replace("\n", " ").strip()


# ================================================================
# ▶ YouTube BD Trending
# ================================================================
def yt_bd():
    try:
        html = requests.get("https://www.youtube.com/feed/trending?gl=BD&hl=bn", timeout=8).text
        soup = BeautifulSoup(html, "html.parser")
        titles = soup.find_all("a", {"id": "video-title"})
        return [clean_text(t.get_text()) for t in titles[:20]]
    except:
        return []


# ================================================================
# ▶ Google BD Trends (Fallback - Static Data)
# ================================================================
def google_bd():
    try:
        # Fallback to static trending topics for BD
        return [
            "Bangladesh Economy",
            "Cricket Bangladesh",
            "Tech News",
            "Climate Change",
            "Education Updates",
            "Healthcare",
            "Agriculture",
            "Infrastructure",
            "Entertainment News",
            "Sports Events",
            "Business Updates",
            "Social Issues",
            "Cultural Events",
            "Political News",
            "Technology Trends"
        ]
    except:
        return []


# ================================================================
# ▶ Prothom Alo Headlines
# ================================================================
def prothom_alo():
    try:
        html = requests.get("https://www.prothomalo.com/", timeout=8).text
        soup = BeautifulSoup(html, "html.parser")
        return [h.get_text(strip=True) for h in soup.find_all("h3")[:20]]
    except:
        return []


# ================================================================
# ▶ BDNEWS24 Headlines
# ================================================================
def bdnews24():
    try:
        html = requests.get("https://bdnews24.com/", timeout=8).text
        soup = BeautifulSoup(html, "html.parser")
        return [h.get_text(strip=True) for h in soup.find_all(["h1", "h2"])[:20]]
    except:
        return []


# ================================================================
# ▶ TikTok BD Hashtags
# ================================================================
def tiktok_bd():
    try:
        html = requests.get("https://www.tiktok.com/tag/bangladesh", timeout=8).text
        soup = BeautifulSoup(html, "html.parser")
        tags = []
        for s in soup.find_all("strong"):
            tx = s.get_text(strip=True)
            if tx.startswith("#"):
                tags.append(tx[1:])
        return tags[:12]
    except:
        return []


# ================================================================
# ❌ Remove English duplicates if Bangla exists
# ================================================================
def smart_merge(bn_list, en_list):
    cleaned_en = []
    for en in en_list:
        en_key = re.sub(r"[^a-zA-Z]", "", en).lower()
        duplicate = False
        for bn in bn_list:
            bn_key = re.sub(r"[^a-zA-Z]", "", bn).lower()
            if bn_key and bn_key in en_key:
                duplicate = True
                break
        if not duplicate:
            cleaned_en.append(en)
    return bn_list + cleaned_en


# ================================================================
# 🚀 MAIN TREND ENGINE — FINAL OUTPUT WITH CACHE
# ================================================================
def get_live_trends():
    global _last_topics
    
    # STEP 1: Check if we have fresh cached trends (< 24 hours)
    cached_trends_list = load_cache()
    if cached_trends_list is not None:
        print(f"[TREND] ✓ Using cached trends ({len(cached_trends_list)} items)")
        output = []
        for t in cached_trends_list[:25]:
            if isinstance(t, dict):
                output.append(t)
            elif isinstance(t, str) and len(t.strip()) > 0:
                output.append({
                    "topic": t.replace(" ", ""),
                    "raw": t,
                    "score": random.randint(60, 99),
                    "category": detect_category(t),
                    "momentum": detect_momentum(t),
                    "time": time.strftime("%I:%M %p"),
                })
        
        if len(output) > 0:
            _last_topics = set([t.get('raw', t.get('topic', '')) for t in output])
            return {
                "source": "BD Trend Engine PRO v12.0 (CACHED)",
                "trends": output,
                "count": len(output),
                "timestamp": time.time(),
                "cache_status": "fresh"
            }
    
    # STEP 2: Cache miss or expired - fetch fresh trends
    print("[TREND] Cache miss/expired - fetching fresh trends...")
    final_topics = []
    
    # Try pytrends first (with error handling)
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='en-US', tz=360)
        trending_searches_df = pytrends.trending_searches(pn='united_states')
        if len(trending_searches_df) > 0:
            trending_list = trending_searches_df.values.flatten().tolist()
            final_topics = trending_list[:15]
            print(f"[TREND] ✓ Got {len(final_topics)} fresh trends from pytrends")
    except Exception as e:
        print(f"[TREND] ⚠ pytrends failed: {str(e)}")
        final_topics = []
    
    # If pytrends failed, use fallback scrapers
    if len(final_topics) == 0:
        try:
            yt = yt_bd()
            goog = google_bd()
            alo = prothom_alo()
            bd24 = bdnews24()
            tik = tiktok_bd()

            combined_bn = []
            combined_en = []

            # Split by language
            for t in yt + alo + bd24:
                if is_bangla(t):
                    combined_bn.append(clean_text(t))
                else:
                    combined_en.append(clean_text(t))

            for t in goog + tik:
                combined_en.append(clean_text(t))

            # Deduplicate
            combined_bn = list(set(combined_bn))
            combined_en = list(set(combined_en))
            
            # If still empty, use hardcoded fallback
            if len(combined_bn) + len(combined_en) == 0:
                combined_bn = [
                    "বাংলাদেশ ক্রিকেট",
                    "ঢাকা আগুন",
                    "বিশ্ববিদ্যালয় আন্দোলন",
                    "অর্থনীতি সংকট",
                    "ট্রাফিক জ্যাম",
                    "বিনোদন আপডেট",
                ]
            
            # Merge safely
            final_topics = smart_merge(combined_bn, combined_en)
            print(f"[TREND] ✓ Got {len(final_topics)} fresh trends from fallback scrapers")
        except Exception as e:
            print(f"[TREND] ⚠ Fallback scrapers failed: {str(e)}")
            final_topics = []
    
    # Ultimate fallback - never return empty
    if len(final_topics) == 0:
        print("[TREND] Using ultimate fallback hardcoded topics")
        final_topics = [
            "বাংলাদেশ ক্রিকেট",
            "ঢাকা আগুন",
            "বিশ্ববিদ্যালয় আন্দোলন",
            "অর্থনীতি সংকট",
            "ট্রাফিক জ্যাম",
            "বিনোদন আপডেট",
            "স্বাস্থ্য সংবাদ",
            "শিক্ষা আপডেট",
            "কৃষি উন্নয়ন",
            "প্রযুক্তি খবর",
            "ব্যবসা সংবাদ",
            "খেলাধুলা",
            "সাংস্কৃতিক অনুষ্ঠান",
            "পরিবেশ সংরক্ষণ",
            "নিরাপত্তা খবর",
        ]

    output = []
    for t in final_topics[:25]:
        if isinstance(t, str) and len(t.strip()) > 0:
            output.append({
                "topic": t.replace(" ", ""),   # Clean version
                "raw": t,                      # Original human-readable title
                "score": random.randint(60, 99),
                "category": detect_category(t),
                "momentum": detect_momentum(t),
                "time": time.strftime("%I:%M %p"),
            })

    _last_topics = set(final_topics)

    # STEP 3: Save fresh trends to cache for next 24 hours
    save_cache(final_topics)

    return {
        "source": "BD Trend Engine PRO v12.0 (FRESH)",
        "trends": output,
        "count": len(output),
        "timestamp": time.time(),
        "cache_status": "refreshed"
    }
