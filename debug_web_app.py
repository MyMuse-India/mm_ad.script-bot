#!/usr/bin/env python3
"""
Debug script to test the exact same path the web app uses
"""

import os
import sys

def test_web_app_path():
    print("🔍 Testing web app execution path...")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script directory: {os.path.dirname(__file__)}")
    print(f"Files in current directory: {os.listdir('.')}")
    
    # Test the exact import path the web app uses
    try:
        print("\n🎯 Testing import of EnhancedScriptGenerator...")
        from enhanced_script_generator import EnhancedScriptGenerator
        print("✅ Import successful")
        
        # Test the exact path construction the web app uses
        training_data_path = os.path.join(os.path.dirname(__file__), "mymuse_training_data.json")
        print(f"🔍 Training data path: {training_data_path}")
        print(f"🔍 File exists: {os.path.exists(training_data_path)}")
        
        # Test initialization
        print("\n🎯 Testing initialization...")
        generator = EnhancedScriptGenerator(training_data_path)
        print("✅ Initialization successful")
        
        # Test the exact transcript from the web app
        transcript = """As a couple who run two businesses together, even our flights turn into meeting preps or brainstorming sessions. Friends, calls, launches, it never ends. But at night, we carve out time for us to luxuriate in intimacy. And that's when the lover's bundle comes in. It doesn't just come in handy, it elevates, deepens, leaves us breathless. And that's when the lover's bundle comes in."""
        
        print(f"\n🎯 Testing script generation with transcript: {transcript[:100]}...")
        script = generator.generate_human_script('dive+', transcript)
        print(f"✅ Script generated successfully")
        print(f"🔍 Script length: {len(script)}")
        print(f"🔍 Script content: {repr(script)}")
        print(f"🔍 Script lines: {len([line for line in script.split('\\n') if line.strip()])}")
        
        # Test variations generation
        print(f"\n🎯 Testing variations generation...")
        variations = generator.generate_variations('dive+', transcript, 10, False)
        print(f"✅ Variations generated successfully")
        print(f"🔍 Number of variations: {len(variations)}")
        
        if variations:
            print(f"🔍 First variation: {repr(variations[0]['text'])}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_web_app_path()
