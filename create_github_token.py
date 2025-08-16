#!/usr/bin/env python3

import webbrowser
import subprocess
import os

def create_github_token():
    """Guide user through creating a GitHub Personal Access Token"""
    print("🔑 Creating GitHub Personal Access Token")
    print("=" * 50)
    
    # Open GitHub token creation page
    print("🌐 Opening GitHub token creation page...")
    webbrowser.open("https://github.com/settings/tokens/new")
    
    print("\n📋 Follow these steps:")
    print("1. Note: 'SEO Analysis Automation Token'")
    print("2. Expiration: 'No expiration' (or 90 days)")
    print("3. Select scopes:")
    print("   ✅ repo (Full control of private repositories)")
    print("   ✅ workflow (Update GitHub Action workflows)")
    print("4. Click 'Generate token'")
    print("5. Copy the token (you won't see it again!)")
    
    input("\nPress Enter when you have the token...")
    
    # Get token from user
    token = input("Paste your GitHub token: ").strip()
    
    if len(token) < 20:
        print("❌ Token seems too short. Please check and try again.")
        return None
    
    # Set token as environment variable
    os.environ['GITHUB_TOKEN'] = token
    
    # Also save to a temporary file for the session
    with open('.github_token', 'w') as f:
        f.write(token)
    
    print("✅ Token saved for this session")
    return token

def main():
    """Main function"""
    token = create_github_token()
    if token:
        print("\n🎉 Token created successfully!")
        print("Now you can run: python3 setup_production.py")
    else:
        print("\n❌ Failed to create token")

if __name__ == "__main__":
    main()
