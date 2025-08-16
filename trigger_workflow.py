#!/usr/bin/env python3

import requests
import json
import os
import time

def trigger_workflow():
    """Trigger the GitHub Actions workflow manually"""
    print("🚀 Triggering GitHub Actions workflow...")
    
    # Repository details
    owner = "MatrixDKK"
    repo = "seo-analysis-automation"
    workflow_id = "daily_seo_analysis.yml"
    
    # Get token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ No GitHub token found. Please set GITHUB_TOKEN environment variable.")
        return False
    
    # API endpoint for triggering workflow
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "ref": "main"
    }
    
    try:
        print(f"📤 Sending workflow trigger request...")
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 204:
            print("✅ Workflow triggered successfully!")
            print("\n📊 Workflow Status:")
            print(f"Repository: https://github.com/{owner}/{repo}")
            print(f"Actions: https://github.com/{owner}/{repo}/actions")
            print(f"Workflow: Daily SEO Analysis")
            
            print("\n⏰ The workflow is now running and will:")
            print("1. Check Devoteam's Google ranking")
            print("2. Analyze 3 Devoteam pages")
            print("3. Calculate SEO metrics")
            print("4. Upload results to Snowflake")
            print("5. Generate analysis artifacts")
            
            print(f"\n🔍 Monitor progress at:")
            print(f"https://github.com/{owner}/{repo}/actions")
            
            return True
        else:
            print(f"❌ Failed to trigger workflow: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error triggering workflow: {e}")
        return False

def check_workflow_status():
    """Check the status of the latest workflow run"""
    print("\n🔍 Checking workflow status...")
    
    owner = "MatrixDKK"
    repo = "seo-analysis-automation"
    
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ No GitHub token found.")
        return
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    # Get workflow runs
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            runs = response.json()
            if runs['workflow_runs']:
                latest_run = runs['workflow_runs'][0]
                status = latest_run['status']
                conclusion = latest_run.get('conclusion', 'running')
                
                print(f"📊 Latest Workflow Run:")
                print(f"   Status: {status}")
                print(f"   Conclusion: {conclusion}")
                print(f"   URL: {latest_run['html_url']}")
                
                if status == 'completed':
                    if conclusion == 'success':
                        print("✅ Workflow completed successfully!")
                        print("📄 Check the artifacts for analysis results")
                    else:
                        print(f"❌ Workflow failed: {conclusion}")
                elif status == 'in_progress':
                    print("🔄 Workflow is currently running...")
                    print("⏰ This usually takes 2-3 minutes")
                else:
                    print(f"📋 Workflow status: {status}")
            else:
                print("❌ No workflow runs found")
        else:
            print(f"❌ Failed to get workflow runs: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking workflow status: {e}")

def main():
    """Main function"""
    print("🎯 Triggering SEO Analysis Workflow")
    print("=" * 50)
    
    # Trigger the workflow
    if trigger_workflow():
        print("\n⏳ Waiting 10 seconds for workflow to start...")
        time.sleep(10)
        
        # Check status
        check_workflow_status()
        
        print("\n🎉 Workflow triggered successfully!")
        print("📊 Monitor the execution at:")
        print("https://github.com/MatrixDKK/seo-analysis-automation/actions")
        
        print("\n📋 What's happening:")
        print("1. GitHub Actions is setting up the environment")
        print("2. Installing Python dependencies")
        print("3. Running the SEO analysis script")
        print("4. Uploading results to Snowflake")
        print("5. Generating analysis artifacts")
        
        print("\n⏰ Expected completion time: 2-3 minutes")
        
    else:
        print("\n❌ Failed to trigger workflow")
        print("Please check the error messages above")

if __name__ == "__main__":
    main()
