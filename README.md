# CSV Text Converter Tool

A powerful tool for converting JSON content to GoHighLevel CSV format with AI-powered content enhancement using Google Gemini 2.5 Pro.

## Features

- **JSON to CSV Conversion**: Convert JSON input to GoHighLevel-compatible CSV format
- **AI Content Enhancement**: Use Google Gemini 2.5 Pro API for intelligent content formatting
- **Multiple Content Types**: Support for Carousel, Poll, Short Story, Listing, Quote Card formats
- **Platform Optimization**: Tailored formatting for LinkedIn, Facebook, Instagram, TikTok
- **Smart Formatting**: Automatic conversion of structured tags to readable format
- **UTM Tracking**: Built-in UTM parameter management
- **Required Hashtags**: Automatic inclusion of mandatory hashtags

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/csv-text-converter-tool.git
cd csv-text-converter-tool
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Gemini API key
```

## Usage

1. Start the application:
```bash
python run.py
```

2. Open your browser and go to: http://localhost:5001

3. Navigate to the JSON converter: http://localhost:5001/json

4. Input your JSON content and configure AI settings

5. Download the generated CSV file

## API Endpoints

- `GET /` - Main page
- `GET /json` - JSON converter interface
- `POST /api/parse-json` - Parse JSON and generate CSV
- `POST /api/download-csv` - Download generated CSV file

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### AI Settings

- **Enable AI**: Toggle AI-powered content enhancement
- **Platform**: Select target platform (LinkedIn, Facebook, Instagram, TikTok)
- **API Key**: Your Google Gemini 2.5 Pro API key

## Content Formatting

The tool automatically converts structured tags to readable format:

- `[TITLE]...[/TITLE]` → **TITLE** (in caps)
- `[HIGHLIGHT]...[/HIGHLIGHT]` → **HIGHLIGHT** (in caps)
- `[CTA]...[/CTA]` → 👉 **CTA** (in caps)
- `[EMOJI]` → Removed (emoji preserved)
- `[HASHTAGS]...[/HASHTAGS]` → #hashtag1 #hashtag2
- `[BLOCK]` → Line breaks for visual separation

## Supported Content Types

1. **Carousel**: Multi-slide content with structured data
2. **Poll**: Interactive polls with multiple choice questions
3. **Short Story**: Narrative content with hooks and lessons
4. **Listing**: Bullet-point content with highlights
5. **Quote Card**: Quote-based content with attribution

## Development

### Project Structure

```
csv-text-converter-tool/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Flask application
│   ├── enhanced_json_parser.py # JSON parsing and AI integration
│   └── ...
├── templates/
│   ├── index.html
│   └── json_template.html
├── static/
├── requirements.txt
├── run.py
└── README.md
```

### Branches

- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: Feature development branches
- `experiment/*`: Experimental features

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email support@banna.vn or create an issue in this repository.

## Changelog

### v1.0.0
- Initial release
- JSON to CSV conversion
- AI-powered content enhancement
- Multi-platform support
- Structured tag formatting