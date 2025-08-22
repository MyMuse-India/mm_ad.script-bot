#!/usr/bin/env python3
"""Test all 10 variations for couple intimacy"""

from enhanced_script_generator import EnhancedScriptGenerator

def test_10_variations():
    print("🔟 Testing ALL 10 Variations for Couple Intimacy")
    print("=" * 60)
    
    # Your transcript
    transcript = "As a couple who run to businesses together, even our flights turn into meeting press or brainstorming sessions. Sets, calls, launches, it never ends. But at night, we carve out time for us to luxuriate in intimacy. And that's when the lovers bundle comes in. It doesn't just come in handy. It elevates. Depends. Leaves us, Bratless."
    
    print(f"📝 Transcript: {len(transcript.split())} words")
    print()
    
    try:
        generator = EnhancedScriptGenerator('mymuse_training_data.json')
        
        # Generate ALL 10 variations
        variations = generator.generate_variations("lovers bundle", transcript, count=10, gen_z=False)
        
        print(f"🎯 Generated {len(variations)} variations:")
        print()
        
        for i, variation in enumerate(variations, 1):
            words = len(variation["text"].split())
            print(f"🔄 Variation {i} ({words} words):")
            print(variation["text"])
            print("-" * 50)
        
        # Check uniqueness
        all_texts = [v["text"] for v in variations]
        unique_texts = set(all_texts)
        
        print(f"\n📊 Results:")
        print(f"Total variations: {len(variations)}")
        print(f"Unique variations: {len(unique_texts)}")
        print(f"All unique: {'✅' if len(unique_texts) == len(variations) else '❌'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_10_variations()
