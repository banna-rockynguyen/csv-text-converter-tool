"""
GoHighLevel Integration Handler
Converts CSV data to GHL social media post format and handles batch operations
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from .ghl_api_client import GHLAPIClient, GHLBatchProcessor

logger = logging.getLogger(__name__)


class GHLIntegrationHandler:
    """Handles integration between CSV converter and GoHighLevel API"""
    
    def __init__(self, api_key: str, location_id: str):
        """
        Initialize GHL integration handler
        
        Args:
            api_key: GoHighLevel API key
            location_id: GoHighLevel location ID
        """
        self.ghl_client = GHLAPIClient(api_key, location_id)
        self.batch_processor = GHLBatchProcessor(self.ghl_client)
    
    def test_connection(self) -> Dict[str, Any]:
        """Test GHL API connection"""
        return self.ghl_client.test_connection()
    
    def convert_csv_to_ghl_posts(self, csv_data: List[Dict[str, Any]], 
                                platform: str = "LinkedIn") -> List[Dict[str, Any]]:
        """
        Convert CSV data to GHL social media post format
        
        Args:
            csv_data: List of CSV rows (dictionaries)
            platform: Target social media platform
            
        Returns:
            List of GHL-formatted post data
        """
        ghl_posts = []
        
        for i, row in enumerate(csv_data):
            try:
                ghl_post = self._convert_single_row_to_ghl(row, platform, i)
                if ghl_post:
                    ghl_posts.append(ghl_post)
            except Exception as e:
                logger.error(f"Error converting row {i}: {str(e)}")
                continue
        
        return ghl_posts
    
    def _convert_single_row_to_ghl(self, row: Dict[str, Any], 
                                  platform: str, index: int) -> Optional[Dict[str, Any]]:
        """
        Convert a single CSV row to GHL post format
        
        Args:
            row: CSV row data
            platform: Target platform
            index: Row index for scheduling
            
        Returns:
            GHL-formatted post data or None if conversion fails
        """
        try:
            # Extract basic post information
            content = self._extract_content(row)
            if not content:
                logger.warning(f"Row {index}: No content found, skipping")
                return None
            
            # Calculate scheduled time (spread posts over time)
            scheduled_time = self._calculate_scheduled_time(row, index)
            
            # Extract media URLs
            media_urls = self._extract_media_urls(row)
            
            # Extract tags and hashtags
            tags = self._extract_tags(row)
            
            # Create GHL post data
            ghl_post = {
                "platform": platform,
                "content": content,
                "scheduled_time": scheduled_time,
                "image_url": media_urls.get("image"),
                "video_url": media_urls.get("video"),
                "tags": tags,
                "utm_parameters": self._extract_utm_parameters(row),
                "post_type": self._determine_post_type(row),
                "engagement_settings": self._get_engagement_settings(platform)
            }
            
            return ghl_post
            
        except Exception as e:
            logger.error(f"Error converting row {index} to GHL format: {str(e)}")
            return None
    
    def _extract_content(self, row: Dict[str, Any]) -> str:
        """Extract and format post content"""
        # Try different content fields
        content_fields = ["content", "post_content", "text", "message", "description"]
        
        for field in content_fields:
            if field in row and row[field]:
                content = str(row[field]).strip()
                if content:
                    return self._format_content_for_platform(content)
        
        return ""
    
    def _format_content_for_platform(self, content: str) -> str:
        """Format content for specific platform requirements"""
        # Remove any remaining formatting tags
        content = content.replace("[BLOCK]", "").replace("[/BLOCK]", "")
        content = content.replace("[TITLE]", "").replace("[/TITLE]", "")
        content = content.replace("[HIGHLIGHT]", "").replace("[/HIGHLIGHT]", "")
        content = content.replace("[CTA]", "").replace("[/CTA]", "")
        content = content.replace("[HASHTAGS]", "").replace("[/HASHTAGS]", "")
        content = content.replace("[EMOJI]", "")
        
        # Clean up excessive whitespace
        import re
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = content.strip()
        
        return content
    
    def _extract_media_urls(self, row: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """Extract media URLs from row data"""
        media_urls = {
            "image": None,
            "video": None
        }
        
        # Check for image URL
        image_fields = ["image_url", "imageUrl", "image", "photo_url", "photo"]
        for field in image_fields:
            if field in row and row[field]:
                media_urls["image"] = str(row[field]).strip()
                break
        
        # Check for video URL
        video_fields = ["video_url", "videoUrl", "video", "media_url"]
        for field in video_fields:
            if field in row and row[field]:
                media_urls["video"] = str(row[field]).strip()
                break
        
        return media_urls
    
    def _extract_tags(self, row: Dict[str, Any]) -> str:
        """Extract and format tags"""
        tag_fields = ["tags", "hashtags", "keywords", "categories"]
        
        for field in tag_fields:
            if field in row and row[field]:
                tags = str(row[field]).strip()
                if tags:
                    return self._format_tags(tags)
        
        return ""
    
    def _format_tags(self, tags: str) -> str:
        """Format tags for social media"""
        # Split by comma and clean up
        tag_list = [tag.strip() for tag in tags.split(",")]
        
        # Ensure hashtags start with #
        formatted_tags = []
        for tag in tag_list:
            if tag and not tag.startswith("#"):
                formatted_tags.append(f"#{tag}")
            elif tag:
                formatted_tags.append(tag)
        
        return ", ".join(formatted_tags)
    
    def _extract_utm_parameters(self, row: Dict[str, Any]) -> Dict[str, str]:
        """Extract UTM parameters from row data"""
        utm_params = {}
        
        utm_fields = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"]
        
        for field in utm_fields:
            if field in row and row[field]:
                utm_params[field] = str(row[field]).strip()
        
        return utm_params
    
    def _determine_post_type(self, row: Dict[str, Any]) -> str:
        """Determine post type based on content"""
        content = self._extract_content(row).lower()
        
        if "poll" in content or "câu hỏi" in content:
            return "poll"
        elif "carousel" in content or "slide" in content:
            return "carousel"
        elif "story" in content or "câu chuyện" in content:
            return "story"
        elif "quote" in content or "trích dẫn" in content:
            return "quote"
        elif "listing" in content or "danh sách" in content:
            return "listing"
        else:
            return "text"
    
    def _get_engagement_settings(self, platform: str) -> Dict[str, Any]:
        """Get platform-specific engagement settings"""
        settings = {
            "allow_comments": True,
            "allow_shares": True,
            "allow_likes": True
        }
        
        if platform.lower() == "linkedin":
            settings.update({
                "visibility": "public",
                "allow_reshares": True
            })
        elif platform.lower() == "facebook":
            settings.update({
                "allow_reactions": True,
                "allow_shares": True
            })
        elif platform.lower() == "instagram":
            settings.update({
                "allow_comments": True,
                "story_highlights": True
            })
        
        return settings
    
    def _calculate_scheduled_time(self, row: Dict[str, Any], index: int) -> str:
        """Calculate scheduled time for post"""
        # Check if there's a specific scheduled time in the data
        if "scheduled_time" in row and row["scheduled_time"]:
            return str(row["scheduled_time"])
        
        if "ngay" in row and row["ngay"]:
            try:
                # Parse Vietnamese date format (dd/mm/yyyy)
                date_str = str(row["ngay"])
                if "/" in date_str:
                    day, month, year = date_str.split("/")
                    scheduled_date = datetime(int(year), int(month), int(day))
                    # Add some time variation (9 AM + index hours)
                    scheduled_time = scheduled_date.replace(hour=9 + (index % 8), minute=0)
                    return scheduled_time.isoformat()
            except Exception:
                pass
        
        # Default: schedule posts starting from tomorrow, spread over time
        base_time = datetime.now() + timedelta(days=1)
        scheduled_time = base_time + timedelta(hours=index * 2)  # 2 hours apart
        
        return scheduled_time.isoformat()
    
    def create_posts_in_ghl(self, csv_data: List[Dict[str, Any]], 
                           platform: str = "LinkedIn") -> Dict[str, Any]:
        """
        Convert CSV data and create posts in GoHighLevel
        
        Args:
            csv_data: List of CSV rows
            platform: Target platform
            
        Returns:
            Dict with creation results
        """
        try:
            # Convert CSV data to GHL format
            ghl_posts = self.convert_csv_to_ghl_posts(csv_data, platform)
            
            if not ghl_posts:
                return {
                    "success": False,
                    "message": "No valid posts found in CSV data",
                    "total_posts": 0,
                    "created_posts": 0
                }
            
            # Create posts in GHL
            batch_results = self.batch_processor.create_multiple_posts(ghl_posts)
            
            return {
                "success": True,
                "message": f"Successfully processed {batch_results['successful']} out of {batch_results['total_posts']} posts",
                "total_posts": batch_results["total_posts"],
                "created_posts": batch_results["successful"],
                "failed_posts": batch_results["failed"],
                "results": batch_results["results"]
            }
            
        except Exception as e:
            logger.error(f"Error creating posts in GHL: {str(e)}")
            return {
                "success": False,
                "message": f"Error creating posts: {str(e)}",
                "error": str(e)
            }
    
    def get_existing_posts(self, limit: int = 50) -> Dict[str, Any]:
        """Get existing social media posts from GHL"""
        return self.ghl_client.get_social_media_posts(limit)
    
    def delete_post(self, post_id: str) -> Dict[str, Any]:
        """Delete a specific post from GHL"""
        return self.ghl_client.delete_social_media_post(post_id)
