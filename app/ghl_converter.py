"""
GoHighLevel Converter Module
Converts simple format (Date|Time|Content|ImageURL|Link) to GoHighLevel template format
"""

from typing import List, Dict, Any
from datetime import datetime
import re


class GHLConverter:
    """Converts simple social media data to GoHighLevel format"""
    
    def __init__(self):
        # Platform headers (first row)
        self.platform_headers = [
            'All Social', 'All Social', 'All Social', 'All Social', 'All Social', 'All Social', 'All Social', 'All Social', 'All Social', 'All Social', 'All Social',
            'Facebook', 'Instagram', 'LinkedIn', 'LinkedIn',
            'Google (GBP)', 'Google (GBP)', 'Google (GBP)', 'Google (GBP)', 'Google (GBP)', 'Google (GBP)', 'Google (GBP)', 'Google (GBP)', 'Google (GBP)', 'Google (GBP)',
            'YouTube', 'YouTube', 'YouTube',
            'TikTok', 'TikTok', 'TikTok', 'TikTok', 'TikTok', 'TikTok', 'TikTok',
            'Community', 'Community',
            'Pinterest', 'Pinterest'
        ]
        
        # Field headers (second row)
        self.ghl_headers = [
            'postAtSpecificTime (YYYY-MM-DD HH:mm:ss)',
            'content',
            'OGmetaUrl (url)',
            'imageUrls (comma-separated)',
            'gifUrl',
            'videoUrls (comma-separated)',
            'mediaOptimization (true/false)',
            'applyWatermark (true/false)',
            'tags (comma-separated)',
            'category',
            'followUpComment',
            'type (post/story/reel)',
            'type (post/story/reel)',
            'pdfTitle',
            'postAsPdf (true/false)',
            'eventType (call_to_action/event/offer)',
            'actionType (none/order/book/shop/learn_more/call/sign_up)',
            'title',
            'offerTitle',
            'startDate (YYYY-MM-DD HH:mm:ss)',
            'endDate (YYYY-MM-DD HH:mm:ss)',
            'termsConditions',
            'couponCode',
            'redeemOnlineUrl',
            'actionUrl',
            'title',
            'privacyLevel (private/public/unlisted)',
            'type (video/short)',
            'privacyLevel (everyone/friends/only_me)',
            'promoteOtherBrand (true/false)',
            'enableComment (true/false)',
            'enableDuet (true/false)',
            'enableStitch (true/false)',
            'videoDisclosure (true/false)',
            'promoteYourBrand (true/false)',
            'title',
            'notifyAllGroupMembers (true/false)',
            'title',
            'link'
        ]
    
    def convert_simple_to_ghl(self, simple_data: List[List[str]]) -> Dict[str, Any]:
        """
        Convert simple format data to GoHighLevel format
        
        Args:
            simple_data: List of rows with [Date, Time, Content, ImageURL, Link]
            
        Returns:
            Dictionary with converted data and metadata
        """
        if not simple_data or len(simple_data) < 2:
            return {
                'success': False,
                'error': 'No data provided or insufficient data',
                'data': [],
                'headers': []
            }
        
        # Extract headers (first row)
        simple_headers = simple_data[0]
        simple_rows = simple_data[1:]
        
        # Validate simple format
        if len(simple_headers) < 5:
            return {
                'success': False,
                'error': 'Simple format must have at least 5 columns: Date, Time, Content, ImageURL, Link',
                'data': [],
                'headers': []
            }
        
        # Convert each row
        converted_rows = []
        for row in simple_rows:
            if len(row) < 5:
                # Pad with empty strings if row is too short
                row.extend([''] * (5 - len(row)))
            
            converted_row = self._convert_single_row(row)
            converted_rows.append(converted_row)
        
        return {
            'success': True,
            'data': converted_rows,
            'headers': self.ghl_headers,
            'platform_headers': self.platform_headers,
            'original_format': 'simple',
            'converted_format': 'goHighLevel',
            'row_count': len(converted_rows),
            'column_count': len(self.ghl_headers)
        }
    
    def _convert_single_row(self, row: List[str]) -> List[str]:
        """
        Convert a single row from simple format to GoHighLevel format
        
        Args:
            row: [Date, Time, Content, ImageURL, Link]
            
        Returns:
            List of 40 GoHighLevel fields
        """
        date = row[0].strip() if len(row) > 0 else ''
        time = row[1].strip() if len(row) > 1 else ''
        content = row[2].strip() if len(row) > 2 else ''
        image_url = row[3].strip() if len(row) > 3 else ''
        link = row[4].strip() if len(row) > 4 else ''
        
        # Combine date and time
        post_time = self._combine_date_time(date, time)
        
        # Extract hashtags from content
        hashtags = self._extract_hashtags(content)
        
        # Determine post type based on content
        post_type = self._determine_post_type(content)
        
        # Create GoHighLevel row
        ghl_row = [
            post_time,  # postAtSpecificTime
            content,    # content
            link,       # OGmetaUrl
            image_url,  # imageUrls
            '',         # gifUrl
            '',         # videoUrls
            'TRUE',     # mediaOptimization
            'FALSE',    # applyWatermark
            hashtags,   # tags
            'Social Media',  # category
            '',         # followUpComment
            post_type,  # type (post/story/reel)
            post_type,  # type (post/story/reel)
            '',         # pdfTitle
            'FALSE',    # postAsPdf
            'call_to_action',  # eventType
            'learn_more',      # actionType
            self._extract_title(content),  # title
            '',         # offerTitle
            '',         # startDate
            '',         # endDate
            '',         # termsConditions
            '',         # couponCode
            '',         # redeemOnlineUrl
            link,       # actionUrl
            self._extract_title(content),  # title
            'public',   # privacyLevel
            'video' if 'video' in content.lower() else 'short',  # type
            'everyone', # privacyLevel
            'FALSE',    # promoteOtherBrand
            'TRUE',     # enableComment
            'FALSE',    # enableDuet
            'FALSE',    # enableStitch
            'FALSE',    # videoDisclosure
            'TRUE',     # promoteYourBrand
            self._extract_title(content),  # title
            'FALSE',    # notifyAllGroupMembers
            self._extract_title(content),  # title
            link        # link
        ]
        
        return ghl_row
    
    def _combine_date_time(self, date: str, time: str) -> str:
        """Combine date and time into GoHighLevel format"""
        if not date or not time:
            return ''
        
        try:
            # Handle different date formats
            if '/' in date:
                # MM/DD/YYYY or DD/MM/YYYY format
                date_parts = date.split('/')
                if len(date_parts) == 3:
                    # Assume DD/MM/YYYY for Vietnamese format
                    day, month, year = date_parts
                    date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            elif '-' in date and len(date.split('-')[0]) == 4:
                # Already in YYYY-MM-DD format
                pass
            else:
                return ''
            
            # Handle time format
            if ':' in time:
                time_parts = time.split(':')
                if len(time_parts) >= 2:
                    hour = time_parts[0].zfill(2)
                    minute = time_parts[1].zfill(2)
                    second = time_parts[2].zfill(2) if len(time_parts) > 2 else '00'
                    time = f"{hour}:{minute}:{second}"
                else:
                    return ''
            else:
                return ''
            
            return f"{date} {time}"
        except:
            return ''
    
    def _extract_hashtags(self, content: str) -> str:
        """Extract hashtags from content"""
        hashtags = re.findall(r'#\w+', content)
        return ','.join(hashtags) if hashtags else ''
    
    def _determine_post_type(self, content: str) -> str:
        """Determine post type based on content"""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['story', 'stories', 'tin nổi bật']):
            return 'story'
        elif any(keyword in content_lower for keyword in ['reel', 'video ngắn', 'tiktok']):
            return 'reel'
        else:
            return 'post'
    
    def _extract_title(self, content: str) -> str:
        """Extract title from content (first line or first sentence)"""
        # Remove hashtags and mentions for title
        clean_content = re.sub(r'#\w+', '', content)
        clean_content = re.sub(r'@\w+', '', clean_content)
        clean_content = clean_content.strip()
        
        # Get first line or first sentence
        lines = clean_content.split('\n')
        first_line = lines[0].strip()
        
        # If first line is too long, truncate
        if len(first_line) > 100:
            first_line = first_line[:97] + '...'
        
        return first_line if first_line else 'Social Media Post'
    
    def validate_simple_format(self, data: List[List[str]]) -> Dict[str, Any]:
        """Validate simple format data"""
        issues = []
        warnings = []
        
        if not data:
            issues.append("No data provided")
            return {'valid': False, 'issues': issues, 'warnings': warnings}
        
        if len(data) < 2:
            issues.append("Need at least header row and one data row")
            return {'valid': False, 'issues': issues, 'warnings': warnings}
        
        headers = data[0]
        if len(headers) < 5:
            issues.append("Simple format requires at least 5 columns: Date, Time, Content, ImageURL, Link")
        
        # Check data rows
        for i, row in enumerate(data[1:], 1):
            if len(row) < 5:
                warnings.append(f"Row {i}: Missing columns, padding with empty values")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
