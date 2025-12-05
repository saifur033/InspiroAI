"""
Facebook Graph API v18.0 - Posting Module
============================================
Handles posting captions to Facebook Pages using the latest Graph API.

Features:
- Publish posts with message/media
- Error handling for invalid tokens, permissions
- Response with Post ID on success
- Detailed error messages for debugging
"""

import requests
import json
from typing import Dict, Tuple, Optional


class FacebookPoster:
    """
    Reusable Facebook posting utility for Streamlit apps.
    
    Usage:
    ------
    poster = FacebookPoster(page_token="...", page_id="...")
    success, result = poster.publish_post(message="Hello World")
    """
    
    # Facebook Graph API version
    API_VERSION = "v18.0"
    GRAPH_URL = f"https://graph.facebook.com/{API_VERSION}"
    
    # Timeout for API requests (seconds)
    REQUEST_TIMEOUT = 15
    
    def __init__(self, page_token: str, page_id: str):
        """
        Initialize Facebook Poster.
        
        Args:
            page_token (str): Facebook Page Access Token (from Meta Developer Dashboard)
            page_id (str): Facebook Page ID (numeric)
        """
        self.page_token = page_token.strip() if page_token else None
        self.page_id = page_id.strip() if page_id else None
        self.last_post_id = None
        self.last_error = None
    
    def validate_credentials(self) -> Tuple[bool, str]:
        """
        Validate if token and page ID are valid.
        
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if not self.page_token:
            return False, "❌ Missing Facebook Page Access Token"
        
        if not self.page_id:
            return False, "❌ Missing Facebook Page ID"
        
        # Check if page_id is numeric
        if not str(self.page_id).isdigit():
            return False, "❌ Page ID must be numeric (no dashes or special characters)"
        
        if len(self.page_token) < 50:
            return False, "❌ Token looks too short (tokens are usually 100+ characters)"
        
        return True, "✅ Credentials look valid"
    
    def publish_post(self, message: str, media_url: Optional[str] = None) -> Tuple[bool, Dict]:
        """
        Publish a post to Facebook Page.
        
        Args:
            message (str): Caption/message text (required)
            media_url (str, optional): URL to image or video
        
        Returns:
            Tuple[bool, Dict]: 
                (success: bool, response_data: {
                    'post_id': str,
                    'message': str,
                    'timestamp': str,
                    'url': str
                } or {
                    'error': str,
                    'error_code': int,
                    'details': str
                })
        """
        
        # Validate credentials first
        is_valid, validation_msg = self.validate_credentials()
        if not is_valid:
            self.last_error = validation_msg
            return False, {
                'error': validation_msg,
                'error_code': 400,
                'details': 'Credentials validation failed'
            }
        
        # Validate message
        if not message or not str(message).strip():
            self.last_error = "❌ Message cannot be empty"
            return False, {
                'error': 'Message is empty',
                'error_code': 400,
                'details': 'Please provide caption text'
            }
        
        message = str(message).strip()
        
        # Build endpoint
        endpoint = f"{self.GRAPH_URL}/{self.page_id}/feed"
        
        # Build payload
        payload = {
            'message': message,
            'access_token': self.page_token
        }
        
        # Add media if provided
        if media_url:
            payload['picture'] = media_url
        
        try:
            # Make POST request to Facebook
            response = requests.post(
                endpoint,
                data=payload,
                timeout=self.REQUEST_TIMEOUT
            )
            
            # Parse response
            response_data = response.json()
            
            # Check for success (200 status code)
            if response.status_code == 200:
                post_id = response_data.get('id', 'unknown')
                self.last_post_id = post_id
                
                return True, {
                    'post_id': post_id,
                    'message': message[:100] + ('...' if len(message) > 100 else ''),
                    'timestamp': self._get_timestamp(),
                    'url': f"https://facebook.com/{post_id}"
                }
            
            # Handle errors from Facebook
            else:
                error_info = response_data.get('error', {})
                error_message = error_info.get('message', 'Unknown error from Facebook')
                error_code = error_info.get('code', response.status_code)
                error_type = error_info.get('type', 'Unknown')
                
                # Map common errors to user-friendly messages
                detailed_msg = self._interpret_error(error_code, error_message, error_type)
                
                self.last_error = detailed_msg
                
                return False, {
                    'error': f"❌ {detailed_msg}",
                    'error_code': error_code,
                    'details': error_message,
                    'error_type': error_type
                }
        
        except requests.exceptions.Timeout:
            error_msg = "❌ Request timed out (15 seconds). Facebook servers may be slow or unreachable."
            self.last_error = error_msg
            return False, {
                'error': error_msg,
                'error_code': 504,
                'details': 'Connection timeout - server did not respond in time'
            }
        
        except requests.exceptions.ConnectionError:
            error_msg = "❌ Connection failed. Please check internet and firewall."
            self.last_error = error_msg
            return False, {
                'error': error_msg,
                'error_code': 503,
                'details': 'Could not reach Facebook servers'
            }
        
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ Request error: {str(e)}"
            self.last_error = error_msg
            return False, {
                'error': error_msg,
                'error_code': 500,
                'details': str(e)
            }
        
        except json.JSONDecodeError:
            error_msg = "❌ Invalid response from Facebook (not JSON)"
            self.last_error = error_msg
            return False, {
                'error': error_msg,
                'error_code': 502,
                'details': 'Response could not be parsed'
            }
        
        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            self.last_error = error_msg
            return False, {
                'error': error_msg,
                'error_code': 500,
                'details': str(e)
            }
    
    def _interpret_error(self, error_code: int, error_message: str, error_type: str) -> str:
        """
        Map Facebook error codes to user-friendly messages.
        
        Args:
            error_code (int): Facebook error code
            error_message (str): Original error message
            error_type (str): Error type from Facebook
        
        Returns:
            str: User-friendly error message
        """
        
        error_map = {
            # Authentication errors
            190: "Invalid/expired token. Get a new token from Meta Developer Dashboard.",
            193: "Invalid token for this page. Verify Page ID matches token.",
            102: "Session invalidated. Your permissions may have been revoked.",
            283: "Token has insufficient permissions. Grant publish_pages permission.",
            
            # Permission errors
            200: "Insufficient permissions. Token needs: pages_read_engagement, publish_pages.",
            10: "User does not have permission to post on this page.",
            
            # Page/ID errors
            100: "Invalid Page ID. Check the numeric ID format (no dashes).",
            33: "This Page doesn't exist or is private.",
            
            # Rate limiting
            17: "Too many requests. Facebook is rate-limiting. Wait a few minutes.",
            4: "Too many requests from your IP. Try again after waiting.",
            
            # Content errors
            368: "The action blocked you. Check if page/token is still active.",
            506: "Action requires review. Try again later.",
        }
        
        # Get predefined message or build custom one
        if error_code in error_map:
            return error_map[error_code]
        
        # Build message from error_type and error_message
        if error_type == "OAuthException":
            return f"Authorization failed: {error_message}"
        elif error_type == "GraphMethodException":
            return f"Invalid API request: {error_message}"
        else:
            return f"Facebook error ({error_code}): {error_message}"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()


# Standalone function for easy integration
def publish_post(
    page_token: str,
    page_id: str,
    message: str,
    media_url: Optional[str] = None
) -> Tuple[bool, Dict]:
    """
    Standalone function to publish a post to Facebook Page.
    
    Perfect for quick integration into Streamlit apps.
    
    Args:
        page_token (str): Facebook Page Access Token
        page_id (str): Facebook Page ID
        message (str): Caption text
        media_url (str, optional): Image/video URL
    
    Returns:
        Tuple[bool, Dict]: (success, response_data)
    
    Example:
    --------
    success, result = publish_post(
        page_token="your_token_here",
        page_id="123456789",
        message="Hello Facebook! 🎉"
    )
    
    if success:
        print(f"✅ Posted! ID: {result['post_id']}")
    else:
        print(f"❌ Error: {result['error']}")
    """
    poster = FacebookPoster(page_token=page_token, page_id=page_id)
    return poster.publish_post(message=message, media_url=media_url)
