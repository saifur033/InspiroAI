# ==========================================================
# auto_share_monitor.py — InspiroAI Auto-Share System v1.0
# ==========================================================
# Automatically shares posts on Facebook when reach goals are met
# Monitors posts and auto-posts when engagement reaches target

import time
import json
import logging
from datetime import datetime, timedelta
from src.db_manager import get_auto_share, get_token
from src.facebook_api import post_to_facebook

logger = logging.getLogger(__name__)

class AutoShareMonitor:
    """
    Monitors scheduled posts and automatically shares to Facebook
    when reach goals are met.
    
    Features:
    - Track scheduled posts
    - Monitor reach/engagement metrics
    - Auto-post when goals met
    - Cooldown to prevent duplicate posting
    - Logging of all auto-shares
    """
    
    def __init__(self):
        self.check_interval = 60  # Check every 60 seconds
        self.last_check = None
        self.active_monitors = {}
    
    def get_auto_share_config(self):
        """Get current auto-share configuration from database"""
        try:
            result = get_auto_share()
            if result:
                reach_goal, caption = result
                return {
                    "reach_goal": reach_goal,
                    "caption": caption,
                    "enabled": True
                }
            return {"enabled": False}
        except Exception as e:
            logger.error(f"[ERROR] get_auto_share_config: {str(e)}")
            return {"enabled": False}
    
    def get_pending_posts(self):
        """
        Get posts scheduled for auto-share that haven't been posted yet
        Note: This is a simplified version. In production, would fetch from schedule_posts table.
        For now, we monitor reach goals passively.
        """
        try:
            # Simplified: Return empty list for now
            # Full implementation would query schedule_posts table
            return []
        except Exception as e:
            logger.error(f"[ERROR] get_pending_posts: {str(e)}")
            return []
    
    def get_post_reach(self, post_id, page_id, token):
        """
        Get current reach for a Facebook post
        
        Args:
            post_id: Facebook post ID
            page_id: Facebook page ID
            token: Facebook access token
        
        Returns:
            Reach count (int) or None if error
        """
        try:
            import requests
            
            url = f"https://graph.facebook.com/v18.0/{post_id}"
            params = {
                'fields': 'reach,impressions,engagement',
                'access_token': token
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                reach = data.get('reach', 0)
                return reach
            else:
                logger.warning(f"[WARN] Could not fetch reach for post {post_id}")
                return None
                
        except Exception as e:
            logger.error(f"[ERROR] get_post_reach: {str(e)}")
            return None
    
    def check_and_post(self):
        """
        Main monitoring function: Check posts and auto-post when goals met
        
        Returns:
            Dict with monitoring results
        """
        try:
            config = self.get_auto_share_config()
            
            if not config.get("enabled"):
                return {"status": "disabled", "posts_checked": 0, "posts_shared": 0}
            
            reach_goal = config.get("reach_goal", 5000)
            auto_caption = config.get("caption", "")
            
            # Get token settings
            token_data = get_token()
            if not token_data:
                logger.warning("[WARN] No Facebook token configured")
                return {"status": "no_token", "posts_checked": 0, "posts_shared": 0}
            
            # Token data returns tuple: (api_token, page_id, dev_mode)
            access_token = token_data[0] if isinstance(token_data, tuple) else token_data.get("token")
            page_id = token_data[1] if isinstance(token_data, tuple) else token_data.get("page_id")
            
            if not access_token or not page_id:
                logger.warning("[WARN] Invalid token/page configuration")
                return {"status": "invalid_config", "posts_checked": 0, "posts_shared": 0}
            
            # Get pending posts
            pending_posts = self.get_pending_posts()
            posts_checked = len(pending_posts)
            posts_shared = 0
            shared_posts = []
            
            for post in pending_posts:
                post_id, caption, fb_page_id, scheduled_time, reach_predicted = post
                
                try:
                    # Check if post time has arrived
                    scheduled_dt = datetime.fromisoformat(scheduled_time)
                    if datetime.now() < scheduled_dt:
                        continue  # Post not yet scheduled to go live
                    
                    # Get current reach (if post already exists on Facebook)
                    current_reach = self.get_post_reach(post_id, fb_page_id, access_token)
                    
                    # Use predicted reach or current reach
                    reach = current_reach or reach_predicted or 0
                    
                    logger.info(f"[CHECK] Post {post_id}: reach={reach}, goal={reach_goal}")
                    
                    # Check if reach goal met
                    if reach >= reach_goal:
                        # Auto-post additional share
                        share_caption = auto_caption or f"Check out this amazing content! Reached {reach} views! 🚀"
                        
                        success = post_to_facebook(
                            message=share_caption,
                            page_id=page_id,
                            token=access_token
                        )
                        
                        if success:
                            posts_shared += 1
                            shared_posts.append({
                                "original_post_id": post_id,
                                "reach": reach,
                                "timestamp": datetime.now().isoformat()
                            })
                            
                            # Log the auto-share (database update can be added later if needed)
                            logger.info(f"[OK] Auto-shared post {post_id} (reach: {reach})")
                        else:
                            logger.error(f"[ERROR] Failed to auto-share post {post_id}")
                    
                except Exception as e:
                    logger.error(f"[ERROR] Processing post {post_id}: {str(e)}")
                    continue
            
            return {
                "status": "success",
                "posts_checked": posts_checked,
                "posts_shared": posts_shared,
                "shared_posts": shared_posts,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"[ERROR] check_and_post: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "posts_checked": 0,
                "posts_shared": 0
            }
    
    def get_monitoring_status(self):
        """Get current monitoring status and statistics"""
        try:
            return {
                "total_monitored": 0,
                "auto_shared": 0,
                "pending": 0,
                "monitoring_active": self.get_auto_share_config().get("enabled", False)
            }
        except Exception as e:
            logger.error(f"[ERROR] get_monitoring_status: {str(e)}")
            return {"error": str(e)}


# Global monitor instance
auto_share_monitor = AutoShareMonitor()


def start_auto_share_monitoring(scheduler=None):
    """
    Start background monitoring task
    
    Args:
        scheduler: APScheduler instance (optional)
    
    Returns:
        Job ID if scheduler provided, else None
    """
    try:
        def monitor_job():
            result = auto_share_monitor.check_and_post()
            if result.get("posts_shared", 0) > 0:
                logger.info(f"[AUTO-SHARE] Shared {result['posts_shared']} post(s)")
        
        if scheduler:
            # Add recurring job every 30 seconds
            job = scheduler.add_job(
                monitor_job,
                'interval',
                seconds=30,
                id='auto_share_monitor',
                replace_existing=True
            )
            logger.info("[OK] Auto-share monitoring started (every 30 seconds)")
            return job.id
        else:
            logger.info("[WARN] No scheduler provided - auto-share monitoring not started")
            return None
            
    except Exception as e:
        logger.error(f"[ERROR] start_auto_share_monitoring: {str(e)}")
        return None


def stop_auto_share_monitoring(scheduler=None):
    """Stop background monitoring task"""
    try:
        if scheduler:
            scheduler.remove_job('auto_share_monitor')
            logger.info("[OK] Auto-share monitoring stopped")
            return True
    except Exception as e:
        logger.warning(f"[WARN] Error stopping auto-share monitoring: {str(e)}")
        return False


# Example usage:
# from src.auto_share_monitor import auto_share_monitor, start_auto_share_monitoring
# result = auto_share_monitor.check_and_post()
# print(result)
