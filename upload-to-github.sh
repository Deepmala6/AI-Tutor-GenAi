#!/bin/bash
# AI Tutor Generator - GitHub Upload Script
# Run this script to upload your project to GitHub

echo "🚀 AI Tutor Generator - GitHub Upload Script"
echo "=============================================="
echo ""

# Step 1: Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized. Run: git init"
    exit 1
fi

echo "✅ Git repository detected"
echo ""

# Step 2: Get GitHub repository URL
echo "📝 To upload to GitHub:"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Create a new repository named: AI-Tutor-Generator"
echo "3. DO NOT initialize with README or .gitignore"
echo "4. Click Create Repository"
echo ""
echo "5. Copy the repository URL (should look like:"
echo "   https://github.com/YOUR-USERNAME/AI-Tutor-Generator.git)"
echo ""

read -p "Enter your GitHub repository URL: " github_url

if [ -z "$github_url" ]; then
    echo "❌ No URL provided. Exiting."
    exit 1
fi

# Step 3: Add remote and push
echo ""
echo "⏳ Adding remote origin..."
git remote add origin "$github_url" 2>/dev/null || git remote set-url origin "$github_url"
echo "✅ Remote added"
echo ""

echo "⏳ Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Your project is now on GitHub!"
    echo ""
    echo "📊 Repository URL: $github_url"
    echo ""
    echo "✨ Next steps:"
    echo "  1. Visit your GitHub repo"
    echo "  2. Add a description"
    echo "  3. Add topics (ai, education, generator, etc.)"
    echo "  4. Share with others!"
    else
    echo ""
    echo "❌ Push failed. Check your GitHub URL and try again."
    echo "   Make sure you have:"
    echo "   - GitHub account created"
    echo "   - Repository created on GitHub"
    echo "   - Git authentication configured"
fi

echo ""
echo "Done! 🎓"
