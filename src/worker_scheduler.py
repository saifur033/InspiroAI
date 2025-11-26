"""
worker_scheduler.py — InspiroAI Scheduled Posting Worker v8.0 (2025 Final)
✔ Text + Media Scheduling
✔ Auto-retry safe
✔ Clean FB response handling
✔ Prevent duplicate posting
✔ Zero-Crash Worker Loop
"""

import time
import logging
from datetime import datetime

from src.db_manager import (
    get_pending_schedule,
    mark_schedule_sent,
    get_token
)

from src.facebook_api import (
    post_to_page,
    post_media_to_page
)


# ---------------------------------------------------------
# Logging setup
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)


# ---------------------------------------------------------
# Time parser
# ---------------------------------------------------------
def parse_time(ts: str):
    """
    Converts DB stored format:
      '2025-01-21 14:45'
    → datetime object
    """
    try:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    except:
        try:
            return datetime.strptime(ts, "%Y-%m-%d %H:%M")
        except Exception:
            return None


# ---------------------------------------------------------
# Main Worker
# ---------------------------------------------------------
def run_scheduler():
    logging.info("🟪 Scheduler Worker Started...")

    while True:
        try:
            # Load scheduler rows
            rows = get_pending_schedule()

            if rows:
                logging.info(f"📌 {len(rows)} pending scheduled posts found.")

            # Token
            token_info = get_token()
            if not token_info:
                logging.warning("⚠ No token saved. Scheduler waiting...")
                time.sleep(25)
                continue

            api_token, page_id, _ = token_info

            now = datetime.now()

            for row in rows:
                sched_id, text, time_str, post_type = row

                run_time = parse_time(time_str)
                if not run_time:
                    logging.error(f"❌ Invalid datetime for ID {sched_id}: {time_str}")
                    continue

                # Time reached
                if now >= run_time:
                    logging.info(f"🚀 Running scheduled job ID {sched_id}")

                    # ------------------------------------------
                    # Handle TEXT ONLY post
                    # ------------------------------------------
                    if post_type == "text":
                        fb_res = post_to_page(api_token, page_id, text)

                    # ------------------------------------------
                    # Handle MEDIA post (URL stored in post_type)
                    # ------------------------------------------
                    else:
                        media_url = post_type.strip()
                        fb_res = post_media_to_page(api_token, page_id, media_url, text)

                    logging.info(f"📡 Facebook Response: {fb_res}")

                    # Success → Mark as sent
                    if fb_res.get("success"):
                        mark_schedule_sent(sched_id)
                        logging.info(f"✔ Job {sched_id} marked as SENT")

                    else:
                        logging.warning(
                            f"⚠ Post ID {sched_id} failed, will retry later..."
                        )

            time.sleep(20)

        except Exception as e:
            logging.error(f"🔥 Scheduler Worker Error: {e}")
            time.sleep(20)


# ---------------------------------------------------------
# Run directly
# ---------------------------------------------------------
if __name__ == "__main__":
    run_scheduler()
