"""
Facebook API integration for posting captions
"""
import requests
from datetime import datetime


class FacebookAPI:
    """Facebook Graph API wrapper for posting"""
    
    def __init__(self, access_token=None):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0"
        self.last_post_id = None
        self.last_error = None
    
    def post_caption(self, page_id, caption):
        """
        Post caption to Facebook page
        
        Args:
            page_id: Facebook page ID
            caption: Caption text to post
        
        Returns:
            dict with success, post_id, url, or error message
        """
        if not self.access_token:
            return {
                "success": False,
                "error": "No access token provided. Set token in sidebar."
            }
        
        url = f"{self.base_url}/{page_id}/feed"
        params = {
            "message": caption,
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(url, json=params, timeout=10)
            
            if response.status_code == 200:
                post_data = response.json()
                post_id = post_data.get("id", "")
                self.last_post_id = post_id
                
                # Generate Facebook URL
                fb_url = f"https://www.facebook.com/{post_id.split('_')[1] if '_' in post_id else ''}"
                
                return {
                    "success": True,
                    "post_id": post_id,
                    "facebook_url": fb_url,
                    "message": f"✅ Post published successfully! Post ID: {post_id}",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "Unknown error")
                return {
                    "success": False,
                    "error": f"Facebook API Error: {error_msg}",
                    "status_code": response.status_code
                }
        
        except requests.Timeout:
            return {
                "success": False,
                "error": "Request timeout. Please try again."
            }
        except Exception as e:
            self.last_error = str(e)
            return {
                "success": False,
                "error": f"Error posting to Facebook: {str(e)}"
            }
    
    def schedule_caption(self, page_id, caption, publish_time):
        """
        Schedule caption to be posted at specific time
        
        Args:
            page_id: Facebook page ID
            caption: Caption text
            publish_time: Unix timestamp or datetime string
        
        Returns:
            dict with success status
        """
        if not self.access_token:
            return {
                "success": False,
                "error": "No access token provided."
            }
        
        url = f"{self.base_url}/{page_id}/feed"
        params = {
            "message": caption,
            "published": "false",
            "scheduled_publish_time": int(publish_time) if isinstance(publish_time, (int, float)) else publish_time,
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(url, json=params, timeout=10)
            
            if response.status_code == 200:
                post_data = response.json()
                return {
                    "success": True,
                    "post_id": post_data.get("id", ""),
                    "message": "✅ Post scheduled successfully!",
                    "scheduled_time": publish_time
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to schedule post"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error scheduling post: {str(e)}"
            }


def validate_facebook_token(token):
    """Validate Facebook access token"""
    try:
        url = "https://graph.facebook.com/v18.0/me"
        response = requests.get(url, params={"access_token": token}, timeout=5)
        return response.status_code == 200
    except:
        return False
