#!/usr/bin/env python3
"""
GitHub Token Test - Verify your token works with GitHub API
Loads token from environment variables for security
"""

import os
import requests
from dotenv import load_dotenv


def test_github_token():
    """Test GitHub token with your credentials"""
    # Load from environment variables
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        print("❌ No GitHub token found in environment variables")
        print("   Make sure GITHUB_TOKEN is set in your .env file")
        return False
    
    print("🔑 Testing GitHub Token...")
    print(f"Token: {token[:10]}...{token[-4:]}")
    
    try:
        # Test token with GitHub API
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Test user access
        user_response = requests.get(
            "https://api.github.com/user", 
            headers=headers
        )
        
        if user_response.status_code == 200:
            user_data = user_response.json()
            print(f"✅ GitHub Token: VALID")
            print(f"   Username: {user_data.get('login')}")
            print(f"   Name: {user_data.get('name')}")
            
            # Test repository access
            repos_response = requests.get(
                "https://api.github.com/user/repos", 
                headers=headers,
                params={"per_page": 5}
            )
            
            if repos_response.status_code == 200:
                repos = repos_response.json()
                print(f"   Accessible repos: {len(repos)} (showing first 5)")
                for repo in repos:
                    print(f"     - {repo['full_name']}")
            else:
                print(f"   ⚠️ Repos access failed: {repos_response.status_code}")
            
            # Check specific AI Qube repositories
            print("\n🔍 Checking AI Qube repositories:")
            ai_qube_repos = [
                "OoSos/ai-qube-centaur-ecosystem",
                "OoSos/ai-qube-financial-rust"
            ]
            
            for repo_name in ai_qube_repos:
                repo_response = requests.get(
                    f"https://api.github.com/repos/{repo_name}",
                    headers=headers
                )
                if repo_response.status_code == 200:
                    print(f"   ✅ {repo_name} - Accessible")
                else:
                    print(f"   ❌ {repo_name} - Not accessible ({repo_response.status_code})")
            
            return True
            
        else:
            print(f"❌ GitHub Token: INVALID")
            print(f"   Status Code: {user_response.status_code}")
            print(f"   Response: {user_response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False


if __name__ == "__main__":
    print("🎯 AI QUBE GITHUB TOKEN TEST")
    print("=" * 40)
    
    success = test_github_token()
    
    if success:
        print("\n" + "=" * 40)
        print("🎉 GitHub integration ready for AI Qube!")
        print("✅ Token valid for repository operations")
        print("🚀 Enhanced Git functionality enabled")
    else:
        print("\n" + "=" * 40)
        print("❌ GitHub integration setup needed")
        print("💡 Check your .env file and token permissions")
