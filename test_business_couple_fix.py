#!/usr/bin/env python3
"""Test the business couple scenario detection fix"""

from enhanced_script_generator import EnhancedScriptGenerator

def test_business_couple_fix():
    print("🔧 Testing Business Couple Scenario Detection Fix")
    print("=" * 60)
    
    try:
        generator = EnhancedScriptGenerator('mymuse_training_data.json')
        
        # Your business couple transcript
        transcript = "As a couple who run to businesses together, even our flights turn into meeting press or brainstorming sessions. Sets, calls, launches, it never ends. But at night, we carve out time for us to luxuriate in intimacy. And that's when the lovers bundle comes in. It doesn't just come in handy. It elevates. Depends. Leaves us, Bratless."
        
        print(f"📝 Transcript: {transcript}")
        print()
        
        # Analyze transcript
        context = generator._analyze_transcript(transcript)
        print(f"🔍 SCENARIO DETECTION:")
        print(f"Primary Scenario: {context['primary_scenario']}")
        print(f"Speaker Identity: {context['learned_patterns']['speaker_identity']}")
        print(f"Context Clues: {context['learned_patterns']['context_clues']}")
        print(f"Adaptation Strategy: {context['adaptation_strategy']}")
        print()
        
        # Generate script
        script = generator.generate_human_script("lovers bundle", transcript, gen_z=False)
        print(f"📝 GENERATED SCRIPT:")
        print(script)
        print()
        
        # Generate variations
        variations = generator.generate_variations("lovers bundle", transcript, count=3, gen_z=False)
        print(f"🔄 VARIATIONS (3):")
        for i, variation in enumerate(variations, 1):
            print(f"Variation {i}:")
            print(variation["text"])
            print()
        
        print("✅ Business couple scenario detection and routing should now work correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_business_couple_fix()
