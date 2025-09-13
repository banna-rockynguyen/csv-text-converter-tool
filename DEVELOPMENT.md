# Development Guide

## Branch Strategy

### Main Branches

- **`main`**: Production-ready code, stable releases
- **`develop`**: Integration branch for features, development staging

### Feature Branches

- **`feature/*`**: New features and enhancements
  - `feature/advanced-ai-features`: Enhanced AI capabilities
  - `feature/ui-improvements`: User interface enhancements
  - `feature/performance-optimization`: Performance improvements

### Experiment Branches

- **`experiment/*`**: Experimental features and proof-of-concepts
  - `experiment/multi-language-support`: Multi-language content support
  - `experiment/batch-processing`: Batch processing capabilities
  - `experiment/api-integration`: External API integrations

## Development Workflow

### 1. Starting New Development

```bash
# Switch to develop branch
git checkout develop
git pull origin develop

# Create new feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b experiment/your-experiment-name
```

### 2. Development Process

```bash
# Make your changes
# Test your changes
python -m pytest tests/

# Commit your changes
git add .
git commit -m "feat: add new feature description"

# Push to remote
git push origin feature/your-feature-name
```

### 3. Merging Back

```bash
# Switch to develop
git checkout develop

# Merge feature branch
git merge feature/your-feature-name

# Push to develop
git push origin develop
```

## Experimental Features

### Multi-Language Support (`experiment/multi-language-support`)

**Goal**: Support content generation in multiple languages

**Planned Features**:
- Language detection from input content
- Multi-language AI prompts
- Language-specific formatting rules
- Translation capabilities
- Localized hashtags and CTAs

**Implementation Ideas**:
- Add language detection using `langdetect` library
- Extend AI prompts with language-specific instructions
- Create language-specific formatting templates
- Add translation API integration

### Batch Processing (`experiment/batch-processing`)

**Goal**: Process multiple JSON files simultaneously

**Planned Features**:
- Bulk file upload
- Queue-based processing
- Progress tracking
- Batch result export
- Error handling and reporting

**Implementation Ideas**:
- Add Celery for background task processing
- Create batch upload interface
- Implement progress tracking with WebSockets
- Add batch result management

### API Integration (`experiment/api-integration`)

**Goal**: Integrate with external services and APIs

**Planned Features**:
- GoHighLevel API integration
- Social media platform APIs
- Content scheduling
- Analytics integration
- Webhook support

**Implementation Ideas**:
- Add GoHighLevel SDK integration
- Create social media posting APIs
- Implement content scheduling system
- Add analytics tracking

## Code Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Use meaningful variable names

### Git Commit Messages

- Use conventional commits format
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting
- `refactor:` for code refactoring
- `test:` for tests
- `chore:` for maintenance

### Testing

- Write unit tests for new features
- Test AI integration thoroughly
- Test CSV output format
- Test error handling

## Environment Setup

### Development Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install
```

### Environment Variables

Copy `env.example` to `.env` and configure:

```bash
cp env.example .env
```

## Deployment

### Local Development

```bash
python run.py
```

### Production Deployment

```bash
# Use production WSGI server
gunicorn -w 4 -b 0.0.0.0:5001 app.main:app
```

## Monitoring and Logging

- Use structured logging
- Monitor API usage and performance
- Track error rates
- Monitor AI API costs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Gemini API](https://ai.google.dev/)
- [GoHighLevel API](https://highlevel.stoplight.io/)
- [PEP 8 Style Guide](https://pep8.org/)
