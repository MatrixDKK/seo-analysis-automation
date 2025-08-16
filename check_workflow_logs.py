#!/usr/bin/env python3

import requests
import json
import os

def get_workflow_logs():
    """Get the logs from the latest workflow run"""
    print("🔍 Checking workflow logs...")
    
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
    
    # Get latest workflow run
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            runs = response.json()
            if runs['workflow_runs']:
                latest_run = runs['workflow_runs'][0]
                run_id = latest_run['id']
                
                print(f"📊 Latest Workflow Run:")
                print(f"   ID: {run_id}")
                print(f"   Status: {latest_run['status']}")
                print(f"   Conclusion: {latest_run.get('conclusion', 'None')}")
                print(f"   URL: {latest_run['html_url']}")
                
                # Get jobs for this run
                jobs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/jobs"
                jobs_response = requests.get(jobs_url, headers=headers)
                
                if jobs_response.status_code == 200:
                    jobs = jobs_response.json()
                    print(f"\n📋 Jobs in this run:")
                    
                    for job in jobs['jobs']:
                        print(f"\n🔧 Job: {job['name']}")
                        print(f"   Status: {job['status']}")
                        print(f"   Conclusion: {job.get('conclusion', 'None')}")
                        
                        if job.get('conclusion') == 'failure':
                            print(f"   ❌ This job failed!")
                            
                            # Get logs for this job
                            logs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/jobs/{job['id']}/logs"
                            logs_response = requests.get(logs_url, headers=headers)
                            
                            if logs_response.status_code == 200:
                                print(f"   📄 Logs (last 500 chars):")
                                logs = logs_response.text
                                print(f"   {logs[-500:]}")
                            else:
                                print(f"   ❌ Could not get logs: {logs_response.status_code}")
                
                return latest_run
            else:
                print("❌ No workflow runs found")
        else:
            print(f"❌ Failed to get workflow runs: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking workflow logs: {e}")

def main():
    """Main function"""
    print("🔍 Workflow Logs Analysis")
    print("=" * 50)
    
    latest_run = get_workflow_logs()
    
    if latest_run:
        print(f"\n📋 Analysis:")
        if latest_run.get('conclusion') == 'failure':
            print("❌ The workflow failed. Common causes:")
            print("1. GitHub secrets not configured")
            print("2. Snowflake connection issues")
            print("3. Python dependency issues")
            print("4. Network connectivity problems")
            
            print(f"\n🔧 To fix:")
            print("1. Add GitHub secrets:")
            print("   - Go to: https://github.com/MatrixDKK/seo-analysis-automation/settings")
            print("   - Navigate to: Secrets and variables → Actions")
            print("   - Add: SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT")
            
            print("2. Check the detailed logs at:")
            print(f"   {latest_run['html_url']}")
            
            print("3. Test locally first:")
            print("   python3 daily_seo_analysis.py")
        else:
            print("✅ Workflow completed successfully!")

if __name__ == "__main__":
    main()
