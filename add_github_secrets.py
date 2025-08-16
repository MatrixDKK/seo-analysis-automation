#!/usr/bin/env python3

import requests
import json
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

def get_public_key(owner, repo, token):
    """Get GitHub repository's public key for encrypting secrets"""
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to get public key: {response.status_code}")
        return None

def encrypt_secret(secret_value, public_key):
    """Encrypt a secret value using GitHub's public key"""
    try:
        # Decode the public key
        public_key_bytes = base64.b64decode(public_key)
        
        # Load the public key
        from cryptography.hazmat.primitives.asymmetric import rsa
        pub_key = serialization.load_der_public_key(public_key_bytes)
        
        # Encrypt the secret
        encrypted = pub_key.encrypt(
            secret_value.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        print(f"❌ Error encrypting secret: {e}")
        return None

def add_secret(owner, repo, secret_name, secret_value, token):
    """Add a secret to GitHub repository"""
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/{secret_name}"
    
    # Get public key
    public_key_data = get_public_key(owner, repo, token)
    if not public_key_data:
        return False
    
    # Encrypt the secret
    encrypted_value = encrypt_secret(secret_value, public_key_data['key'])
    if not encrypted_value:
        return False
    
    # Prepare the request
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    
    data = {
        "encrypted_value": encrypted_value,
        "key_id": public_key_data['key_id']
    }
    
    # Add the secret
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [201, 204]:
        print(f"✅ Secret '{secret_name}' added successfully")
        return True
    else:
        print(f"❌ Failed to add secret '{secret_name}': {response.status_code}")
        print(f"Response: {response.text}")
        return False

def main():
    """Main function to add all secrets"""
    print("🔐 Adding GitHub Secrets for SEO Analysis Automation")
    print("=" * 60)
    
    # Repository details
    owner = "MatrixDKK"
    repo = "seo-analysis-automation"
    
    # Get token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ No GitHub token found. Please run create_github_token.py first.")
        return
    
    # Secrets to add
    secrets = {
        "SNOWFLAKE_USER": "mollerhoj",
        "SNOWFLAKE_PASSWORD": "Mollerhoj12344!",
        "SNOWFLAKE_ACCOUNT": "iooooic-wm88724"
    }
    
    print(f"📁 Repository: {owner}/{repo}")
    print(f"🔑 Adding {len(secrets)} secrets...")
    
    success_count = 0
    for name, value in secrets.items():
        print(f"\nAdding {name}...")
        if add_secret(owner, repo, name, value, token):
            success_count += 1
    
    print(f"\n📊 Results: {success_count}/{len(secrets)} secrets added successfully")
    
    if success_count == len(secrets):
        print("\n🎉 All secrets added successfully!")
        print("✅ Your GitHub Actions workflow is ready to run!")
        print("\n🧪 Next step: Test the workflow")
        print("Go to: https://github.com/MatrixDKK/seo-analysis-automation/actions")
        print("Click on 'Daily SEO Analysis' → 'Run workflow'")
    else:
        print("\n⚠️ Some secrets failed to add. You may need to add them manually.")
        print("Go to: Settings → Secrets and variables → Actions")

if __name__ == "__main__":
    main()
