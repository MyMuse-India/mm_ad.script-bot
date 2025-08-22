#!/usr/bin/env python3
"""Test that all 10 variations are now generated successfully"""

from enhanced_script_generator import EnhancedScriptGenerator

def test_10_variations_fixed():
    print("🔟 Testing Fixed 10 Variations Generation")
    print("=" * 60)
    
    # Your transcript
    transcript = "As a couple who run to businesses together, even our flights turn into meeting press or brainstorming sessions. Sets, calls, launches, it never ends. But at night, we carve out time for us to luxuriate in intimacy. And that's when the lovers bundle comes in. It doesn't just come in handy. It elevates. Depends. Leaves us, Bratless."
    
    print(f"📝 Transcript: {len(transcript.split())} words")
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
        
        # Generate ALL 10 variations
        print("🔄 Generating ALL 10 Variations:")
        variations = generator.generate_variations("lovers bundle", transcript, count=10, gen_z=False)
        
        print(f"✅ Total Variations Generated: {len(variations)}")
        print()
        
        # Display all variations
        for i, variation in enumerate(variations, 1):
            print(f"Variation {i}:")
            print(variation["text"])
            print(f"Lines: {len(variation['text'].split(chr(10)))}")
            print(f"Words: {len(variation['text'].split())}")
            print("-" * 50)
        
        # Verify all variations have business couple hooks
        business_hooks = [
            "as a couple who run businesses together",
            "when you're building empires together",
            "for couples who work and travel as one",
            "when your flights become boardroom extensions",
            "as business partners who never stop",
            "when meetings and intimacy collide",
            "for couples who turn every trip into opportunity",
            "when your work life and love life merge"
        ]
        
        hooks_found = 0
        for variation in variations:
            variation_text = variation["text"].lower()
            if any(hook in variation_text for hook in business_hooks):
                hooks_found += 1
        
        print(f"✅ Variations with Business Couple Hooks: {hooks_found}/10")
        print(f"✅ All 10 Variations Generated: {'YES' if len(variations) == 10 else 'NO'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_10_variations_fixed()
