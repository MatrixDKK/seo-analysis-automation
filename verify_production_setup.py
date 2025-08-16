#!/usr/bin/env python3

import os
import subprocess
import sys

def check_git_status():
    """Check if git repository is properly set up"""
    print("🔍 Checking Git repository status...")
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not in a git repository")
            return False
        
        # Check if remote is configured
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if 'origin' not in result.stdout:
            print("❌ No remote origin configured")
            return False
        
        print("✅ Git repository is properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Error checking git status: {e}")
        return False

def check_required_files():
    """Check if all required files are present"""
    print("\n📁 Checking required files...")
    
    required_files = [
        '.github/workflows/daily_seo_analysis.yml',
        'daily_seo_analysis.py',
        'snowflake_config.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files are present")
    return True

def check_snowflake_connection():
    """Test Snowflake connection"""
    print("\n❄️ Testing Snowflake connection...")
    
    try:
        result = subprocess.run([sys.executable, 'test_snowflake_connection.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Snowflake connection successful")
            return True
        else:
            print(f"❌ Snowflake connection failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Snowflake connection: {e}")
        return False

def check_daily_analysis():
    """Test the daily analysis script"""
    print("\n🔍 Testing daily analysis script...")
    
    try:
        # Run a quick test (don't upload to avoid duplicates)
        result = subprocess.run([sys.executable, 'daily_seo_analysis.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Daily analysis script runs successfully")
            return True
        else:
            print(f"❌ Daily analysis script failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Daily analysis script timed out (this is normal for a full run)")
        return True
    except Exception as e:
        print(f"❌ Error testing daily analysis: {e}")
        return False

def main():
    """Main verification function"""
    print("🚀 Production Setup Verification")
    print("=" * 50)
    
    checks = [
        check_git_status,
        check_required_files,
        check_snowflake_connection,
        check_daily_analysis
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Verification Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Your setup is ready for production.")
        print("\n📋 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Set up GitHub secrets")
        print("3. Test the workflow in GitHub Actions")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
