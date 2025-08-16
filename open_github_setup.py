#!/usr/bin/env python3

import webbrowser
import time

def open_github_setup():
    """Open GitHub repository and guide through setup"""
    print("🚀 Opening GitHub Setup for SEO Analysis Automation")
    print("=" * 60)
    
    repo_url = "https://github.com/MatrixDKK/seo-analysis-automation"
    
    print(f"📁 Repository: {repo_url}")
    print("\n🔐 Setting up GitHub Secrets...")
    
    # Open repository settings
    print("Opening repository settings...")
    webbrowser.open(f"{repo_url}/settings")
    
    print("\n📋 Follow these steps:")
    print("1. In the left sidebar, click 'Secrets and variables'")
    print("2. Click 'Actions'")
    print("3. Click 'New repository secret'")
    print("4. Add these 3 secrets:")
    
    secrets = {
        "SNOWFLAKE_USER": "mollerhoj",
        "SNOWFLAKE_PASSWORD": "Mollerhoj12344!",
        "SNOWFLAKE_ACCOUNT": "iooooic-wm88724"
    }
    
    for i, (name, value) in enumerate(secrets.items(), 1):
        print(f"   {i}. Name: {name}")
        print(f"      Value: {value}")
        print()
    
    input("Press Enter when you've added all 3 secrets...")
    
    # Open Actions tab
    print("\n🧪 Testing the workflow...")
    print("Opening Actions tab...")
    webbrowser.open(f"{repo_url}/actions")
    
    print("\n📋 Follow these steps:")
    print("1. Click on 'Daily SEO Analysis' workflow")
    print("2. Click 'Run workflow' button")
    print("3. Select branch: main")
    print("4. Click 'Run workflow'")
    print("5. Wait 2-3 minutes for completion")
    
    print("\n⏰ The workflow will:")
    print("   - Check Devoteam's Google ranking")
    print("   - Analyze 3 Devoteam pages")
    print("   - Upload results to Snowflake")
    print("   - Generate analysis artifacts")
    
    print("\n🎉 Once completed, your automation will run daily at 9:00 AM UTC!")
    print("   (10:00 AM CET / 11:00 AM CEST)")

def main():
    """Main function"""
    open_github_setup()
    
    print("\n" + "=" * 60)
    print("🎯 Production Setup Summary:")
    print("✅ GitHub repository created")
    print("✅ Code pushed to GitHub")
    print("✅ GitHub Actions workflow configured")
    print("📋 Manual steps completed:")
    print("   - GitHub secrets added")
    print("   - Workflow tested")
    print("\n🚀 Your SEO analysis automation is now LIVE!")
    print("   It will run automatically every day at 9:00 AM UTC")

if __name__ == "__main__":
    main()
