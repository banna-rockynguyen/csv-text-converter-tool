"""
Delimiter detection module for CSV Text Converter Tool
Automatically detects the most likely delimiter used in text data
"""

import re
from collections import Counter
from typing import List, Tuple, Optional


class DelimiterDetector:
    """Detects the most likely delimiter in text data"""
    
    # Common delimiters to check (ordered by priority)
    COMMON_DELIMITERS = ['|', '\t', ',', ';', ':', ' ', '~', '^', '#', '$', '%', '&', '*', '+', '=', '@']
    
    # GoHighLevel specific delimiters (higher priority)
    GHL_DELIMITERS = ['|', '\t', ',', ';']
    
    def __init__(self):
        self.delimiter_scores = {}
    
    def detect_delimiter(self, text: str) -> Tuple[str, float, dict]:
        """
        Detect the most likely delimiter in the given text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (best_delimiter, confidence_score, all_scores)
        """
        if not text or not text.strip():
            return ',', 0.0, {}
        
        # Clean the text
        text = text.strip()
        
        # Split into lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return ',', 0.0, {}
        
        # Check if this looks like GoHighLevel format first
        is_ghl_format = self._is_ghl_format(text)
        
        # Calculate scores for each delimiter
        scores = {}
        delimiters_to_check = self.GHL_DELIMITERS if is_ghl_format else self.COMMON_DELIMITERS
        
        for delimiter in delimiters_to_check:
            score = self._calculate_delimiter_score(lines, delimiter)
            # Give bonus for GHL delimiters if it's GHL format
            if is_ghl_format and delimiter in self.GHL_DELIMITERS:
                score *= 1.2
            scores[delimiter] = score
        
        # Special handling: if we have a clear header row, give it extra weight
        if len(lines) >= 2:
            header_score = self._calculate_header_delimiter_score(lines[0], lines[1:])
            for delimiter in scores:
                if delimiter in header_score:
                    # Give much more weight to header analysis for structured data
                    if header_score[delimiter] > 0.5:  # If header analysis is confident
                        scores[delimiter] = header_score[delimiter] * 0.9 + scores[delimiter] * 0.1
                    else:
                        scores[delimiter] = max(scores[delimiter], header_score[delimiter])
        
        # Find the best delimiter
        best_delimiter = max(scores, key=scores.get)
        best_score = scores[best_delimiter]
        
        return best_delimiter, best_score, scores
    
    def _calculate_delimiter_score(self, lines: List[str], delimiter: str) -> float:
        """
        Calculate a score for a specific delimiter based on consistency and frequency
        
        Args:
            lines: List of text lines
            delimiter: Delimiter to test
            
        Returns:
            Score between 0 and 1
        """
        if not lines:
            return 0.0
        
        # Count occurrences of delimiter in each line
        delimiter_counts = []
        for line in lines:
            count = line.count(delimiter)
            delimiter_counts.append(count)
        
        # If no delimiter found in any line, return 0
        if all(count == 0 for count in delimiter_counts):
            return 0.0
        
        # Calculate consistency score
        # More consistent counts across lines = higher score
        if len(set(delimiter_counts)) == 1 and delimiter_counts[0] > 0:
            consistency_score = 1.0
        else:
            # Calculate variance - lower variance = higher consistency
            mean_count = sum(delimiter_counts) / len(delimiter_counts)
            if mean_count == 0:
                consistency_score = 0.0
            else:
                variance = sum((count - mean_count) ** 2 for count in delimiter_counts) / len(delimiter_counts)
                consistency_score = max(0, 1 - (variance / (mean_count + 1)))
        
        # Calculate frequency score
        # More frequent delimiters get higher scores, but not too high
        total_delimiters = sum(delimiter_counts)
        total_chars = sum(len(line) for line in lines)
        frequency_score = min(0.8, total_delimiters / (total_chars + 1))  # Cap at 0.8
        
        # Calculate structure score
        # Check if delimiter creates reasonable number of columns
        avg_columns = sum(delimiter_counts) / len(delimiter_counts) + 1
        if 2 <= avg_columns <= 20:  # Reasonable number of columns
            structure_score = 1.0
        elif avg_columns < 2:
            structure_score = 0.3
        else:
            structure_score = max(0, 1 - (avg_columns - 20) / 50)
        
        # Calculate context score - penalize delimiters that appear in common contexts
        context_penalty = self._calculate_context_penalty(lines, delimiter)
        
        # Calculate priority bonus for common delimiters
        priority_bonus = self._calculate_priority_bonus(delimiter)
        
        # Weighted combination of scores with context penalty and priority bonus
        final_score = (consistency_score * 0.35 + frequency_score * 0.2 + structure_score * 0.25 + context_penalty * 0.1 + priority_bonus * 0.1)
        
        return final_score
    
    def _calculate_context_penalty(self, lines: List[str], delimiter: str) -> float:
        """
        Calculate penalty for delimiters that appear in common contexts (like time, dates, etc.)
        
        Args:
            lines: List of text lines
            delimiter: Delimiter to test
            
        Returns:
            Penalty score (higher = more penalty)
        """
        if delimiter not in [':', '-', '/', '.']:
            return 1.0  # No penalty for uncommon delimiters
        
        penalty = 1.0
        
        # Check for time patterns (HH:MM)
        time_pattern = r'\d{1,2}:\d{2}'
        time_matches = sum(len(re.findall(time_pattern, line)) for line in lines)
        
        # Check for date patterns (YYYY-MM-DD, MM/DD/YYYY, etc.)
        date_patterns = [
            r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
            r'\d{1,2}\.\d{1,2}\.\d{4}',  # MM.DD.YYYY
        ]
        date_matches = sum(len(re.findall(pattern, line)) for line in lines for pattern in date_patterns)
        
        # Check for URL patterns
        url_pattern = r'https?://[^\s]+'
        url_matches = sum(len(re.findall(url_pattern, line)) for line in lines)
        
        # Calculate penalty based on context matches
        total_context_matches = time_matches + date_matches + url_matches
        total_delimiter_occurrences = sum(line.count(delimiter) for line in lines)
        
        if total_delimiter_occurrences > 0:
            context_ratio = total_context_matches / total_delimiter_occurrences
            penalty = max(0.1, 1 - context_ratio)  # Higher context ratio = lower penalty
        
        return penalty
    
    def _calculate_priority_bonus(self, delimiter: str) -> float:
        """
        Calculate priority bonus for common delimiters
        
        Args:
            delimiter: Delimiter to test
            
        Returns:
            Priority bonus score
        """
        # Higher priority delimiters get higher bonuses
        priority_map = {
            '|': 1.0,    # Pipe - highest priority
            '\t': 0.9,   # Tab
            ',': 0.8,    # Comma
            ';': 0.7,    # Semicolon
            ':': 0.6,    # Colon
            ' ': 0.5,    # Space
        }
        
        return priority_map.get(delimiter, 0.3)  # Default bonus for other delimiters
    
    def _calculate_header_delimiter_score(self, header: str, data_lines: List[str]) -> dict:
        """
        Calculate delimiter score based on header row analysis
        
        Args:
            header: Header row
            data_lines: Data rows
            
        Returns:
            Dictionary of delimiter scores
        """
        scores = {}
        
        for delimiter in self.COMMON_DELIMITERS:
            # Count delimiters in header
            header_count = header.count(delimiter)
            
            if header_count == 0:
                scores[delimiter] = 0.0
                continue
            
            # Filter data lines that actually contain the delimiter
            # This handles multi-line records where only some lines contain delimiters
            data_lines_with_delimiter = [line for line in data_lines if delimiter in line]
            
            if not data_lines_with_delimiter:
                # If no data lines contain the delimiter, give it a low score
                scores[delimiter] = 0.1
                continue
            
            # Count delimiters in data lines that contain the delimiter
            data_counts = [line.count(delimiter) for line in data_lines_with_delimiter]
            
            # Calculate consistency with header
            consistent_lines = sum(1 for count in data_counts if count == header_count)
            consistency_ratio = consistent_lines / len(data_counts) if data_counts else 0
            
            # Calculate score based on consistency and header structure
            if consistency_ratio > 0.8:  # Very consistent
                score = 0.9 + (header_count * 0.01)  # Bonus for more columns
            elif consistency_ratio > 0.5:  # Moderately consistent
                score = 0.8 + (header_count * 0.01)  # Increased base score
            elif consistency_ratio > 0.2:  # Somewhat consistent
                score = 0.6 + (header_count * 0.01)
            else:
                score = 0.3 + (header_count * 0.01)
            
            # Bonus for pipe delimiter (common in structured data)
            if delimiter == '|':
                score += 0.2  # Increased bonus
            
            # Bonus if we found data lines with this delimiter
            if data_lines_with_delimiter:
                score += 0.1
            
            scores[delimiter] = min(1.0, score)
        
        return scores
    
    def _is_ghl_format(self, text: str) -> bool:
        """
        Check if text looks like GoHighLevel format
        
        Args:
            text: Input text to analyze
            
        Returns:
            True if it looks like GHL format
        """
        # Check for common GHL field names
        ghl_indicators = [
            'postAtSpecificTime',
            'OGmetaUrl',
            'imageUrls',
            'mediaOptimization',
            'applyWatermark',
            'eventType',
            'actionType',
            'privacyLevel',
            'enableComment',
            'enableDuet',
            'enableStitch',
            'videoDisclosure',
            'promoteYourBrand',
            'notifyAllGroupMembers'
        ]
        
        text_lower = text.lower()
        indicator_count = sum(1 for indicator in ghl_indicators if indicator.lower() in text_lower)
        
        # If we find 3 or more GHL indicators, it's likely GHL format
        return indicator_count >= 3
    
    def get_delimiter_info(self, text: str, delimiter: str) -> dict:
        """
        Get detailed information about a specific delimiter in the text
        
        Args:
            text: Input text
            delimiter: Delimiter to analyze
            
        Returns:
            Dictionary with delimiter statistics
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return {}
        
        delimiter_counts = [line.count(delimiter) for line in lines]
        
        return {
            'delimiter': delimiter,
            'total_occurrences': sum(delimiter_counts),
            'avg_per_line': sum(delimiter_counts) / len(delimiter_counts),
            'min_per_line': min(delimiter_counts),
            'max_per_line': max(delimiter_counts),
            'consistency': len(set(delimiter_counts)) == 1,
            'estimated_columns': sum(delimiter_counts) / len(delimiter_counts) + 1
        }
