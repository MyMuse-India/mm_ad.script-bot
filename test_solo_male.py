#!/usr/bin/env python3
"""Test solo male masturbation script generation with edge product"""

from enhanced_script_generator import EnhancedScriptGenerator

def test_solo_male():
    print("🔥 Testing Solo Male Masturbation Script Generation")
    print("=" * 60)
    
    try:
        generator = EnhancedScriptGenerator('mymuse_training_data.json')
        
        # Your solo male transcript
        transcript = "im horny and a boy i dont want to use my hands"
        
        print(f"📝 Transcript: {transcript}")
        print()
        
        # Analyze transcript
        context = generator._analyze_transcript(transcript)
        print(f"🔍 SCENARIO DETECTION:")
        print(f"Primary Scenario: {context['primary_scenario']}")
        print(f"Speaker Identity: {context['learned_patterns']['speaker_identity']}")
        print(f"Action Patterns: {context['learned_patterns']['action_patterns']}")
        print(f"Desire Patterns: {context['learned_patterns']['desire_patterns']}")
        print(f"Emotional Language: {context['learned_patterns']['emotional_language']}")
        print(f"Adaptation Strategy: {context['adaptation_strategy']}")
        print()
        
        # Generate script
        script = generator.generate_human_script("edge", transcript, gen_z=False)
        print(f"📝 GENERATED SCRIPT:")
        print(script)
        print()
        
        # Generate variations
        variations = generator.generate_variations("edge", transcript, count=10, gen_z=False)
        print(f"🔄 VARIATIONS (10):")
        for i, variation in enumerate(variations, 1):
            print(f"Variation {i}")
            print(variation["text"])
            print()
        
        print("✅ Solo male masturbation script generation complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_solo_male()
