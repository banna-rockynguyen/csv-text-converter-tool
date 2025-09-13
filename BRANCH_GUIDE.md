# Branch Guide - Hướng dẫn sử dụng các nhánh

## 🌳 Cấu trúc nhánh

### Nhánh chính (Main Branches)
- **`main`**: Code production, ổn định, sẵn sàng deploy
- **`develop`**: Nhánh tích hợp, nơi merge các feature trước khi đưa vào main

### Nhánh tính năng (Feature Branches)
- **`feature/advanced-ai-features`**: Tính năng AI nâng cao
- **`feature/ui-improvements`**: Cải thiện giao diện người dùng
- **`feature/performance-optimization`**: Tối ưu hiệu suất

### Nhánh thử nghiệm (Experiment Branches)
- **`experiment/multi-language-support`**: Hỗ trợ đa ngôn ngữ
- **`experiment/batch-processing`**: Xử lý hàng loạt
- **`experiment/api-integration`**: Tích hợp API bên ngoài

## 🚀 Cách sử dụng các nhánh

### 1. Bắt đầu phát triển tính năng mới

```bash
# Chuyển về nhánh develop
git checkout develop
git pull origin develop

# Tạo nhánh mới cho tính năng
git checkout -b feature/ten-tinh-nang-moi
# hoặc
git checkout -b experiment/tinh-nang-thu-nghiem
```

### 2. Phát triển trên nhánh thử nghiệm

#### Multi-Language Support (`experiment/multi-language-support`)
**Mục tiêu**: Hỗ trợ tạo nội dung đa ngôn ngữ

**Các tính năng có thể thêm**:
- Phát hiện ngôn ngữ tự động
- Prompt AI theo ngôn ngữ
- Formatting theo văn hóa từng nước
- Hashtag địa phương hóa

**Ví dụ code**:
```python
# Thêm vào enhanced_json_parser.py
def detect_language(self, content: str) -> str:
    """Detect content language"""
    from langdetect import detect
    return detect(content)

def create_multilingual_prompt(self, content: str, language: str) -> dict:
    """Create AI prompt based on language"""
    language_prompts = {
        'vi': "Tạo nội dung tiếng Việt...",
        'en': "Create English content...",
        'ja': "日本語のコンテンツを作成...",
    }
    # Implementation here
```

#### Batch Processing (`experiment/batch-processing`)
**Mục tiêu**: Xử lý nhiều file JSON cùng lúc

**Các tính năng có thể thêm**:
- Upload nhiều file
- Queue xử lý
- Progress tracking
- Export kết quả hàng loạt

**Ví dụ code**:
```python
# Thêm vào app/batch_processor.py
import celery
from celery import Celery

app = Celery('batch_processor')

@app.task
def process_json_batch(file_paths: list) -> dict:
    """Process multiple JSON files"""
    results = []
    for file_path in file_paths:
        # Process each file
        result = process_single_file(file_path)
        results.append(result)
    return results
```

#### API Integration (`experiment/api-integration`)
**Mục tiêu**: Tích hợp với các API bên ngoài

**Các tính năng có thể thêm**:
- GoHighLevel API
- Social media APIs
- Content scheduling
- Analytics tracking

**Ví dụ code**:
```python
# Thêm vào app/api_integrations.py
import requests

class GoHighLevelAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://rest.gohighlevel.com/v1"
    
    def create_contact(self, contact_data: dict) -> dict:
        """Create contact in GoHighLevel"""
        # Implementation here
        pass
    
    def upload_csv(self, csv_data: str) -> dict:
        """Upload CSV to GoHighLevel"""
        # Implementation here
        pass
```

### 3. Workflow phát triển

```bash
# 1. Tạo nhánh mới
git checkout -b feature/ten-tinh-nang

# 2. Phát triển tính năng
# ... code changes ...

# 3. Test tính năng
python -m pytest tests/
python run.py  # Test thủ công

# 4. Commit changes
git add .
git commit -m "feat: add new feature description"

# 5. Push lên GitHub
git push origin feature/ten-tinh-nang

# 6. Tạo Pull Request trên GitHub
# 7. Merge vào develop sau khi review
```

### 4. Merge về main

```bash
# Khi tính năng đã ổn định
git checkout develop
git merge feature/ten-tinh-nang
git push origin develop

# Khi sẵn sàng release
git checkout main
git merge develop
git tag v1.1.0
git push origin main --tags
```

## 🧪 Các thí nghiệm có thể thực hiện

### 1. Thêm AI Model khác
```python
# Trong experiment/advanced-ai-features
class MultiAIManager:
    def __init__(self):
        self.gemini = GeminiAPI()
        self.openai = OpenAIAPI()
        self.claude = ClaudeAPI()
    
    def get_best_response(self, prompt: str) -> str:
        """Try multiple AI models and pick best result"""
        # Implementation here
```

### 2. Real-time Processing
```python
# Trong experiment/real-time-processing
import asyncio
import websockets

class RealTimeProcessor:
    async def process_live_content(self, websocket, path):
        """Process content in real-time via WebSocket"""
        # Implementation here
```

### 3. Content Analytics
```python
# Trong experiment/analytics
class ContentAnalytics:
    def analyze_performance(self, content: str) -> dict:
        """Analyze content performance metrics"""
        # Implementation here
```

## 📝 Ghi chú quan trọng

1. **Luôn test trước khi commit**
2. **Sử dụng conventional commits**
3. **Tạo Pull Request để review code**
4. **Không merge trực tiếp vào main**
5. **Backup code quan trọng trước khi thử nghiệm**

## 🔧 Công cụ hỗ trợ

```bash
# Cài đặt dependencies phát triển
pip install -r requirements-dev.txt

# Chạy tests
python -m pytest

# Format code
black .
isort .

# Type checking
mypy app/

# Linting
flake8 .
```

## 🚨 Xử lý lỗi

```bash
# Nếu nhánh bị lỗi
git checkout develop
git branch -D feature/broken-feature
git checkout -b feature/fixed-feature

# Nếu cần reset về trạng thái cũ
git reset --hard HEAD~1

# Nếu cần merge từ nhánh khác
git checkout feature/your-feature
git merge develop
```

