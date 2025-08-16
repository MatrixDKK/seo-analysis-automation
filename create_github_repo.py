#!/usr/bin/env python3

import webbrowser
import subprocess
import time
import sys

def open_github_new_repo():
    """Open GitHub new repository page"""
    print("🌐 Opening GitHub new repository page...")
    webbrowser.open("https://github.com/new")
    
    print("\n📋 Follow these steps:")
    print("1. Repository name: seo-analysis-automation")
    print("2. Description: Daily SEO analysis automation for Devoteam")
    print("3. Make it PUBLIC (required for free GitHub Actions)")
    print("4. DO NOT check 'Add a README file'")
    print("5. DO NOT check 'Add .gitignore'")
    print("6. DO NOT check 'Choose a license'")
    print("7. Click 'Create repository'")
    
    input("\nPress Enter when you've created the repository...")

def get_repo_url():
    """Get the repository URL from user"""
    print("\n🔗 Please provide your GitHub repository URL:")
    print("It should look like: https://github.com/MatrixDKK/seo-analysis-automation")
    
    repo_url = input("Repository URL: ").strip()
    
    if not repo_url.startswith("https://github.com/"):
        print("❌ Invalid GitHub URL. Please try again.")
        return get_repo_url()
    
    return repo_url

def setup_remote_and_push(repo_url):
    """Set up remote and push code"""
    print(f"\n🚀 Setting up remote and pushing code to {repo_url}")
    
    try:
        # Add remote origin
        print("Adding remote origin...")
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        print("✅ Remote origin added")
        
        # Set branch to main
        print("Setting branch to main...")
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        print("✅ Branch set to main")
        
        # Push to GitHub
        print("Pushing code to GitHub...")
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("✅ Code pushed to GitHub successfully!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def show_next_steps(repo_url):
    """Show the next steps for setting up secrets"""
    print("\n🎉 Repository created and code pushed successfully!")
    print(f"📁 Repository: {repo_url}")
    
    print("\n📋 Next steps:")
    print("1. Go to your repository settings:")
    print(f"   {repo_url}/settings")
    
    print("\n2. Navigate to Secrets and variables → Actions")
    print("   (Click on 'Secrets and variables' in the left sidebar, then 'Actions')")
    
    print("\n3. Add these three repository secrets:")
    print("   Click 'New repository secret' for each:")
    print("   - Name: SNOWFLAKE_USER, Value: mollerhoj")
    print("   - Name: SNOWFLAKE_PASSWORD, Value: Mollerhoj12344!")
    print("   - Name: SNOWFLAKE_ACCOUNT, Value: iooooic-wm88724")
    
    print("\n4. Test the workflow:")
    print(f"   Go to: {repo_url}/actions")
    print("   Click on 'Daily SEO Analysis' workflow")
    print("   Click 'Run workflow'")
    print("   Select branch: main")
    print("   Click 'Run workflow'")
    
    print("\n5. Monitor the execution (should take 2-3 minutes)")
    print("   You'll see green checkmarks when it completes successfully")

def main():
    """Main function to set up GitHub repository"""
    print("🚀 GitHub Repository Setup for SEO Analysis Automation")
    print("=" * 60)
    
    # Step 1: Open GitHub new repo page
    open_github_new_repo()
    
    # Step 2: Get repository URL
    repo_url = get_repo_url()
    
    # Step 3: Set up remote and push
    if setup_remote_and_push(repo_url):
        # Step 4: Show next steps
        show_next_steps(repo_url)
        
        print("\n🎯 Your SEO analysis automation will be live once you:")
        print("   - Add the GitHub secrets")
        print("   - Test the workflow")
        
        print("\n⏰ The automation will then run daily at 9:00 AM UTC")
        print("   (10:00 AM CET / 11:00 AM CEST)")
        
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
