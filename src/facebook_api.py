"""
facebook_api.py — InspiroAI Facebook Engine v5.0 (Final Ultra Stable Edition)

🔥 Supports:
- Text Posting
- Photo / Video Upload
- Reels Support (Auto detect)
- Scheduled Posting (text + media)
- Safe JSON Response for UI
- Token Verification
"""

import requests
from typing import Dict, Optional
import time

GRAPH_VERSION = "v19.0"
GRAPH_URL = f"https://graph.facebook.com/{GRAPH_VERSION}"


# -------------------------------------------------------------
# 🧾 Safe Response Wrapper
# -------------------------------------------------------------
def _safe(response: requests.Response) -> Dict:
    """Converts every FB response into a clean safe JSON."""
    try:
        data = response.json()
    except:
        return {
            "success": False,
            "reason": "❌ Facebook returned invalid JSON",
            "raw": response.text
        }

    if response.status_code in (200, 201):
        return {
            "success": True,
            "id": data.get("id"),
            "response": data,
            "reason": "OK"
        }

    error = data.get("error", {})
    return {
        "success": False,
        "reason": error.get("message", "Unknown Facebook API Error"),
        "code": error.get("code"),
        "type": error.get("type"),
        "trace_id": error.get("fbtrace_id")
    }


# -------------------------------------------------------------
# 🔍 Detect media type (Image / Video / Reel)
# -------------------------------------------------------------
def _detect_media(url: str) -> str:
    url = url.lower()

    if any(url.endswith(ext) for ext in [".mp4", ".mov", ".mkv", ".avi"]):
        return "video"

    if "reel" in url or "short" in url:
        return "reel"

    return "photo"


# =========================================================================
# 🎯 MAIN WRAPPER - Used by Pro Dashboard Share Button
# =========================================================================
def post_to_facebook(page_id: str, message: str, access_token: str) -> Dict:
    """
    Main wrapper used by Pro Dashboard share button.
    
    Args:
        page_id: Facebook page ID
        message: Caption/post text
        access_token: Facebook access token
    
    Returns:
        {success: bool, id: post_id, error: error_msg, ...}
    """
    return post_to_page(access_token, page_id, message)


# =========================================================================
# =========================================================================

# -------------------------------------------------------------
# 📝 TEXT POST
# -------------------------------------------------------------
def post_to_page(token: str, page_id: str, message: str) -> Dict:

    if not (token and page_id and message.strip()):
        return {"success": False, "reason": "⚠ Missing token/page_id/message"}

    url = f"{GRAPH_URL}/{page_id}/feed"
    params = {
        "access_token": token,
        "message": message.strip()
    }

    try:
        resp = requests.post(url, params=params, timeout=10)
        res = _safe(resp)
        if res["success"]:
            res["reason"] = "✅ Text post published!"
        return res
    except Exception as e:
        return {"success": False, "reason": f"❌ Network error: {e}"}


# -------------------------------------------------------------
# 🖼 MEDIA (PHOTO / VIDEO / REEL)
# -------------------------------------------------------------
def post_media_to_page(token: str, page_id: str, media_url: str, caption: str = "") -> Dict:

    if not (token and page_id and media_url):
        return {"success": False, "reason": "⚠ Missing media info"}

    media_type = _detect_media(media_url)
    endpoint = "videos" if media_type in ("video", "reel") else "photos"

    url = f"{GRAPH_URL}/{page_id}/{endpoint}"

    params = {
        "access_token": token,
        "url": media_url,
        "caption": caption or ""
    }

    try:
        resp = requests.post(url, params=params, timeout=20)
        res = _safe(resp)

        if res["success"]:
            label = "Reel" if media_type == "reel" else media_type.title()
            res["reason"] = f"✅ {label} uploaded successfully!"

        return res

    except Exception as e:
        return {"success": False, "reason": f"❌ Upload failed: {e}"}


# -------------------------------------------------------------
# ⏰ SCHEDULED POST
# -------------------------------------------------------------
def schedule_post_to_page(
    token: str,
    page_id: str,
    message: str,
    publish_unix: int,
    media_url: Optional[str] = None
) -> Dict:

    if not (token and page_id and message):
        return {"success": False, "reason": "⚠ Missing required fields"}

    media_type = _detect_media(media_url) if media_url else None
    endpoint = (
        "videos" if media_type in ("video", "reel") else
        "photos" if media_url else
        "feed"
    )

    url = f"{GRAPH_URL}/{page_id}/{endpoint}"

    params = {
        "access_token": token,
        "published": False,
        "scheduled_publish_time": publish_unix
    }

    if media_url:
        params["url"] = media_url
        params["caption"] = message
    else:
        params["message"] = message

    try:
        resp = requests.post(url, params=params, timeout=20)
        res = _safe(resp)

        if res["success"]:
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(publish_unix))
            res["reason"] = f"⏰ Post scheduled for {dt}"

        return res

    except Exception as e:
        return {"success": False, "reason": f"❌ Scheduling failed: {e}"}


# -------------------------------------------------------------
# 🎯 AUTO SHARE CHECKER
# -------------------------------------------------------------
def post_when_reach_goal(
    token: str,
    page_id: str,
    message: str,
    current_reach: int,
    reach_goal: int,
    media_url: Optional[str] = None
) -> Dict:

    if current_reach < reach_goal:
        return {
            "success": False,
            "status": "waiting",
            "reason": f"📉 Reach {current_reach}/{reach_goal} — waiting..."
        }

    # Ready to post
    if media_url:
        return post_media_to_page(token, page_id, media_url, message)

    return post_to_page(token, page_id, message)


# -------------------------------------------------------------
# 🔐 TOKEN VERIFICATION
# -------------------------------------------------------------
def verify_token(token: str) -> Dict:

    url = f"{GRAPH_URL}/debug_token"
    params = {
        "input_token": token,
        "access_token": token
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()

        info = data.get("data", {})

        if info.get("is_valid"):
            return {
                "success": True,
                "valid": True,
                "app_id": info.get("app_id"),
                "expires_at": info.get("expires_at"),
                "scopes": info.get("scopes"),
                "reason": "✅ Token valid"
            }

        return {
            "success": False,
            "valid": False,
            "reason": info.get("error", "Invalid token"),
            "details": info
        }

    except Exception as e:
        return {
            "success": False,
            "valid": False,
            "reason": f"❌ Network error: {e}"
        }
