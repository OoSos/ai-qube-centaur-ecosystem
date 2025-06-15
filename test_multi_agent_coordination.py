#!/usr/bin/env python3
"""
Multi-Agent API Test - Demonstrate AI Qube Centaur Ecosystem capabilities
Tests Claude, Gemini, and GitHub APIs for coordinated operations
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_claude_api():
    """Test Claude API connectivity and capabilities"""
    try:
        import anthropic
        load_dotenv()
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return False, "No Claude API key found"
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Test basic capability
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{
                "role": "user", 
                "content": "What is 2+2? Respond in exactly 5 words."
            }]
        )
        
        result = response.content[0].text.strip()
        return True, f"Claude response: {result}"
        
    except Exception as e:
        return False, f"Claude error: {str(e)}"

def test_gemini_api():
    """Test Gemini API connectivity and capabilities"""
    try:
        import google.generativeai as genai
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return False, "No Gemini API key found"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test basic capability
        response = model.generate_content("Calculate 5*7 and respond with just the number.")
        result = response.text.strip()
        return True, f"Gemini response: {result}"
        
    except Exception as e:
        return False, f"Gemini error: {str(e)}"

def test_github_api():
    """Test GitHub API connectivity and repository access"""
    try:
        load_dotenv()
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return False, "No GitHub token found"
        
        headers = {"Authorization": f"token {token}"}
        response = requests.get("https://api.github.com/user", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('login')
            return True, f"GitHub user: {username}"
        else:
            return False, f"GitHub API error: {response.status_code}"
            
    except Exception as e:
        return False, f"GitHub error: {str(e)}"

def demonstrate_multi_agent_coordination():
    """Demonstrate coordinated multi-agent capabilities"""
    print("🎯 AI QUBE MULTI-AGENT COORDINATION TEST")
    print("=" * 50)
    
    # Test each agent
    agents = {
        "Claude": test_claude_api,
        "Gemini": test_gemini_api, 
        "GitHub": test_github_api
    }
    
    results = {}
    
    for agent_name, test_func in agents.items():
        print(f"\n🤖 Testing {agent_name} Agent...")
        success, message = test_func()
        results[agent_name] = {"success": success, "message": message}
        
        if success:
            print(f"   ✅ {message}")
        else:
            print(f"   ❌ {message}")
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 MULTI-AGENT SYSTEM STATUS")
    print(f"{'='*50}")
    
    active_agents = sum(1 for r in results.values() if r["success"])
    total_agents = len(results)
    
    print(f"Active Agents: {active_agents}/{total_agents}")
    
    if active_agents >= 2:
        print("✅ Multi-agent coordination READY")
        print("🚀 System capable of advanced operations")
        
        # List available capabilities
        print(f"\n🎯 AVAILABLE CAPABILITIES:")
        if results["Claude"]["success"]:
            print("   • Advanced reasoning and analysis")
            print("   • Natural language processing")
            print("   • Code generation and review")
        
        if results["Gemini"]["success"]:
            print("   • Mathematical computations")
            print("   • Data analysis and processing")
            print("   • Alternative AI perspective")
        
        if results["GitHub"]["success"]:
            print("   • Repository management")
            print("   • Code deployment and CI/CD")
            print("   • Version control operations")
            
        print(f"\n💡 EXAMPLE REQUESTS YOU CAN MAKE:")
        print("   • 'Analyze this code and suggest improvements'")
        print("   • 'Create a new feature and commit to GitHub'")
        print("   • 'Research a topic using multiple AI perspectives'")
        print("   • 'Generate documentation and update repository'")
        print("   • 'Perform mathematical analysis with validation'")
        print("   • 'Coordinate complex multi-step operations'")
        
    else:
        print("⚠️  Partial system functionality")
        print("💡 Some advanced features may be limited")
    
    return active_agents, total_agents

if __name__ == "__main__":
    active, total = demonstrate_multi_agent_coordination()
    
    print(f"\n{'='*50}")
    if active >= 2:
        print("🎉 READY FOR ADVANCED AI OPERATIONS!")
        print("Ask me to perform any complex task using multiple AI agents.")
    else:
        print("🔧 System needs additional configuration.")
    print(f"{'='*50}")
