"""
Scheduler utility for managing scheduled posts
"""
from datetime import datetime
import time

class ScheduledPostManager:
    """Manages scheduled posts and checks when to post them"""
    
    @staticmethod
    def check_and_post(scheduled_posts, facebook_poster):
        """
        Check if any scheduled posts are due to be posted
        Returns list of posts that were posted
        """
        posted = []
        now = datetime.now()
        
        for post in scheduled_posts:
            if post['status'] == 'Pending':
                scheduled_dt = post['scheduled_dt']
                
                # Check if it's time to post (within 1 minute tolerance)
                time_diff = (scheduled_dt - now).total_seconds()
                
                if time_diff <= 0:  # Time has arrived
                    try:
                        success, result = facebook_poster.publish_post(message=post['caption'])
                        
                        if success:
                            post['status'] = 'Posted'
                            post['posted_at'] = now
                            post['post_id'] = result.get('post_id', 'unknown')
                            posted.append(post['id'])
                    except Exception as e:
                        post['status'] = 'Failed'
                        post['error'] = str(e)
        
        return posted
    
    @staticmethod
    def get_countdown(scheduled_dt):
        """
        Get time remaining until scheduled post
        Returns dict with days, hours, minutes, seconds
        """
        now = datetime.now()
        diff = scheduled_dt - now
        
        if diff.total_seconds() <= 0:
            return {'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'is_due': True}
        
        total_seconds = int(diff.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        return {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'is_due': False
        }
    
    @staticmethod
    def format_countdown(countdown):
        """Format countdown dict to readable string"""
        if countdown['is_due']:
            return "Ready to post!"
        
        parts = []
        if countdown['days'] > 0:
            parts.append(f"{countdown['days']}d")
        if countdown['hours'] > 0:
            parts.append(f"{countdown['hours']}h")
        if countdown['minutes'] > 0:
            parts.append(f"{countdown['minutes']}m")
        if countdown['seconds'] > 0:
            parts.append(f"{countdown['seconds']}s")
        
        return " ".join(parts) if parts else "Now"
