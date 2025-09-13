#!/bin/bash

# Setup GitHub Repository Script
# This script helps you set up the GitHub repository

echo "🚀 Setting up GitHub repository for CSV Text Converter Tool"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Please run 'git init' first."
    exit 1
fi

# Get repository name from user
echo "📝 Please enter your GitHub username:"
read -r GITHUB_USERNAME

echo "📝 Please enter your repository name (or press Enter for 'csv-text-converter-tool'):"
read -r REPO_NAME

if [ -z "$REPO_NAME" ]; then
    REPO_NAME="csv-text-converter-tool"
fi

# Set up remote origin
echo "🔗 Setting up remote origin..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Push all branches
echo "📤 Pushing all branches to GitHub..."

# Push main branch
git checkout main
git push -u origin main

# Push develop branch
git checkout develop
git push -u origin develop

# Push feature branches
git checkout feature/advanced-ai-features
git push -u origin feature/advanced-ai-features

# Push experiment branches
git checkout experiment/multi-language-support
git push -u origin experiment/multi-language-support

git checkout experiment/batch-processing
git push -u origin experiment/batch-processing

git checkout experiment/api-integration
git push -u origin experiment/api-integration

# Switch back to main
git checkout main

echo "✅ GitHub repository setup complete!"
echo "🌐 Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "2. Update repository description and topics"
echo "3. Enable GitHub Pages if needed"
echo "4. Set up branch protection rules"
echo "5. Configure GitHub Actions for CI/CD"
echo ""
echo "🔧 Development commands:"
echo "- Switch to develop: git checkout develop"
echo "- Create new feature: git checkout -b feature/your-feature"
echo "- Create new experiment: git checkout -b experiment/your-experiment"
echo "- Run tests: python -m pytest"
echo "- Format code: black . && isort ."
echo "- Install dev dependencies: pip install -r requirements-dev.txt"
