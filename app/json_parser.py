import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional


class JSONContentParser:
    """Parser for JSON content format to convert to GoHighLevel CSV"""

    def __init__(self):
        self.ghl_headers = [
            "All Social",
            "All Social",
            "All Social",
            "All Social",
            "All Social",
            "All Social",
            "All Social",
            "All Social",
            "All Social",
            "All Social",
            "All Social",
            "Facebook",
            "Instagram",
            "LinkedIn",
            "LinkedIn",
            "Google (GBP)",
            "Google (GBP)",
            "Google (GBP)",
            "Google (GBP)",
            "Google (GBP)",
            "Google (GBP)",
            "Google (GBP)",
            "Google (GBP)",
            "Google (GBP)",
            "Google (GBP)",
            "YouTube",
            "YouTube",
            "YouTube",
            "TikTok",
            "TikTok",
            "TikTok",
            "TikTok",
            "TikTok",
            "TikTok",
            "TikTok",
            "Community",
            "Community",
            "Pinterest",
            "Pinterest",
        ]

        self.ghl_field_headers = [
            "postAtSpecificTime (YYYY-MM-DD HH:mm:ss)",
            "content",
            "OGmetaUrl (url)",
            "imageUrls (comma-separated)",
            "gifUrl",
            "videoUrls (comma-separated)",
            "mediaOptimization (true/false)",
            "applyWatermark (true/false)",
            "tags (comma-separated)",
            "category",
            "followUpComment",
            "type (post/story/reel)",
            "type (post/story/reel)",
            "pdfTitle",
            "postAsPdf (true/false)",
            "eventType (call_to_action/event/offer)",
            "actionType (none/order/book/shop/learn_more/call/sign_up)",
            "title",
            "offerTitle",
            "startDate (YYYY-MM-DD HH:mm:ss)",
            "endDate (YYYY-MM-DD HH:mm:ss)",
            "termsConditions",
            "couponCode",
            "redeemOnlineUrl",
            "actionUrl",
            "title",
            "privacyLevel (private/public/unlisted)",
            "type (video/short)",
            "privacyLevel (everyone/friends/only_me)",
            "promoteOtherBrand (true/false)",
            "enableComment (true/false)",
            "enableDuet (true/false)",
            "enableStitch (true/false)",
            "videoDisclosure (true/false)",
            "promoteYourBrand (true/false)",
            "title",
            "notifyAllGroupMembers (true/false)",
            "title",
            "link",
        ]

    def parse_json_content(self, json_text: str) -> Dict[str, Any]:
        """Parse JSON content and return structured data"""
        try:
            content_data = json.loads(json_text)

            if not isinstance(content_data, list):
                return {
                    "success": False,
                    "error": "JSON content must be an array of posts",
                }

            parsed_posts = []
            for post in content_data:
                parsed_post = self._parse_single_post(post)
                if parsed_post:
                    parsed_posts.append(parsed_post)

            return {
                "success": True,
                "posts": parsed_posts,
                "total_posts": len(parsed_posts),
            }

        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON format: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Error parsing content: {str(e)}"}

    def _parse_single_post(self, post: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse a single post from JSON"""
        try:
            # Extract basic info
            ngay = post.get("ngay", "")
            dinh_dang = post.get("dinh_dang", "")
            giai_doan_pheu = post.get("giai_doan_pheu", "Awareness")
            tags = post.get("tags", [])
            utm = post.get("utm", {})
            goi_y_cta = post.get("goi_y_cta", [])

            # Generate content based on post type
            content = self._generate_content(post, dinh_dang)

            # Generate title
            title = self._generate_title(post, dinh_dang)

            # Generate CTA
            cta_text = self._generate_cta(goi_y_cta)

            # Generate tags string
            tags_string = ", ".join(tags) if tags else ""

            # Generate UTM link
            utm_link = self._generate_utm_link(utm)

            # Convert date format
            post_time = self._convert_date_format(ngay)

            return {
                "post_time": post_time,
                "content": content,
                "title": title,
                "cta": cta_text,
                "tags": tags_string,
                "utm_link": utm_link,
                "post_type": dinh_dang,
                "funnel_stage": giai_doan_pheu,
                "utm_source": utm.get("utm_source", ""),
                "utm_medium": utm.get("utm_medium", ""),
                "utm_campaign": utm.get("utm_campaign", ""),
                "utm_content": utm.get("utm_content", ""),
            }

        except Exception as e:
            print(f"Error parsing post: {e}")
            return None

    def _generate_content(self, post: Dict[str, Any], post_type: str) -> str:
        """Generate content based on post type"""
        if post_type == "Carousel":
            return self._generate_carousel_content(post)
        elif post_type == "Poll":
            return self._generate_poll_content(post)
        elif post_type == "Short Story":
            return self._generate_story_content(post)
        elif post_type == "Listing":
            return self._generate_listing_content(post)
        elif post_type == "Quote Card":
            return self._generate_quote_content(post)
        else:
            return post.get("noi_dung_post", "")

    def _generate_carousel_content(self, post: Dict[str, Any]) -> str:
        """Generate content for Carousel post"""
        tieu_de_chinh = post.get("tieu_de_chinh", "")
        noi_dung_carousel = post.get("noi_dung_carousel", [])

        content_parts = [f"🎯 {tieu_de_chinh}"]

        for slide in noi_dung_carousel:
            slide_title = slide.get("tieu_de", "")
            slide_content = slide.get("noi_dung", [])

            if slide_title:
                content_parts.append(f"\n📌 {slide_title}")

            for line in slide_content:
                content_parts.append(line)

        return "\n".join(content_parts)

    def _generate_poll_content(self, post: Dict[str, Any]) -> str:
        """Generate content for Poll post"""
        cau_hoi = post.get("cau_hoi", "")
        cac_lua_chon = post.get("cac_lua_chon", [])
        noi_dung_post = post.get("noi_dung_post", "")

        content_parts = [f"📊 {cau_hoi}"]

        for i, lua_chon in enumerate(cac_lua_chon, 1):
            content_parts.append(f"{lua_chon}")

        if noi_dung_post:
            content_parts.append(f"\n{noi_dung_post}")

        return "\n".join(content_parts)

    def _generate_story_content(self, post: Dict[str, Any]) -> str:
        """Generate content for Short Story post"""
        hook = post.get("hook", "")
        noi_dung_post = post.get("noi_dung_post", "")
        bai_hoc = post.get("bai_hoc", "")

        content_parts = [f"💡 {hook}"]
        content_parts.append(f"\n{noi_dung_post}")

        if bai_hoc:
            content_parts.append(f"\n📚 Bài học: {bai_hoc}")

        return "\n".join(content_parts)

    def _generate_listing_content(self, post: Dict[str, Any]) -> str:
        """Generate content for Listing post"""
        hook = post.get("hook", "")
        noi_dung_post = post.get("noi_dung_post", [])

        content_parts = [f"📋 {hook}"]

        for i, item in enumerate(noi_dung_post, 1):
            content_parts.append(f"\n{i}. {item}")

        return "\n".join(content_parts)

    def _generate_quote_content(self, post: Dict[str, Any]) -> str:
        """Generate content for Quote Card post"""
        noi_dung_post = post.get("noi_dung_post", {})

        if isinstance(noi_dung_post, dict):
            quote = noi_dung_post.get("quote", "")
            tac_gia = noi_dung_post.get("tac_gia", "")

            content_parts = [f'"{quote}"']
            if tac_gia:
                content_parts.append(f"\n— {tac_gia}")

            return "\n".join(content_parts)

        return str(noi_dung_post)

    def _generate_title(self, post: Dict[str, Any], post_type: str) -> str:
        """Generate title for the post"""
        if post_type == "Carousel":
            return post.get("tieu_de_chinh", "")
        elif post_type == "Poll":
            return post.get("cau_hoi", "")
        elif post_type == "Short Story":
            return post.get("hook", "")
        elif post_type == "Listing":
            return post.get("hook", "")
        elif post_type == "Quote Card":
            noi_dung_post = post.get("noi_dung_post", {})
            if isinstance(noi_dung_post, dict):
                return noi_dung_post.get("tac_gia", "Quote")
            return "Quote"
        else:
            return post.get("tieu_de_chinh", "")

    def _generate_cta(self, goi_y_cta: List[str]) -> str:
        """Generate CTA text from suggestions"""
        if not goi_y_cta:
            return ""

        return " ".join(goi_y_cta)

    def _generate_utm_link(self, utm: Dict[str, str]) -> str:
        """Generate UTM tracking link"""
        base_url = "https://banna.vn"
        utm_params = []

        for key, value in utm.items():
            if value:
                utm_params.append(f"{key}={value}")

        if utm_params:
            return f"{base_url}?{'&'.join(utm_params)}"

        return base_url

    def _convert_date_format(self, ngay: str) -> str:
        """Convert date from DD/MM/YYYY to YYYY-MM-DD HH:mm:ss"""
        try:
            # Handle different date formats
            if "/" in ngay:
                # DD/MM/YYYY format
                if "-" in ngay:
                    # Handle range like "06-07/09/2025"
                    parts = ngay.split("/")
                    if len(parts) == 2:
                        day_range, month_year = parts
                        if "-" in day_range:
                            start_day, end_day = day_range.split("-")
                            # Use start day
                            day = start_day
                        else:
                            day = day_range
                        month, year = month_year.split("/")
                    else:
                        day, month, year = parts
                else:
                    day, month, year = ngay.split("/")

                # Convert to YYYY-MM-DD format
                formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

                # Add default time (08:30:00)
                return f"{formatted_date} 08:30:00"
            else:
                # If format is not recognized, return as is
                return f"{ngay} 08:30:00"

        except Exception:
            # If conversion fails, return current date
            return datetime.now().strftime("%Y-%m-%d 08:30:00")

    def convert_to_ghl_csv(self, posts: List[Dict[str, Any]]) -> str:
        """Convert parsed posts to GoHighLevel CSV format"""
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

        # Write platform headers
        writer.writerow(self.ghl_headers)

        # Write field headers
        writer.writerow(self.ghl_field_headers)

        # Write data rows
        for post in posts:
            row = self._create_ghl_row(post)
            writer.writerow(row)

        return output.getvalue()

    def _create_ghl_row(self, post: Dict[str, Any]) -> List[str]:
        """Create a single row for GoHighLevel CSV"""
        # Initialize row with empty values for all 40 columns
        row = [""] * 40

        # Map post data to GoHighLevel columns
        row[0] = post.get("post_time", "")  # postAtSpecificTime
        row[1] = post.get("content", "")  # content
        row[2] = post.get("utm_link", "")  # OGmetaUrl
        row[3] = ""  # imageUrls (comma-separated)
        row[4] = ""  # gifUrl
        row[5] = ""  # videoUrls (comma-separated)
        row[6] = "false"  # mediaOptimization
        row[7] = "false"  # applyWatermark
        row[8] = post.get("tags", "")  # tags (comma-separated)
        row[9] = post.get("funnel_stage", "Awareness")  # category
        row[10] = post.get("cta", "")  # followUpComment
        row[11] = "post"  # type (post/story/reel)
        row[12] = "post"  # type (post/story/reel)
        row[13] = ""  # pdfTitle
        row[14] = "false"  # postAsPdf
        row[15] = "call_to_action"  # eventType
        row[16] = "learn_more"  # actionType
        row[17] = post.get("title", "")  # title
        row[18] = ""  # offerTitle
        row[19] = ""  # startDate
        row[20] = ""  # endDate
        row[21] = ""  # termsConditions
        row[22] = ""  # couponCode
        row[23] = ""  # redeemOnlineUrl
        row[24] = post.get("utm_link", "")  # actionUrl
        row[25] = post.get("title", "")  # title
        row[26] = "public"  # privacyLevel
        row[27] = "video"  # type (video/short)
        row[28] = "everyone"  # privacyLevel
        row[29] = "false"  # promoteOtherBrand
        row[30] = "true"  # enableComment
        row[31] = "false"  # enableDuet
        row[32] = "false"  # enableStitch
        row[33] = "false"  # videoDisclosure
        row[34] = "true"  # promoteYourBrand
        row[35] = post.get("title", "")  # title
        row[36] = "false"  # notifyAllGroupMembers
        row[37] = post.get("title", "")  # title
        row[38] = post.get("utm_link", "")  # link

        return row
