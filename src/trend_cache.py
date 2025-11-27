"""
Trend Cache Manager - Stores trending data with daily refresh
Fresh trends every 24 hours, fallback if API fails
"""

import json
import os
import time
from datetime import datetime, timedelta

CACHE_FILE = "trends_cache.json"
CACHE_EXPIRY = 24 * 3600  # 24 hours in seconds

def get_cache_path():
    """Get absolute path for cache file"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), CACHE_FILE)

def load_cache():
    """Load cached trends if valid"""
    cache_path = get_cache_path()
    
    if not os.path.exists(cache_path):
        return None
    
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if cache is still fresh (< 24 hours old)
        cached_time = data.get('timestamp', 0)
        current_time = time.time()
        age_seconds = current_time - cached_time
        
        if age_seconds < CACHE_EXPIRY:
            print(f"[CACHE] ✓ Using fresh cache (age: {age_seconds/3600:.1f}h)")
            return data.get('trends', None)
        else:
            print(f"[CACHE] Expired (age: {age_seconds/3600:.1f}h > 24h) - will refresh")
            return None
            
    except Exception as e:
        print(f"[CACHE-ERROR] Failed to load cache: {e}")
        return None

def save_cache(trends):
    """Save trends to cache file"""
    cache_path = get_cache_path()
    
    try:
        cache_data = {
            'timestamp': time.time(),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'trends': trends,
            'count': len(trends) if isinstance(trends, list) else 0
        }
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print(f"[CACHE] ✓ Saved {len(trends)} trends to cache")
        return True
    except Exception as e:
        print(f"[CACHE-ERROR] Failed to save cache: {e}")
        return False

def get_cache_info():
    """Get cache metadata (for debugging)"""
    cache_path = get_cache_path()
    
    if not os.path.exists(cache_path):
        return {"status": "no_cache"}
    
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cached_time = data.get('timestamp', 0)
        current_time = time.time()
        age_seconds = current_time - cached_time
        
        return {
            "status": "cached",
            "date": data.get('date', 'unknown'),
            "age_hours": round(age_seconds / 3600, 2),
            "count": data.get('count', 0),
            "expires_in_hours": round((CACHE_EXPIRY - age_seconds) / 3600, 2)
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def clear_cache():
    """Clear cache (manual refresh)"""
    cache_path = get_cache_path()
    
    try:
        if os.path.exists(cache_path):
            os.remove(cache_path)
            print("[CACHE] ✓ Cache cleared")
            return True
    except Exception as e:
        print(f"[CACHE-ERROR] Failed to clear cache: {e}")
        return False
