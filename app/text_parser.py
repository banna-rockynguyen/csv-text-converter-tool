"""
Text parser module for CSV Text Converter Tool
Handles parsing of various text formats and converting to structured data
"""

import re
import csv
import io
from typing import List, Dict, Any, Optional
from .delimiter_detector import DelimiterDetector


class TextParser:
    """Parses text data and converts it to structured format"""
    
    def __init__(self):
        self.delimiter_detector = DelimiterDetector()
    
    def parse_text_to_csv_data(self, text: str, delimiter: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse text data and convert to CSV format
        
        Args:
            text: Input text data
            delimiter: Optional delimiter to use (if None, auto-detect)
            
        Returns:
            Dictionary containing parsed data and metadata
        """
        if not text or not text.strip():
            return {
                'success': False,
                'error': 'Empty text provided',
                'data': [],
                'headers': [],
                'delimiter': None
            }
        
        # Auto-detect delimiter if not provided
        if delimiter is None:
            delimiter, confidence, all_scores = self.delimiter_detector.detect_delimiter(text)
            if confidence < 0.1:
                return {
                    'success': False,
                    'error': f'Could not detect a reliable delimiter. Best guess: "{delimiter}" (confidence: {confidence:.2f})',
                    'data': [],
                    'headers': [],
                    'delimiter': delimiter,
                    'confidence': confidence,
                    'all_scores': all_scores
                }
        else:
            confidence = 1.0
            all_scores = {delimiter: 1.0}
        
        # Parse the text
        try:
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            if not lines:
                return {
                    'success': False,
                    'error': 'No valid lines found in text',
                    'data': [],
                    'headers': [],
                    'delimiter': delimiter
                }
            
            # Parse each line
            parsed_data = []
            for line in lines:
                # Handle quoted fields that might contain the delimiter
                parsed_line = self._parse_line_with_quotes(line, delimiter)
                parsed_data.append(parsed_line)
            
            # Extract headers (first row)
            headers = parsed_data[0] if parsed_data else []
            data_rows = parsed_data[1:] if len(parsed_data) > 1 else []
            
            # Clean headers
            headers = [self._clean_field(header) for header in headers]
            
            # Clean data
            cleaned_data = []
            for row in data_rows:
                cleaned_row = [self._clean_field(field) for field in row]
                cleaned_data.append(cleaned_row)
            
            return {
                'success': True,
                'data': cleaned_data,
                'headers': headers,
                'delimiter': delimiter,
                'confidence': confidence,
                'all_scores': all_scores,
                'row_count': len(cleaned_data),
                'column_count': len(headers)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error parsing text: {str(e)}',
                'data': [],
                'headers': [],
                'delimiter': delimiter
            }
    
    def _parse_line_with_quotes(self, line: str, delimiter: str) -> List[str]:
        """
        Parse a line handling quoted fields that might contain the delimiter
        
        Args:
            line: Line to parse
            delimiter: Delimiter to use
            
        Returns:
            List of parsed fields
        """
        # Use Python's csv module for robust parsing
        reader = csv.reader(io.StringIO(line), delimiter=delimiter)
        try:
            return next(reader)
        except StopIteration:
            return []
    
    def _clean_field(self, field: str) -> str:
        """
        Clean a field value
        
        Args:
            field: Field value to clean
            
        Returns:
            Cleaned field value
        """
        if field is None:
            return ''
        
        # Convert to string and strip whitespace
        field = str(field).strip()
        
        # Remove surrounding quotes if they exist
        if len(field) >= 2 and field[0] == field[-1] and field[0] in ['"', "'"]:
            field = field[1:-1]
        
        return field
    
    def generate_csv_content(self, headers: List[str], data: List[List[str]], delimiter: str = ',', platform_headers: List[str] = None) -> str:
        """
        Generate CSV content from headers and data with UTF-8 support
        
        Args:
            headers: List of column headers
            data: List of data rows
            delimiter: Delimiter to use (default: comma)
            platform_headers: Optional platform headers (first row)
            
        Returns:
            CSV content as string with UTF-8 BOM for Excel compatibility
        """
        output = io.StringIO()
        # Use QUOTE_MINIMAL to match GoHighLevel sample format (no quotes around simple fields)
        writer = csv.writer(output, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        
        # Write platform headers if provided (for GoHighLevel format)
        if platform_headers:
            writer.writerow(platform_headers)
        
        # Write field headers
        writer.writerow(headers)
        
        # Write data rows
        for row in data:
            writer.writerow(row)
        
        # Add UTF-8 BOM for better Excel/GoHighLevel compatibility
        content = output.getvalue()
        return '\ufeff' + content
    
    def validate_data(self, headers: List[str], data: List[List[str]]) -> Dict[str, Any]:
        """
        Validate the parsed data with GoHighLevel specific validation
        
        Args:
            headers: List of column headers
            data: List of data rows
            
        Returns:
            Validation results
        """
        issues = []
        warnings = []
        
        if not headers:
            issues.append("No headers found")
            return {'valid': False, 'issues': issues, 'warnings': warnings}
        
        if not data:
            warnings.append("No data rows found")
            return {'valid': True, 'issues': issues, 'warnings': warnings}
        
        # Check for consistent column count
        expected_columns = len(headers)
        inconsistent_rows = []
        
        for i, row in enumerate(data):
            if len(row) != expected_columns:
                inconsistent_rows.append({
                    'row': i + 1,
                    'expected': expected_columns,
                    'actual': len(row)
                })
        
        if inconsistent_rows:
            issues.append(f"Found {len(inconsistent_rows)} rows with inconsistent column count")
        
        # Check for empty headers
        empty_headers = [i for i, header in enumerate(headers) if not header.strip()]
        if empty_headers:
            warnings.append(f"Found {len(empty_headers)} empty headers at positions: {empty_headers}")
        
        # Check for completely empty rows
        empty_rows = [i for i, row in enumerate(data) if all(not field.strip() for field in row)]
        if empty_rows:
            warnings.append(f"Found {len(empty_rows)} completely empty rows at positions: {empty_rows}")
        
        # GoHighLevel specific validations
        ghl_validation = self._validate_ghl_format(headers, data)
        issues.extend(ghl_validation['issues'])
        warnings.extend(ghl_validation['warnings'])
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'inconsistent_rows': inconsistent_rows,
            'empty_headers': empty_headers,
            'empty_rows': empty_rows,
            'ghl_validation': ghl_validation
        }
    
    def _validate_ghl_format(self, headers: List[str], data: List[List[str]]) -> Dict[str, Any]:
        """
        Validate data for GoHighLevel format compatibility
        
        Args:
            headers: List of column headers
            data: List of data rows
            
        Returns:
            GoHighLevel specific validation results
        """
        issues = []
        warnings = []
        
        # GoHighLevel expected headers (from sample)
        expected_headers = [
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
        
        # Check if this looks like GoHighLevel format
        is_ghl_format = len(headers) >= 10 and any('postAtSpecificTime' in h for h in headers)
        
        if is_ghl_format:
            # Validate date formats
            date_headers = [i for i, h in enumerate(headers) if 'Date' in h or 'Time' in h]
            for row_idx, row in enumerate(data):
                for col_idx in date_headers:
                    if col_idx < len(row) and row[col_idx].strip():
                        if not self._is_valid_date_format(row[col_idx]):
                            warnings.append(f"Row {row_idx + 1}, Column {col_idx + 1}: Invalid date format '{row[col_idx]}'. Expected: YYYY-MM-DD HH:mm:ss")
            
            # Validate boolean fields
            boolean_headers = [i for i, h in enumerate(headers) if 'true/false' in h.lower()]
            for row_idx, row in enumerate(data):
                for col_idx in boolean_headers:
                    if col_idx < len(row) and row[col_idx].strip():
                        if row[col_idx].lower() not in ['true', 'false', '']:
                            warnings.append(f"Row {row_idx + 1}, Column {col_idx + 1}: Invalid boolean value '{row[col_idx]}'. Expected: true/false")
            
            # Validate URL fields
            url_headers = [i for i, h in enumerate(headers) if 'url' in h.lower()]
            for row_idx, row in enumerate(data):
                for col_idx in url_headers:
                    if col_idx < len(row) and row[col_idx].strip():
                        if not self._is_valid_url(row[col_idx]):
                            warnings.append(f"Row {row_idx + 1}, Column {col_idx + 1}: Invalid URL format '{row[col_idx]}'")
        
        return {
            'is_ghl_format': is_ghl_format,
            'issues': issues,
            'warnings': warnings
        }
    
    def _is_valid_date_format(self, date_str: str) -> bool:
        """Check if date string matches YYYY-MM-DD HH:mm:ss format"""
        import re
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        return bool(re.match(pattern, date_str.strip()))
    
    def _is_valid_url(self, url_str: str) -> bool:
        """Check if string is a valid URL"""
        import re
        pattern = r'^https?://[^\s]+$'
        return bool(re.match(pattern, url_str.strip()))
