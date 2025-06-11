#!/usr/bin/env python3
"""
AI Qube Centaur Ecosystem - Health Check Script
Performs comprehensive system health validation
"""

import os
import sys
import subprocess
import requests
import json
from datetime import datetime

def check_python_environment():
    """Check Python version and dependencies"""
    print("🐍 Checking Python Environment...")
    
    # Check Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    else:
        print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} - Requires 3.8+")
        return False
    
    # Check critical dependencies
    dependencies = [
        'requests', 'psycopg2', 'openai', 'anthropic', 
        'google.generativeai', 'weaviate'
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"  ✅ {dep} - Available")
        except ImportError:
            print(f"  ❌ {dep} - Missing")
            missing.append(dep)
    
    if missing:
        print(f"  📋 Install missing dependencies: pip install {' '.join(missing)}")
        return False
    
    return True

def check_environment_variables():
    """Check required environment variables"""
    print("\n🔑 Checking Environment Variables...")
    
    required_vars = [
        'ANTHROPIC_API_KEY',
        'OPENAI_API_KEY', 
        'GOOGLE_API_KEY',
        'POSTGRES_PASSWORD'
    ]
    
    optional_vars = [
        'GITHUB_TOKEN',
        'WEAVIATE_URL',
        'N8N_URL'
    ]
    
    missing_required = []
    for var in required_vars:
        if os.getenv(var):
            print(f"  ✅ {var} - Configured")
        else:
            print(f"  ❌ {var} - Missing")
            missing_required.append(var)
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"  ✅ {var} - Configured")
        else:
            print(f"  ⚠️ {var} - Optional (using default)")
    
    if missing_required:
        print(f"\n  📋 Set required variables:")
        for var in missing_required:
            print(f"     export {var}=\"your_key_here\"")
        return False
    
    return True

def check_database():
    """Check PostgreSQL database connectivity"""
    print("\n🗄️ Checking PostgreSQL Database...")
    
    try:
        # Check if PostgreSQL is running
        result = subprocess.run(['pg_isready', '-h', 'localhost'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("  ✅ PostgreSQL - Service Running")
            
            # Check database connection
            try:
                import psycopg2
                password = os.getenv('POSTGRES_PASSWORD', '')
                conn = psycopg2.connect(
                    host='localhost',
                    database='centaur_coordination',
                    user='postgres',
                    password=password
                )
                conn.close()
                print("  ✅ Database Connection - Successful")
                return True
            except Exception as e:
                print(f"  ❌ Database Connection - Failed: {str(e)}")
                return False
        else:
            print("  ❌ PostgreSQL - Service Not Running")
            return False
            
    except subprocess.TimeoutExpired:
        print("  ❌ PostgreSQL - Connection Timeout")
        return False
    except FileNotFoundError:
        print("  ⚠️ PostgreSQL - pg_isready command not found")
        return False

def check_weaviate():
    """Check Weaviate vector database"""
    print("\n🧠 Checking Weaviate Vector Database...")
    
    weaviate_url = os.getenv('WEAVIATE_URL', 'http://localhost:8080')
    
    try:
        response = requests.get(f"{weaviate_url}/v1/.well-known/ready", timeout=10)
        if response.status_code == 200:
            print(f"  ✅ Weaviate - Service Running ({weaviate_url})")
            return True
        else:
            print(f"  ❌ Weaviate - Service Error (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Weaviate - Connection Failed: {str(e)}")
        print(f"  💡 Start Weaviate: docker run -p 8080:8080 semitechnologies/weaviate:latest")
        return False

def check_n8n():
    """Check n8n workflow engine"""
    print("\n🔄 Checking n8n Workflow Engine...")
    
    n8n_url = os.getenv('N8N_URL', 'http://localhost:5678')
    
    try:
        response = requests.get(f"{n8n_url}/healthz", timeout=10)
        if response.status_code == 200:
            print(f"  ✅ n8n - Service Running ({n8n_url})")
            return True
        else:
            print(f"  ❌ n8n - Service Error (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ n8n - Connection Failed: {str(e)}")
        print(f"  💡 Start n8n: npx n8n start")
        return False

def check_ai_services():
    """Check AI service API connectivity"""
    print("\n🤖 Checking AI Service APIs...")
    
    services = []
    
    # Check OpenAI
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        models = client.models.list()
        print("  ✅ OpenAI API - Connected")
        services.append(True)
    except Exception as e:
        print(f"  ❌ OpenAI API - Failed: {str(e)}")
        services.append(False)
    
    # Check Anthropic (Claude)
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        # Note: Anthropic doesn't have a simple health check, so we just verify the client
        print("  ✅ Anthropic API - Key Configured")
        services.append(True)
    except Exception as e:
        print(f"  ❌ Anthropic API - Failed: {str(e)}")
        services.append(False)
    
    # Check Google Gemini
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        models = genai.list_models()
        print("  ✅ Google Gemini API - Connected")
        services.append(True)
    except Exception as e:
        print(f"  ❌ Google Gemini API - Failed: {str(e)}")
        services.append(False)
    
    return all(services)

def check_project_files():
    """Check critical project files"""
    print("\n📁 Checking Project Files...")
    
    critical_files = [
        'src/agents/agent_integration.py',
        'src/digital_twin/api.py',
        'src/rag_system/core.py',
        'scripts/deploy_n8n_workflows.py',
        'scripts/populate_rag_system.py',
        'scripts/end_to_end_integration.py',
        'database/coordination_schema.sql',
        'n8n-workflows/production-multi-agent-coordination.json'
    ]
    
    missing_files = []
    for file_path in critical_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - Missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n  📋 Missing {len(missing_files)} critical files")
        return False
    
    return True

def generate_health_report():
    """Generate comprehensive health report"""
    print("=" * 60)
    print("🏛️ AI QUBE CENTAUR ECOSYSTEM - HEALTH CHECK REPORT")
    print("=" * 60)
    print(f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        ("Python Environment", check_python_environment),
        ("Environment Variables", check_environment_variables),
        ("PostgreSQL Database", check_database),
        ("Weaviate Vector DB", check_weaviate),
        ("n8n Workflow Engine", check_n8n),
        ("AI Service APIs", check_ai_services),
        ("Project Files", check_project_files)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ {name} - Error: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 HEALTH CHECK SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {name}")
    
    print(f"\n🎯 Overall Status: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL SYSTEMS OPERATIONAL - Ready for deployment!")
        return True
    else:
        print("⚠️ ISSUES DETECTED - Please resolve before deployment")
        print("\n💡 Quick fixes:")
        print("   - Install missing dependencies: pip install -r requirements.txt")
        print("   - Set environment variables in .env file")
        print("   - Start missing services (PostgreSQL, Weaviate, n8n)")
        return False

def main():
    """Main health check execution"""
    success = generate_health_report()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
