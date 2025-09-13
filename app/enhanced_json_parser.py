import json
import re
import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import google.generativeai as genai


class EnhancedJSONContentParser:
    """Enhanced JSON Parser with AI content formatting using Gemini 2.5 Pro"""

    def __init__(self, gemini_api_key: str = None):
        # GoHighLevel headers (unchanged)
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

        # AI Configuration
        self.gemini_api_key = gemini_api_key
        self.ai_enabled = False
        if gemini_api_key:
            try:
                genai.configure(api_key=gemini_api_key)
                self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
                self.ai_enabled = True
                print("✅ Gemini 2.5 Pro API initialized successfully")
            except Exception as e:
                print(f"❌ Gemini API initialization failed: {e}")
                self.ai_enabled = False

    def parse_json_content(
        self, json_text: str, enable_ai: bool = True, platform: str = "LinkedIn"
    ) -> Dict[str, Any]:
        """Parse JSON content with optional AI enhancement"""
        try:
            content_data = json.loads(json_text)

            if not isinstance(content_data, list):
                return {
                    "success": False,
                    "error": "JSON content must be an array of posts",
                }

            parsed_posts = []
            for post in content_data:
                parsed_post = self._parse_single_post(post, enable_ai, platform)
                if parsed_post:
                    parsed_posts.append(parsed_post)

            return {
                "success": True,
                "posts": parsed_posts,
                "total_posts": len(parsed_posts),
                "ai_enhanced": enable_ai and self.ai_enabled,
            }

        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON format: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Error parsing content: {str(e)}"}

    def _parse_single_post(
        self, post: Dict[str, Any], enable_ai: bool, platform: str
    ) -> Optional[Dict[str, Any]]:
        """Parse a single post with AI enhancement"""
        try:
            # Extract basic info
            ngay = post.get("ngay", "")
            dinh_dang = post.get("dinh_dang", "")
            giai_doan_pheu = post.get("giai_doan_pheu", "Awareness")
            tags = post.get("tags", [])
            utm = post.get("utm", {})
            goi_y_cta = post.get("goi_y_cta", [])

            # Generate base content
            base_content = self._generate_content(post, dinh_dang)

            # Apply AI enhancement if enabled
            if enable_ai and self.ai_enabled:
                enhanced_content = self._enhance_content_with_ai(
                    base_content, dinh_dang, platform
                )
                content = enhanced_content if enhanced_content else base_content
            else:
                content = self._enhance_content_formatting(base_content, dinh_dang)

            # Generate other fields
            title = self._generate_title(post, dinh_dang)
            cta_text = self._generate_cta(goi_y_cta)
            tags_string = self._format_tags(tags)  # Updated method
            utm_note = self._generate_utm_note(utm)  # Updated method
            post_time = self._convert_date_format(ngay)

            return {
                "post_time": post_time,
                "content": content,
                "title": title,
                "cta": cta_text,
                "tags": tags_string,
                "utm_note": utm_note,  # Changed from utm_link
                "post_type": dinh_dang,
                "funnel_stage": giai_doan_pheu,
                "utm_source": utm.get("utm_source", ""),
                "utm_medium": utm.get("utm_medium", ""),
                "utm_campaign": utm.get("utm_campaign", ""),
                "utm_content": utm.get("utm_content", ""),
                "ai_enhanced": enable_ai and self.ai_enabled,
            }

        except Exception as e:
            print(f"Error parsing post: {e}")
            return None

    def _enhance_content_formatting(self, content: str, post_type: str) -> str:
        """Enhanced content formatting (Tier 1 improvements)"""
        if not content:
            return content

        # 1. Fix line breaks and spacing
        content = re.sub(r"\n\s*\n+", "\n\n", content)  # Clean multiple line breaks
        content = re.sub(r"[ \t]+", " ", content)  # Clean extra spaces

        # 2. Enhance bold text formatting
        content = re.sub(r"\*\*(.*?)\*\*", r"**\1**", content)

        # 3. Add proper spacing around emojis
        content = re.sub(r"([🎯📊💡📋💬])([A-Za-z])", r"\1 \2", content)

        # 4. Post-type specific formatting
        if post_type == "Carousel":
            content = self._format_carousel_enhanced(content)
        elif post_type == "Poll":
            content = self._format_poll_enhanced(content)
        elif post_type == "Listing":
            content = self._format_listing_enhanced(content)
        elif post_type == "Short Story":
            content = self._format_story_enhanced(content)
        elif post_type == "Quote Card":
            content = self._format_quote_enhanced(content)

        return content.strip()

    def _format_carousel_enhanced(self, content: str) -> str:
        """Enhanced carousel formatting"""
        lines = content.split("\n")
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Format slide titles with better spacing
            if line.startswith("📌"):
                formatted_lines.append(f"\n\n{line}")
            # Format main title
            elif line.startswith("🎯"):
                formatted_lines.append(f"{line}\n")
            # Format bullet points with proper indentation
            elif line.startswith("•") or line.startswith("-"):
                formatted_lines.append(f"  ✓ {line[1:].strip()}")
            # Enhance bold text
            elif "**" in line:
                formatted_lines.append(self._enhance_bold_text(line))
            else:
                formatted_lines.append(line)

        return "\n".join(formatted_lines)

    def _format_poll_enhanced(self, content: str) -> str:
        """Enhanced poll formatting"""
        lines = content.split("\n")
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Format question with emphasis
            if line.startswith("📊"):
                formatted_lines.append(f"{line}\n")
            # Format options with better styling
            elif re.match(r"^\([A-D]\)", line):
                formatted_lines.append(f"  {line}")
            # Add spacing for description
            else:
                formatted_lines.append(f"\n{line}")

        return "\n".join(formatted_lines)

    def _format_listing_enhanced(self, content: str) -> str:
        """Enhanced listing formatting"""
        lines = content.split("\n")
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Format main title
            if line.startswith("📋"):
                formatted_lines.append(f"{line}\n")
            # Format numbered items with proper spacing
            elif re.match(r"^\d+\.", line):
                formatted_lines.append(f"\n{line}")
            # Format sub-items
            else:
                formatted_lines.append(f"  {line}")

        return "\n".join(formatted_lines)

    def _format_story_enhanced(self, content: str) -> str:
        """Enhanced story formatting"""
        lines = content.split("\n")
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Format hook with emphasis
            if line.startswith("💡"):
                formatted_lines.append(f"{line}\n")
            # Format lesson with spacing
            elif line.startswith("📚"):
                formatted_lines.append(f"\n{line}")
            # Add paragraph breaks for better readability
            else:
                if len(line) > 100 and "." in line:
                    sentences = line.split(". ")
                    for i, sentence in enumerate(sentences):
                        if i > 0 and len(sentence) > 20:
                            formatted_lines.append(f"\n{sentence.strip()}")
                        else:
                            formatted_lines.append(
                                sentence.strip()
                                + ("." if i < len(sentences) - 1 else "")
                            )
                else:
                    formatted_lines.append(line)

        return "\n".join(formatted_lines)

    def _format_quote_enhanced(self, content: str) -> str:
        """Enhanced quote formatting"""
        lines = content.split("\n")
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Format quote with better styling
            if line.startswith('"') and line.endswith('"'):
                formatted_lines.append(f"💬 {line}")
            # Format attribution with spacing
            elif line.startswith("—"):
                formatted_lines.append(f"\n{line}")
            else:
                formatted_lines.append(line)

        return "\n".join(formatted_lines)

    def _enhance_bold_text(self, text: str) -> str:
        """Enhance bold text with better formatting"""
        # Ensure proper bold formatting
        text = re.sub(r"\*\*(.*?)\*\*", r"**\1**", text)
        # Add emphasis markers for key terms
        text = re.sub(
            r"\b(QUAN TRỌNG|CHÍNH|CỐT LÕI|THÀNH CÔNG)\b",
            r"**\1**",
            text,
            flags=re.IGNORECASE,
        )
        return text

    def _enhance_content_with_ai(
        self, content: str, post_type: str, platform: str
    ) -> Optional[str]:
        """Enhance content using Gemini 2.5 Pro API with new structured prompt"""
        if not self.ai_enabled:
            return None

        try:
            # Create structured prompt
            prompt_data = self._create_structured_prompt(content, post_type, platform)

            # Call Gemini API with retry logic
            response = self._call_gemini_api_structured(prompt_data)

            if response:
                enhanced_content = self._extract_enhanced_content(response)
                return enhanced_content

        except Exception as e:
            print(f"AI enhancement failed: {e}")

        return None

    def _create_structured_prompt(
        self, content: str, post_type: str, platform: str
    ) -> Dict[str, Any]:
        """Create structured prompt with System and User prompts"""

        # System Prompt (System Instruction)
        system_prompt = """Bạn là một Engine Tái cấu trúc Nội dung AI (AI Content Restructuring Engine) chuyên nghiệp. Nhiệm vụ của bạn là nhận một object JSON chứa nội dung thô và các yêu cầu, sau đó chuyển đổi nó thành một chuỗi văn bản (string) có cấu trúc chặt chẽ, sẵn sàng để hiển thị trên các nền tảng mạng xã hội.

**Mục tiêu cuối cùng:** Tạo ra nội dung có tính nhất quán cao, dễ đọc, nhấn mạnh thông tin hiệu quả và có thể được xử lý tự động bởi các hệ thống khác.

---
### **QUY TẮC VÀ CÚ PHÁP ĐẦU RA (OUTPUT SYNTAX)**
Bạn PHẢI tuân thủ tuyệt đối các cú pháp sau. Toàn bộ đầu ra phải là một chuỗi văn bản duy nhất.

1.  **Cấu trúc nội dung:**
    * Sử dụng xuống dòng tự nhiên để tạo các đoạn văn rõ ràng.
    * Mỗi ý tưởng chính nên được tách thành đoạn riêng biệt.
    * Sử dụng khoảng trắng để tạo sự thoáng đãng và dễ đọc.

2.  **Tiêu đề `[TITLE]...[/TITLE]`:**
    * Dùng để xác định tiêu đề chính. Sử dụng CHỮ IN HOA để nhấn mạnh.
    * Ví dụ: `[TITLE]3 CÂU HỎI QUAN TRỌNG[/TITLE]`

3.  **Nhấn mạnh `[HIGHLIGHT]...[/HIGHLIGHT]`:**
    * Sử dụng để bao bọc các từ khóa quan trọng. Chuyển thành CHỮ IN HOA.
    * Ví dụ: Xác định rõ ràng [HIGHLIGHT]KẾT QUẢ MƠ ƯỚC[/HIGHLIGHT] là bước đầu tiên.

4.  **Emoji `[EMOJI]`:**
    * Đặt `[EMOJI]` tại vị trí bạn cho rằng cần có một icon phù hợp với ngữ cảnh và nền tảng.
    * Ví dụ: `[EMOJI] Chuyển đổi số thành công!`

5.  **Kêu gọi hành động `[CTA]...[/CTA]`:**
    * Sử dụng để đánh dấu phần kêu gọi hành động của bài viết.
    * Ví dụ: `[CTA]Comment "TƯ VẤN" để nhận lộ trình chi tiết![/CTA]`

6.  **Hashtags `[HASHTAGS]...[/HASHTAGS]`:**
    * Tất cả các hashtag phải được đặt trong khối này, ở cuối nội dung.
    * Ví dụ: `[HASHTAGS]#chuyendoiso #marketing #strategy[/HASHTAGS]`

**QUAN TRỌNG:** KHÔNG sử dụng **in đậm** hay *in nghiêng*. Chỉ sử dụng CHỮ IN HOA, dấu ngoặc kép "", xuống dòng và ngắt dòng để tạo điểm nhấn.

---
### **LOGIC XỬ LÝ THEO NỀN TẢNG (PLATFORM-SPECIFIC LOGIC)**
Dựa vào trường `"platform"` trong JSON đầu vào, bạn phải điều chỉnh văn phong và cách sử dụng cú pháp như sau:

**IF platform = "LinkedIn":**
* **Văn phong:** Chuyên nghiệp, tập trung vào insight, giá trị cho doanh nghiệp và chuyên gia.
* **Emoji:** Tiết chế tối đa. Chỉ sử dụng các emoji chuyên nghiệp như 🎯, 📌, 👉, 💡, 🚀. Đặt `[EMOJI]` ở đầu dòng hoặc đầu `[BLOCK]`.
* **Độ dài:** Các câu có thể dài và phức tạp hơn để diễn giải ý tưởng sâu sắc. Các `[BLOCK]` nên được phân tách rõ ràng.
* **Hashtags:** 3-5 hashtags rất liên quan, tập trung vào ngành và chuyên môn.

**IF platform = "Facebook":**
* **Văn phong:** Thân thiện, gần gũi, khuyến khích tương tác (đặt câu hỏi, kêu gọi thảo luận).
* **Emoji:** Sử dụng `[EMOJI]` một cách tự nhiên và phong phú hơn để thể hiện cảm xúc (😊, 🤔, 🎉, 👍). Có thể đặt giữa câu.
* **Độ dài:** Câu ngắn gọn, dễ hiểu. Sử dụng nhiều `[BLOCK]` để ngắt đoạn, tạo sự thoáng đãng.
* **Hashtags:** 3-7 hashtags, có thể bao gồm cả hashtag thương hiệu và hashtag trending (nếu phù hợp).

**IF platform = "Instagram":**
* **Văn phong:** Tập trung vào hình ảnh, ngắn gọn, trendy. Đoạn mô tả (caption) cần hấp dẫn ngay từ dòng đầu tiên.
* **Emoji:** Sử dụng `[EMOJI]` rất nhiều để tạo điểm nhấn thị giác và thể hiện cá tính.
* **Độ dài:** Cực kỳ ngắn gọn. Ưu tiên các `[BLOCK]` chỉ có 1 câu. Tận dụng tối đa ngắt dòng.
* **Hashtags:** Rất quan trọng. Tạo một khối `[HASHTAGS]` lớn với 10-20 hashtags liên quan.

**IF platform = "TikTok":**
* **Văn phong:** Bắt trend, trẻ trung, trực diện, mang tính hành động cao.
* **Emoji:** Sử dụng `[EMOJI]` theo trend.
* **Độ dài:** Các câu phải siêu ngắn, đanh gọn. Gần như mỗi dòng là một `[BLOCK]` mới.
* **Hashtags:** Tập trung vào các hashtag đang thịnh hành trên nền tảng.

---
### **QUY TRÌNH THỰC HIỆN**

1.  **Phân tích JSON:** Đọc kỹ `input_content` và các tham số `platform`, `post_type`, `objective`.
2.  **Tái cấu trúc:** Chia `input_content` thành các đơn vị logic với xuống dòng tự nhiên.
3.  **Áp dụng Cú pháp:** Sử dụng `[TITLE]`, `[HIGHLIGHT]`, `[EMOJI]`, `[CTA]`, `[HASHTAGS]` để format nội dung. Chuyển đổi thành CHỮ IN HOA thay vì in đậm.
4.  **Tinh chỉnh theo Nền tảng:** Dựa vào `platform`, điều chỉnh văn phong, số lượng và vị trí `[EMOJI]`, độ dài câu, và nội dung của `[HASHTAGS]`.
5.  **Xuất kết quả:** Trả về một chuỗi văn bản duy nhất tuân thủ tất cả các quy tắc trên."""

        # User Prompt (JSON format)
        user_prompt = {
            "input_content": content,
            "platform": platform,
            "post_type": post_type,
            "objective": "Chia sẻ kiến thức chuyên môn, xây dựng uy tín.",
            "custom_instructions": [
                f"Tối ưu hóa nội dung cho {platform}",
                "Đảm bảo phù hợp văn hóa Việt Nam",
                "Tạo nội dung engaging và professional",
            ],
        }

        return {"system_prompt": system_prompt, "user_prompt": user_prompt}

    def _call_gemini_api_structured(
        self, prompt_data: Dict[str, Any], max_retries: int = 3
    ) -> Optional[str]:
        """Call Gemini API with structured prompt"""
        system_prompt = prompt_data["system_prompt"]
        user_prompt = prompt_data["user_prompt"]

        # Convert user prompt to JSON string
        user_prompt_json = json.dumps(user_prompt, ensure_ascii=False, indent=2)

        # Combine system and user prompts
        full_prompt = f"{system_prompt}\n\n---\n\n**INPUT JSON:**\n{user_prompt_json}\n\n**OUTPUT:**"

        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        candidate_count=1,
                        max_output_tokens=2048,
                        temperature=0.7,
                    ),
                )

                if response.text:
                    return response.text

            except Exception as e:
                print(f"Gemini API attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)  # Exponential backoff

        return None

    def _extract_enhanced_content(self, response: str) -> str:
        """Extract and clean enhanced content from AI response - FIXED VERSION"""
        # Remove prompt echo and extract actual content
        lines = response.split("\n")
        content_lines = []
        started = False

        for line in lines:
            if "**OUTPUT:**" in line or started:
                started = True
                if "**OUTPUT:**" not in line:
                    content_lines.append(line)
            elif not started and (
                line.strip().startswith("[BLOCK]")
                or line.strip().startswith("[TITLE]")
                or line.strip().startswith("[HIGHLIGHT]")
                or line.strip().startswith("[EMOJI]")
                or line.strip().startswith("[CTA]")
                or line.strip().startswith("[HASHTAGS]")
            ):
                started = True
                content_lines.append(line)

        if not content_lines:
            content_lines = lines

        # Clean and format
        enhanced_content = "\n".join(content_lines).strip()

        # Remove any remaining artifacts
        enhanced_content = re.sub(
            r"^(OUTPUT:|Enhanced Content:)",
            "",
            enhanced_content,
            flags=re.IGNORECASE,
        )
        enhanced_content = re.sub(r"\n\s*\n\s*\n", "\n\n", enhanced_content)

        # CRITICAL FIX: Convert structured tags to readable format
        enhanced_content = self._format_structured_content(enhanced_content)

        return enhanced_content.strip()

    def _format_structured_content(self, content: str) -> str:
        """Convert structured tags to readable format - NO BOLD, CAPS ONLY with MAXIMUM SPACING"""
        import re

        # Step 1: Handle all [BLOCK] patterns first with MAXIMUM spacing
        # [BLOCK]content -> content with MAXIMUM line breaks
        content = re.sub(r"\[BLOCK\]([^\n\[]+)", r"\n\n\n\n\1", content)
        # [BLOCK]**text** -> TEXT with MAXIMUM line breaks (convert to CAPS)
        content = re.sub(
            r"\[BLOCK\]\*\*([^*]+)\*\*",
            lambda m: f"\n\n\n\n{m.group(1).upper()}",
            content,
        )
        # [BLOCK][CTA]... -> CTA with MAXIMUM line breaks
        content = re.sub(r"\[BLOCK\]\[CTA\](.*?)\[/CTA\]", r"\n\n\n\n👉 \1", content)
        # [BLOCK] followed by any non-bracket character
        content = re.sub(r"\[BLOCK\]([^\[])", r"\n\n\n\n\1", content)

        # Step 2: Handle other structured tags with MAXIMUM spacing BEFORE removing [BLOCK]
        content = re.sub(r"\[CTA\](.*?)\[/CTA\]", r"\n\n\n\n👉 \1", content)
        content = re.sub(
            r"\[TITLE\](.*?)\[/TITLE\]",
            lambda m: f"\n\n\n{m.group(1).upper()}\n\n",
            content,
        )
        content = re.sub(
            r"\[HIGHLIGHT\](.*?)\[/HIGHLIGHT\]", lambda m: m.group(1).upper(), content
        )
        content = re.sub(r"\[EMOJI\]", "", content)
        content = re.sub(r"\[HASHTAGS\](.*?)\[/HASHTAGS\]", r"\n\n\n\n\1", content)

        # Step 3: Convert ALL **bold** text to CAPS
        content = re.sub(r"\*\*([^*]+)\*\*", lambda m: m.group(1).upper(), content)

        # Step 4: Add MAXIMUM spacing around important elements
        # Add spacing before numbered lists (1., 2., 3., etc.)
        content = re.sub(r"\n(\d+\.)", r"\n\n\n\1", content)
        # Add spacing before bullet points
        content = re.sub(r"\n([•\-\*])", r"\n\n\n\1", content)
        # Add spacing before emoji lines
        content = re.sub(r"\n([🎯📊💡📋💬📌])", r"\n\n\n\1", content)
        # Add spacing before CTA lines
        content = re.sub(r"\n(👉)", r"\n\n\n\1", content)

        # Step 5: Add spacing between paragraphs
        # Add spacing after sentences ending with period
        content = re.sub(r"(\.)\n([A-Z])", r"\1\n\n\2", content)
        # Add spacing after sentences ending with exclamation
        content = re.sub(r"(!)\n([A-Z])", r"\1\n\n\2", content)
        # Add spacing after sentences ending with question mark
        content = re.sub(r"(\?)\n([A-Z])", r"\1\n\n\2", content)

        # Step 6: Remove all remaining [BLOCK] and [/BLOCK] tags AFTER processing
        content = re.sub(r"\[BLOCK\]", "", content)
        content = re.sub(r"\[/BLOCK\]", "", content)

        # Step 7: Clean up excessive line breaks (but keep more than before)
        # Allow up to 4 consecutive line breaks, replace more with 4
        content = re.sub(r"\n\s*\n\s*\n\s*\n\s*\n+", "\n\n\n\n", content)
        # Clean up spaces around line breaks
        content = re.sub(r"\n\s+", "\n", content)
        content = re.sub(r"\s+\n", "\n", content)

        # Step 8: Final cleanup
        content = content.rstrip()

        return content

    def _format_tags(self, tags: List[str]) -> str:
        """Format tags with required hashtags - UPDATED METHOD"""
        if not tags:
            tags = []

        # Required hashtags
        required_tags = ["#RockyNguyen", "#BANNAConsulting", "#NguyenDanhNgoc"]

        # Combine original tags with required tags
        all_tags = tags + required_tags

        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in all_tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)

        return ", ".join(unique_tags)

    def _generate_utm_note(self, utm: Dict[str, str]) -> str:
        """Generate UTM note instead of URL - NEW METHOD"""
        if not utm:
            return ""

        utm_parts = []
        for key, value in utm.items():
            if value:
                utm_parts.append(f"{key}: {value}")

        if utm_parts:
            return f"UTM tracking: {', '.join(utm_parts)}"

        return ""

    # Keep all existing methods unchanged (generate_content, generate_title, etc.)
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

        for lua_chon in cac_lua_chon:
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

    def _convert_date_format(self, ngay: str) -> str:
        """Convert date from DD/MM/YYYY to YYYY-MM-DD HH:mm:ss"""
        try:
            if "/" in ngay:
                if "-" in ngay:
                    parts = ngay.split("/")
                    if len(parts) == 2:
                        day_range, month_year = parts
                        if "-" in day_range:
                            start_day = day_range.split("-")[0]
                            day = start_day
                        else:
                            day = day_range
                        month, year = month_year.split("/")
                    else:
                        day, month, year = parts
                else:
                    day, month, year = ngay.split("/")

                formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                return f"{formatted_date} 08:30:00"
            else:
                return f"{ngay} 08:30:00"

        except Exception:
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
        """Create a single row for GoHighLevel CSV - UPDATED"""
        row = [""] * 40

        row[0] = post.get("post_time", "")
        row[1] = post.get("content", "")
        row[2] = ""  # No URL, keep empty
        row[3] = ""
        row[4] = ""
        row[5] = ""
        row[6] = "false"
        row[7] = "false"
        row[8] = post.get("tags", "")
        row[9] = post.get("funnel_stage", "Awareness")
        row[10] = post.get("utm_note", "")  # UTM note instead of URL
        row[11] = "post"
        row[12] = "post"
        row[13] = ""
        row[14] = "false"
        row[15] = "call_to_action"
        row[16] = "learn_more"
        row[17] = post.get("title", "")
        row[18] = ""
        row[19] = ""
        row[20] = ""
        row[21] = ""
        row[22] = ""
        row[23] = ""
        row[24] = ""  # No URL, keep empty
        row[25] = post.get("title", "")
        row[26] = "public"
        row[27] = "video"
        row[28] = "everyone"
        row[29] = "false"
        row[30] = "true"
        row[31] = "false"
        row[32] = "false"
        row[33] = "false"
        row[34] = "true"
        row[35] = post.get("title", "")
        row[36] = "false"
        row[37] = post.get("title", "")
        row[38] = ""  # No URL, keep empty

        return row
