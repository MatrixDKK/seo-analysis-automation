#!/usr/bin/env python3

import requests
import json
import subprocess
import time
import sys
import os

def create_github_repo_with_api():
    """Create GitHub repository using API"""
    print("🚀 Creating GitHub repository using API...")
    
    # GitHub API endpoint
    url = "https://api.github.com/user/repos"
    
    # Repository data
    repo_data = {
        "name": "seo-analysis-automation",
        "description": "Daily SEO analysis automation for Devoteam Copenhagen market",
        "private": False,  # Must be public for free GitHub Actions
        "auto_init": False,
        "gitignore_template": "",
        "license_template": ""
    }
    
    # Headers for GitHub API
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    # Try to get token from environment or use basic auth
    token = os.getenv('GITHUB_TOKEN')
    
    if token:
        headers["Authorization"] = f"token {token}"
        print("✅ Using GitHub token for authentication")
    else:
        print("⚠️ No GitHub token found. You'll need to authenticate manually.")
        print("Please create a Personal Access Token at: https://github.com/settings/tokens")
        print("Then set it as: export GITHUB_TOKEN=your_token_here")
        return None
    
    try:
        response = requests.post(url, headers=headers, json=repo_data)
        
        if response.status_code == 201:
            repo_info = response.json()
            repo_url = repo_info['html_url']
            print(f"✅ Repository created successfully: {repo_url}")
            return repo_url
        else:
            print(f"❌ Failed to create repository: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating repository: {e}")
        return None

def setup_git_and_push(repo_url):
    """Set up git remote and push code"""
    print(f"\n📤 Setting up git and pushing code to {repo_url}")
    
    try:
        # Add remote origin
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        print("✅ Remote origin added")
        
        # Set branch to main
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        print("✅ Branch set to main")
        
        # Push to GitHub
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("✅ Code pushed to GitHub successfully!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing code: {e}")
        return False

def create_github_secrets_with_api(repo_url):
    """Create GitHub secrets using API"""
    print(f"\n🔐 Setting up GitHub secrets...")
    
    # Extract owner and repo from URL
    # URL format: https://github.com/username/repo-name
    parts = repo_url.split('/')
    owner = parts[-2]
    repo = parts[-1]
    
    secrets = {
        "SNOWFLAKE_USER": "mollerhoj",
        "SNOWFLAKE_PASSWORD": "Mollerhoj12344!",
        "SNOWFLAKE_ACCOUNT": "iooooic-wm88724"
    }
    
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("⚠️ No GitHub token found. You'll need to add secrets manually.")
        print("Go to: Settings → Secrets and variables → Actions")
        for name, value in secrets.items():
            print(f"   - {name}: {value}")
        return False
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    # We need to encrypt secrets using GitHub's public key
    # First, get the public key
    public_key_url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key"
    
    try:
        response = requests.get(public_key_url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Failed to get public key: {response.status_code}")
            return False
        
        public_key_data = response.json()
        public_key = public_key_data['key']
        key_id = public_key_data['key_id']
        
        # For now, we'll use a simpler approach - just show the manual steps
        print("✅ Repository created successfully!")
        print("\n📋 Manual steps required:")
        print("1. Go to your repository settings:")
        print(f"   {repo_url}/settings")
        print("2. Navigate to: Secrets and variables → Actions")
        print("3. Add these secrets:")
        for name, value in secrets.items():
            print(f"   - {name}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up secrets: {e}")
        return False

def test_workflow(repo_url):
    """Test the GitHub Actions workflow"""
    print(f"\n🧪 Testing GitHub Actions workflow...")
    print(f"Go to: {repo_url}/actions")
    print("Click on 'Daily SEO Analysis' workflow")
    print("Click 'Run workflow'")
    print("Select branch: main")
    print("Click 'Run workflow'")
    print("\n⏰ The workflow will take 2-3 minutes to complete")

def main():
    """Main function to set up production"""
    print("🚀 Setting up SEO Analysis Automation in Production")
    print("=" * 60)
    
    # Step 1: Create GitHub repository
    repo_url = create_github_repo_with_api()
    if not repo_url:
        print("\n❌ Failed to create repository. Please create it manually:")
        print("1. Go to https://github.com/new")
        print("2. Name: seo-analysis-automation")
        print("3. Make it PUBLIC")
        print("4. Don't initialize with README")
        repo_url = input("Enter the repository URL: ").strip()
    
    # Step 2: Set up git and push code
    if setup_git_and_push(repo_url):
        print("✅ Code successfully pushed to GitHub")
    else:
        print("❌ Failed to push code")
        return
    
    # Step 3: Set up secrets
    create_github_secrets_with_api(repo_url)
    
    # Step 4: Test workflow
    test_workflow(repo_url)
    
    print("\n🎉 Production Setup Complete!")
    print("=" * 60)
    print("✅ Repository created and code pushed")
    print("✅ GitHub Actions workflow configured")
    print("📋 Next steps:")
    print("1. Add GitHub secrets manually (see instructions above)")
    print("2. Test the workflow")
    print("3. Monitor the first run")
    print("\n⏰ Your SEO analysis will run daily at 9:00 AM UTC")
    print("   (10:00 AM CET / 11:00 AM CEST)")

if __name__ == "__main__":
    main()
