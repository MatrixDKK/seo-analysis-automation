#!/bin/bash

echo "🚀 Setting up GitHub repository for SEO analysis automation..."
echo ""

# Check if git is configured
if ! git config --global user.name > /dev/null 2>&1; then
    echo "❌ Git is not configured. Please run these commands first:"
    echo "   git config --global user.name 'Your Name'"
    echo "   git config --global user.email 'your.email@example.com'"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "✅ Git is configured"
echo ""

echo "📋 Next steps to complete the setup:"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Create a new repository named 'seo-analysis-automation' (or any name you prefer)"
echo "3. Make it PUBLIC (required for free GitHub Actions)"
echo "4. DO NOT initialize with README, .gitignore, or license"
echo "5. Click 'Create repository'"
echo ""
echo "6. After creating the repository, GitHub will show you commands like:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/seo-analysis-automation.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "7. Replace YOUR_USERNAME with your actual GitHub username and run those commands"
echo ""
echo "8. Then set up the GitHub secrets:"
echo "   - Go to your repository → Settings → Secrets and variables → Actions"
echo "   - Add these secrets:"
echo "     * SNOWFLAKE_USER = mollerhoj"
echo "     * SNOWFLAKE_PASSWORD = Mollerhoj12344!"
echo "     * SNOWFLAKE_ACCOUNT = iooooic-wm88724"
echo ""
echo "9. Test the workflow:"
echo "   - Go to Actions tab → Daily SEO Analysis → Run workflow"
echo ""
echo "🎉 Once completed, your SEO analysis will run automatically every day at 9:00 AM UTC!"
echo ""
echo "Would you like me to help you with any of these steps?"
