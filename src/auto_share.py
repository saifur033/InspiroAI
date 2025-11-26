import requests
import time
from src.fb_poster import facebook_post


# ============================================================
#  FACEBOOK POST REACH READER (SAFE + UPDATED)
# ============================================================
def get_post_reach(post_id: str, token: str) -> int:
    """
    Safely fetch the reach of a Facebook post using the Graph API.
    Fully compatible with latest API versions.
    """

    url = f"https://graph.facebook.com/v18.0/{post_id}/insights"
    params = {
        "metric": "post_impressions",
        "access_token": token
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        # If API gives error, return safe fallback
        if "error" in data:
            print("❌ FB Insights Error:", data["error"].get("message"))
            return 0

        # Extract value safely
        return int(
            data.get("data", [{}])[0]
                .get("values", [{}])[0]
                .get("value", 0)
        )

    except Exception as e:
        print("❌ Reach Read Error:", e)
        return 0



# ============================================================
#  AUTO-SHARE WORKER (SAFE BACKGROUND ENGINE)
# ============================================================
def auto_share_runner(post_id, token, page_id, next_caption, target_reach):
    """
    Background smart auto-share engine:

    ✔ Reads post reach safely
    ✔ Waits until target reach is hit
    ✔ Auto-posts next message
    ✔ Avoids Facebook API rate limit
    ✔ Crash-safe infinite loop protection
    """

    print("\n============================")
    print("🚀 Auto-Share Worker Started")
    print("============================")
    print(f"📌 Watching Post: {post_id}")
    print(f"🎯 Target Reach: {target_reach}")
    print(f"🕒 Checking every 60 sec...\n")

    fail_count = 0

    while True:
        reach = get_post_reach(post_id, token)
        print(f"📊 Current Reach: {reach}")

        # If reach check fails too many times → abort for safety
        if reach == 0:
            fail_count += 1
            if fail_count >= 10:
                print("❌ Auto-Share stopped (too many failed checks).")
                break

        # If target reached → post automatically
        if reach >= target_reach:
            print("\n🎉 Target reached!")
            print("✈️ Auto posting next caption...\n")

            result = facebook_post(token, page_id, next_caption)

            print("📨 Post Result:", result)
            print("✅ Auto-Share Completed.\n")
            break

        # Sleep 1 minute to avoid API spam
        time.sleep(60)
