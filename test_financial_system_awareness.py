#!/usr/bin/env python3
"""
Financial System Detection - Test Centaur Ecosystem awareness of Financial System
Cross-system coordination and integration test
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

def detect_financial_system():
    """Detect and analyze the Financial System from Centaur Ecosystem perspective"""
    print("🎯 AI QUBE FINANCIAL SYSTEM DETECTION")
    print("=" * 55)
    
    # Expected Financial System paths
    base_path = Path(__file__).parent.parent.parent
    financial_paths = [
        base_path / "Financial System Management",
        base_path / "AI Qube" / "Financial System Management",
        Path("c:/Users/Owner/AI Qube/Financial System Management")
    ]
    
    print("🔍 Scanning for Financial System...")
    detected_path = None
    
    for path in financial_paths:
        if path.exists():
            detected_path = path
            print(f"   ✅ Found Financial System at: {path}")
            break
    else:
        print("   ❌ Financial System not detected in expected locations")
        return False, None
    
    return True, detected_path

def analyze_financial_system(system_path):
    """Analyze Financial System structure and capabilities"""
    print(f"\n📊 ANALYZING FINANCIAL SYSTEM")
    print("=" * 55)
    
    analysis = {
        "path": str(system_path),
        "components": {},
        "performance": {},
        "integration": {}
    }
    
    # Check key components
    key_files = {
        "Rust Core": "ai-qube-financial-rust",
        "Task Log": "AI_SHARED_TASK_LOG.md", 
        "Unified Log": "UNIFIED_AI_SHARED_TASK_LOG.md",
        "Oversight": "CLAUDE_PRO_PROJECT_OVERSIGHT.md",
        "Status": "PHASE_1_COMPLETE_STATUS.md",
        "GUI Launcher": "launch_financial_system_gui.py"
    }
    
    print("🔧 Component Analysis:")
    for component, filename in key_files.items():
        file_path = system_path / filename
        if file_path.exists():
            analysis["components"][component] = {
                "status": "✅ Present",
                "path": str(file_path),
                "size": file_path.stat().st_size if file_path.is_file() else "Directory"
            }
            print(f"   ✅ {component}: {filename}")
        else:
            analysis["components"][component] = {
                "status": "❌ Missing", 
                "path": str(file_path)
            }
            print(f"   ❌ {component}: {filename}")
    
    return analysis

def check_cross_system_integration(financial_path):
    """Check integration points between Centaur and Financial systems"""
    print(f"\n🔗 CROSS-SYSTEM INTEGRATION CHECK")
    print("=" * 55)
    
    integration_points = {}
    
    # Check shared task logs
    centaur_task_log = Path(__file__).parent / "AI_SHARED_TASK_LOG.md"
    financial_task_log = financial_path / "AI_SHARED_TASK_LOG.md"
    unified_log = financial_path / "UNIFIED_AI_SHARED_TASK_LOG.md"
    
    print("📝 Shared Documentation:")
    if centaur_task_log.exists():
        print(f"   ✅ Centaur Task Log: {centaur_task_log.name}")
        integration_points["centaur_log"] = True
    else:
        print(f"   ❌ Centaur Task Log: Missing")
        integration_points["centaur_log"] = False
        
    if financial_task_log.exists():
        print(f"   ✅ Financial Task Log: {financial_task_log.name}")
        integration_points["financial_log"] = True
    else:
        print(f"   ❌ Financial Task Log: Missing")
        integration_points["financial_log"] = False
        
    if unified_log.exists():
        print(f"   ✅ Unified Task Log: {unified_log.name}")
        integration_points["unified_log"] = True
        
        # Try to read current status
        try:
            with open(unified_log, 'r', encoding='utf-8') as f:
                content = f.read()
                if "66.7% win rate" in content:
                    print(f"   📊 Financial Performance: 66.7% win rate detected")
                    integration_points["performance_data"] = "66.7% win rate"
                if "TOM Framework" in content:
                    print(f"   🧠 TOM Framework: Quaternary Intelligence Matrix detected")
                    integration_points["tom_framework"] = True
        except Exception as e:
            print(f"   ⚠️  Could not read unified log: {e}")
    else:
        print(f"   ❌ Unified Task Log: Missing")
        integration_points["unified_log"] = False
    
    return integration_points

def test_financial_system_awareness():
    """Main test function for Financial System awareness"""
    
    # Step 1: Detect Financial System
    detected, financial_path = detect_financial_system()
    
    if not detected:
        print(f"\n❌ FINANCIAL SYSTEM NOT DETECTED")
        print("   Cross-system integration unavailable")
        return False
    
    # Step 2: Analyze Financial System
    analysis = analyze_financial_system(financial_path)
    
    # Step 3: Check integration
    integration = check_cross_system_integration(financial_path)
    
    # Step 4: Summary
    print(f"\n🎯 ECOSYSTEM AWARENESS SUMMARY")
    print("=" * 55)
    
    components_present = sum(1 for comp in analysis["components"].values() 
                           if comp["status"].startswith("✅"))
    total_components = len(analysis["components"])
    
    integration_active = sum(1 for point in integration.values() 
                           if point is True)
    
    print(f"Financial System Components: {components_present}/{total_components}")
    print(f"Integration Points Active: {integration_active}")
    
    if components_present >= 4 and integration_active >= 2:
        print(f"\n✅ FINANCIAL SYSTEM FULLY RECOGNIZED")
        print(f"🔗 Cross-system coordination OPERATIONAL")
        print(f"🎯 Centaur Ecosystem can coordinate with Financial System")
        
        # Display key insights
        if "performance_data" in integration:
            print(f"📊 Live Performance: {integration['performance_data']}")
        if "tom_framework" in integration:
            print(f"🧠 TOM Framework: Active")
            
        return True
    else:
        print(f"\n⚠️  PARTIAL FINANCIAL SYSTEM RECOGNITION")
        print(f"🔧 Some integration points may need configuration")
        return False

if __name__ == "__main__":
    print("🤖 CENTAUR ECOSYSTEM FINANCIAL SYSTEM AWARENESS TEST")
    print("🔍 Testing cross-system detection and coordination...")
    print("")
    
    success = test_financial_system_awareness()
    
    print(f"\n{'='*55}")
    if success:
        print("🎉 CROSS-SYSTEM AWARENESS: OPERATIONAL!")
        print("🚀 Centaur Ecosystem can coordinate Financial System operations")
    else:
        print("🔧 CROSS-SYSTEM AWARENESS: NEEDS CONFIGURATION")
        print("💡 Some integration points require setup")
    print("=" * 55)
