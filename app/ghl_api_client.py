"""
GoHighLevel API Client for Social Media Integration
Handles authentication and social media post creation
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GHLAPIClient:
    """GoHighLevel API Client for social media operations"""
    
    def __init__(self, api_key: str, location_id: str):
        """
        Initialize GHL API client
        
        Args:
            api_key: GoHighLevel API key
            location_id: GoHighLevel location ID
        """
        self.api_key = api_key
        self.location_id = location_id
        self.base_url = "https://services.leadconnectorhq.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Version": "2021-07-28"
        }
        
    def test_connection(self) -> Dict[str, Any]:
        """
        Test API connection and authentication
        
        Returns:
            Dict with connection status and location info
        """
        try:
            url = f"{self.base_url}/locations/{self.location_id}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                location_data = response.json()
                return {
                    "success": True,
                    "message": "Connection successful",
                    "location_name": location_data.get("name", "Unknown"),
                    "location_id": self.location_id
                }
            else:
                return {
                    "success": False,
                    "message": f"API Error: {response.status_code} - {response.text}",
                    "error_code": response.status_code
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}",
                "error": str(e)
            }
    
    def create_social_media_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a social media post in GoHighLevel
        
        Args:
            post_data: Post data including content, platform, scheduled time, etc.
            
        Returns:
            Dict with creation status and post ID
        """
        try:
            # Prepare the post payload for GHL API
            payload = self._prepare_post_payload(post_data)
            
            # GHL API endpoint for social media posts
            url = f"{self.base_url}/locations/{self.location_id}/social-media/posts"
            
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code in [200, 201]:
                response_data = response.json()
                return {
                    "success": True,
                    "message": "Post created successfully",
                    "post_id": response_data.get("id"),
                    "platform": post_data.get("platform", "Unknown"),
                    "scheduled_time": post_data.get("scheduled_time")
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to create post: {response.status_code} - {response.text}",
                    "error_code": response.status_code,
                    "error_details": response.text
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error creating post: {str(e)}",
                "error": str(e)
            }
    
    def _prepare_post_payload(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare post data for GHL API format
        
        Args:
            post_data: Raw post data from our CSV converter
            
        Returns:
            Formatted payload for GHL API
        """
        # Map our CSV fields to GHL API format
        payload = {
            "platform": self._map_platform(post_data.get("platform", "LinkedIn")),
            "content": post_data.get("content", ""),
            "mediaUrls": self._extract_media_urls(post_data),
            "scheduledTime": self._format_scheduled_time(post_data.get("scheduled_time")),
            "status": "scheduled",  # or "draft" for draft posts
            "tags": self._extract_tags(post_data.get("tags", "")),
            "locationId": self.location_id
        }
        
        # Add platform-specific fields
        if payload["platform"] == "linkedin":
            payload["linkedinSettings"] = {
                "visibility": "public",
                "allowComments": True
            }
        elif payload["platform"] == "facebook":
            payload["facebookSettings"] = {
                "allowComments": True,
                "allowShares": True
            }
        elif payload["platform"] == "instagram":
            payload["instagramSettings"] = {
                "caption": post_data.get("content", ""),
                "hashtags": self._extract_hashtags(post_data.get("tags", ""))
            }
        
        return payload
    
    def _map_platform(self, platform: str) -> str:
        """Map platform names to GHL API format"""
        platform_mapping = {
            "LinkedIn": "linkedin",
            "Facebook": "facebook", 
            "Instagram": "instagram",
            "TikTok": "tiktok",
            "Twitter": "twitter"
        }
        return platform_mapping.get(platform, "linkedin")
    
    def _extract_media_urls(self, post_data: Dict[str, Any]) -> List[str]:
        """Extract media URLs from post data"""
        media_urls = []
        
        # Check for image URL
        if post_data.get("image_url"):
            media_urls.append(post_data["image_url"])
        
        # Check for video URL
        if post_data.get("video_url"):
            media_urls.append(post_data["video_url"])
            
        return media_urls
    
    def _format_scheduled_time(self, scheduled_time: Optional[str]) -> Optional[str]:
        """Format scheduled time for GHL API"""
        if not scheduled_time:
            return None
            
        try:
            # Parse the scheduled time and format for GHL API
            # GHL expects ISO 8601 format
            if isinstance(scheduled_time, str):
                # Try to parse various date formats
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"]:
                    try:
                        dt = datetime.strptime(scheduled_time, fmt)
                        return dt.isoformat() + "Z"
                    except ValueError:
                        continue
            
            return scheduled_time
        except Exception:
            return None
    
    def _extract_tags(self, tags_string: str) -> List[str]:
        """Extract tags from comma-separated string"""
        if not tags_string:
            return []
        
        tags = [tag.strip() for tag in tags_string.split(",")]
        return [tag for tag in tags if tag]
    
    def _extract_hashtags(self, tags_string: str) -> List[str]:
        """Extract hashtags from tags string"""
        tags = self._extract_tags(tags_string)
        hashtags = []
        
        for tag in tags:
            if tag.startswith("#"):
                hashtags.append(tag)
            else:
                hashtags.append(f"#{tag}")
        
        return hashtags
    
    def get_social_media_posts(self, limit: int = 50) -> Dict[str, Any]:
        """
        Get existing social media posts from GHL
        
        Args:
            limit: Maximum number of posts to retrieve
            
        Returns:
            Dict with posts data
        """
        try:
            url = f"{self.base_url}/locations/{self.location_id}/social-media/posts"
            params = {"limit": limit}
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "posts": response.json().get("posts", []),
                    "total": len(response.json().get("posts", []))
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to retrieve posts: {response.status_code} - {response.text}",
                    "error_code": response.status_code
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving posts: {str(e)}",
                "error": str(e)
            }
    
    def delete_social_media_post(self, post_id: str) -> Dict[str, Any]:
        """
        Delete a social media post from GHL
        
        Args:
            post_id: ID of the post to delete
            
        Returns:
            Dict with deletion status
        """
        try:
            url = f"{self.base_url}/locations/{self.location_id}/social-media/posts/{post_id}"
            
            response = requests.delete(url, headers=self.headers)
            
            if response.status_code in [200, 204]:
                return {
                    "success": True,
                    "message": "Post deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to delete post: {response.status_code} - {response.text}",
                    "error_code": response.status_code
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting post: {str(e)}",
                "error": str(e)
            }


class GHLBatchProcessor:
    """Handle batch operations for multiple social media posts"""
    
    def __init__(self, ghl_client: GHLAPIClient):
        self.ghl_client = ghl_client
        self.results = []
    
    def create_multiple_posts(self, posts_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple social media posts
        
        Args:
            posts_data: List of post data dictionaries
            
        Returns:
            Dict with batch creation results
        """
        results = {
            "total_posts": len(posts_data),
            "successful": 0,
            "failed": 0,
            "results": []
        }
        
        for i, post_data in enumerate(posts_data):
            logger.info(f"Creating post {i+1}/{len(posts_data)}")
            
            result = self.ghl_client.create_social_media_post(post_data)
            results["results"].append({
                "post_index": i + 1,
                "platform": post_data.get("platform", "Unknown"),
                "success": result["success"],
                "message": result["message"],
                "post_id": result.get("post_id")
            })
            
            if result["success"]:
                results["successful"] += 1
            else:
                results["failed"] += 1
        
        return results
