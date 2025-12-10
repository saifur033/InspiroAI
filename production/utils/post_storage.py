"""
Persistent storage for scheduled posts
Saves to JSON file so posts persist across app restarts
"""
import json
import os
from datetime import datetime
from pathlib import Path


class PostStorage:
    """Handle persistent storage of scheduled posts"""
    
    STORAGE_FILE = "scheduled_posts.json"
    
    @staticmethod
    def get_storage_path():
        """Get the path to the storage file"""
        return os.path.join(os.path.dirname(__file__), "..", "scheduled_posts.json")
    
    @staticmethod
    def load_posts():
        """Load scheduled posts from file"""
        try:
            storage_path = PostStorage.get_storage_path()
            
            if not os.path.exists(storage_path):
                return []
            
            with open(storage_path, 'r') as f:
                data = json.load(f)
            
            # Convert datetime strings back to datetime objects
            for post in data:
                if 'scheduled_dt' in post and isinstance(post['scheduled_dt'], str):
                    post['scheduled_dt'] = datetime.fromisoformat(post['scheduled_dt'])
                if 'created_at' in post and isinstance(post['created_at'], str):
                    post['created_at'] = datetime.fromisoformat(post['created_at'])
                if 'posted_at' in post and isinstance(post['posted_at'], str):
                    post['posted_at'] = datetime.fromisoformat(post['posted_at'])
            
            return data
        except Exception as e:
            print(f"Error loading posts: {e}")
            return []
    
    @staticmethod
    def save_posts(posts):
        """Save scheduled posts to file"""
        try:
            storage_path = PostStorage.get_storage_path()
            
            # Convert datetime objects to ISO format strings for JSON serialization
            serialized_posts = []
            for post in posts:
                post_copy = post.copy()
                if 'scheduled_dt' in post_copy and isinstance(post_copy['scheduled_dt'], datetime):
                    post_copy['scheduled_dt'] = post_copy['scheduled_dt'].isoformat()
                if 'created_at' in post_copy and isinstance(post_copy['created_at'], datetime):
                    post_copy['created_at'] = post_copy['created_at'].isoformat()
                if 'posted_at' in post_copy and isinstance(post_copy['posted_at'], datetime):
                    post_copy['posted_at'] = post_copy['posted_at'].isoformat()
                serialized_posts.append(post_copy)
            
            with open(storage_path, 'w') as f:
                json.dump(serialized_posts, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving posts: {e}")
            return False
    
    @staticmethod
    def add_post(post):
        """Add a new post and save"""
        posts = PostStorage.load_posts()
        posts.append(post)
        PostStorage.save_posts(posts)
        return posts
    
    @staticmethod
    def update_post(post_id, updated_post):
        """Update an existing post and save"""
        posts = PostStorage.load_posts()
        for i, post in enumerate(posts):
            if post['id'] == post_id:
                posts[i] = updated_post
                PostStorage.save_posts(posts)
                return posts
        return posts
    
    @staticmethod
    def delete_post(post_id):
        """Delete a post and save"""
        posts = PostStorage.load_posts()
        posts = [p for p in posts if p['id'] != post_id]
        PostStorage.save_posts(posts)
        return posts
    
    @staticmethod
    def clear_old_posts(days=7):
        """Remove posts older than specified days"""
        try:
            posts = PostStorage.load_posts()
            now = datetime.now()
            
            # Keep posts that are recent or have status 'Pending'
            filtered_posts = [
                p for p in posts
                if p.get('status') == 'Pending' or 
                   (p.get('posted_at') and 
                    (now - datetime.fromisoformat(p['posted_at'])).days < days)
            ]
            
            PostStorage.save_posts(filtered_posts)
            return filtered_posts
        except Exception as e:
            print(f"Error clearing old posts: {e}")
            return posts
