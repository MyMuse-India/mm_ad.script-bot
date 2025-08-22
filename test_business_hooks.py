#!/usr/bin/env python3
"""Test the improved business couple hooks that match the transcript structure"""

from enhanced_script_generator import EnhancedScriptGenerator

def test_business_hooks():
    print("💼 Testing Improved Business Couple Hooks")
    print("=" * 60)
    
    # Your transcript
    transcript = "As a couple who run to businesses together, even our flights turn into meeting press or brainstorming sessions. Sets, calls, launches, it never ends. But at night, we carve out time for us to luxuriate in intimacy. And that's when the lovers bundle comes in. It doesn't just come in handy. It elevates. Depends. Leaves us, Bratless."
    
    print(f"📝 Original Transcript ({len(transcript.split())} words):")
    print(transcript)
    print()
    
    try:
        generator = EnhancedScriptGenerator('mymuse_training_data.json')
        
        # Generate script
        print("📝 Generated Script:")
        script = generator.generate_human_script("lovers bundle", transcript, gen_z=False)
        print(script)
        print(f"Lines: {len(script.split(chr(10)))}")
        print(f"Words: {len(script.split())}")
        print()
        
        # Generate 5 variations to show the hooks
        print("🔄 Variations (5) - Showing Business Couple Hooks:")
        variations = generator.generate_variations("lovers bundle", transcript, count=5, gen_z=False)
        for i, variation in enumerate(variations, 1):
            print(f"Variation {i}:")
            print(variation["text"])
            print(f"Words: {len(variation['text'].split())}")
            print("-" * 50)
        
        # Check if hooks are prominent
        script_text = script.lower()
        has_business_hook = any(phrase in script_text for phrase in [
            "as a couple who run businesses together",
            "when you're building empires together",
            "for couples who work and travel as one",
            "when your flights become boardroom extensions"
        ])
        
        print(f"✅ Business Couple Hook: {'YES' if has_business_hook else 'NO'}")
        print(f"✅ Matches Transcript Structure: {'YES' if has_business_hook else 'NO'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_business_hooks()
