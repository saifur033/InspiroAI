"""
scheduler_engine.py — InspiroAI Auto Scheduler Engine v6.0 (2025 Ultra Stable)

✔ Auto Scheduler (Background)
✔ Clean JSON
✔ Duplicate Job Protection
✔ Media + Text Posting
✔ Auto Cleanup of Old Jobs
"""

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from src.facebook_api import post_to_page, post_media_to_page

scheduler = BackgroundScheduler()
scheduler.start()


# ---------------------------------------------------------
# 🔥 INTERNAL CLEANUP — remove expired jobs
# ---------------------------------------------------------
def _cleanup_old_jobs():
    for job in scheduler.get_jobs():
        if job.next_run_time and job.next_run_time < datetime.now():
            try:
                scheduler.remove_job(job.id)
            except:
                pass


# ---------------------------------------------------------
# 🔥 ADD NEW SCHEDULE
# ---------------------------------------------------------
def scheduler_add(data):
    try:
        token = data.get("token")
        page_id = data.get("page_id")
        caption = data.get("caption")
        run_time = data.get("run_time")
        media_url = data.get("media_url")

        if not (token and page_id and caption and run_time):
            return {"success": False, "message": "Missing required fields."}

        # Convert string → datetime
        try:
            dt = datetime.strptime(run_time, "%Y-%m-%d %H:%M:%S")
        except:
            return {"success": False, "message": "Invalid time format. Use YYYY-MM-DD HH:MM:SS"}

        # Cleanup old jobs
        _cleanup_old_jobs()

        # Unique job id based on timestamp
        job_id = f"job_{int(dt.timestamp())}"

        # Remove old job with same ID
        try:
            scheduler.remove_job(job_id)
        except:
            pass

        # Choose function
        if media_url and media_url.strip():
            func = post_media_to_page
            args = [token, page_id, media_url, caption]
        else:
            func = post_to_page
            args = [token, page_id, caption]

        scheduler.add_job(
            func=func,
            trigger="date",
            run_date=dt,
            id=job_id,
            args=args,
            replace_existing=True
        )

        return {
            "success": True,
            "message": "Scheduled successfully!",
            "job_id": job_id,
            "run_time": dt.strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------------------------------------------------------
# 📋 LIST ALL JOBS
# ---------------------------------------------------------
def scheduler_list():
    _cleanup_old_jobs()

    jobs = scheduler.get_jobs()
    arr = []

    for j in jobs:
        arr.append({
            "id": j.id,
            "run_time": j.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
            if j.next_run_time else "N/A"
        })

    return {"success": True, "jobs": arr}


# ---------------------------------------------------------
# ❌ DELETE JOB
# ---------------------------------------------------------
def scheduler_delete(job_id):
    try:
        scheduler.remove_job(job_id)
        return {"success": True, "message": "Job deleted"}
    except:
        return {"success": False, "message": "Invalid job ID"}
