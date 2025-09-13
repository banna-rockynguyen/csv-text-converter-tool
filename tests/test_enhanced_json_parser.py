"""
Tests for enhanced_json_parser module
"""

import pytest
from app.enhanced_json_parser import EnhancedJSONContentParser


class TestEnhancedJSONContentParser:
    """Test cases for EnhancedJSONContentParser"""

    def setup_method(self):
        """Set up test fixtures"""
        self.parser = EnhancedJSONContentParser()

    def test_format_structured_content_basic(self):
        """Test basic content formatting"""
        content = "[TITLE]Test Title[/TITLE]"
        result = self.parser._format_structured_content(content)
        assert "TEST TITLE" in result
        assert "[TITLE]" not in result

    def test_format_structured_content_highlight(self):
        """Test highlight formatting"""
        content = "This is [HIGHLIGHT]important text[/HIGHLIGHT]"
        result = self.parser._format_structured_content(content)
        assert "IMPORTANT TEXT" in result
        assert "[HIGHLIGHT]" not in result

    def test_format_structured_content_cta(self):
        """Test CTA formatting"""
        content = "[CTA]Click here[/CTA]"
        result = self.parser._format_structured_content(content)
        assert "👉" in result
        assert "CLICK HERE" in result
        assert "[CTA]" not in result

    def test_format_structured_content_hashtags(self):
        """Test hashtags formatting"""
        content = "[HASHTAGS]test hashtag[/HASHTAGS]"
        result = self.parser._format_structured_content(content)
        assert "#test hashtag" in result
        assert "[HASHTAGS]" not in result

    def test_format_structured_content_bold_to_caps(self):
        """Test bold text conversion to caps"""
        content = "This is **bold text**"
        result = self.parser._format_structured_content(content)
        assert "BOLD TEXT" in result
        assert "**" not in result

    def test_format_structured_content_block_tags(self):
        """Test [BLOCK] tag processing"""
        content = "[BLOCK]Block content here"
        result = self.parser._format_structured_content(content)
        assert "Block content here" in result
        assert "[BLOCK]" not in result

    def test_parse_single_post_carousel(self):
        """Test parsing carousel post"""
        post = {
            "ngay": "01/01/2025",
            "dinh_dang": "Carousel",
            "tieu_de_chinh": "Test Carousel",
            "noi_dung_carousel": [
                {
                    "slide_number": 1,
                    "tieu_de": "Slide 1",
                    "noi_dung": ["Content 1", "Content 2"],
                }
            ],
            "giai_doan_pheu": "Awareness",
            "goi_y_cta": ["Test CTA"],
            "utm": {"utm_source": "Test"},
            "tags": ["#test"],
            "ghi_chu": "Test note",
        }

        result = self.parser._parse_single_post(
            post, enable_ai=False, platform="LinkedIn"
        )

        assert result is not None
        assert result["Date"] == "01/01/2025"
        assert result["Content Type"] == "Carousel"
        assert "Test Carousel" in result["Content"]
        assert "#RockyNguyen" in result["Tags"]  # Required hashtag

    def test_parse_single_post_poll(self):
        """Test parsing poll post"""
        post = {
            "ngay": "01/01/2025",
            "dinh_dang": "Poll",
            "cau_hoi": "Test question?",
            "cac_lua_chon": ["Option A", "Option B"],
            "noi_dung_post": "Test poll content",
            "giai_doan_pheu": "Awareness",
            "goi_y_cta": ["Test CTA"],
            "utm": {"utm_source": "Test"},
            "tags": ["#test"],
        }

        result = self.parser._parse_single_post(
            post, enable_ai=False, platform="LinkedIn"
        )

        assert result is not None
        assert result["Content Type"] == "Poll"
        assert "Test question?" in result["Content"]

    def test_required_hashtags_always_included(self):
        """Test that required hashtags are always included"""
        post = {
            "ngay": "01/01/2025",
            "dinh_dang": "Carousel",
            "tieu_de_chinh": "Test",
            "noi_dung_carousel": [],
            "giai_doan_pheu": "Awareness",
            "goi_y_cta": [],
            "utm": {},
            "tags": ["#custom"],
        }

        result = self.parser._parse_single_post(
            post, enable_ai=False, platform="LinkedIn"
        )

        assert "#RockyNguyen" in result["Tags"]
        assert "#BANNAConsulting" in result["Tags"]
        assert "#NguyenDanhNgoc" in result["Tags"]
        assert "#custom" in result["Tags"]

    def test_utm_link_generation(self):
        """Test UTM link generation"""
        utm = {"utm_source": "LinkedIn", "utm_medium": "Post", "utm_campaign": "Test"}

        result = self.parser._generate_utm_link(utm)
        assert "UTM tracking" in result
        assert "utm_source: LinkedIn" in result
        assert "utm_medium: Post" in result
        assert "utm_campaign: Test" in result

    def test_parse_json_data(self):
        """Test parsing JSON data"""
        json_data = [
            {
                "ngay": "01/01/2025",
                "dinh_dang": "Carousel",
                "tieu_de_chinh": "Test",
                "noi_dung_carousel": [],
                "giai_doan_pheu": "Awareness",
                "goi_y_cta": [],
                "utm": {},
                "tags": [],
            }
        ]

        result = self.parser.parse_json_to_csv(
            json_data, enable_ai=False, platform="LinkedIn"
        )

        assert result is not None
        assert len(result) > 0
        assert "Date" in result[0]
        assert "Content" in result[0]

