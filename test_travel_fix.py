#!/usr/bin/env python3
"""Test the travel transcript analysis fix"""

from enhanced_script_generator import EnhancedScriptGenerator

def test_travel_fix():
    print("✈️ Testing Travel Transcript Analysis Fix")
    print("=" * 60)
    
    # Your travel transcript
    transcript = "I'm on my way to the airport and look who's coming with me on my trip! It's Mini Jadugar! Time for security check, got a lot of Dijayatra, got to get through with my Mini Jadugar. I will see you on the other side. Let's just say Mini Jadugar and I, we really like to take Jadugar places."
    
    print(f"📝 Transcript: {len(transcript.split())} words")
    print(transcript)
    print()
    
    try:
        generator = EnhancedScriptGenerator('mymuse_training_data.json')
        
        # Analyze transcript
        context = generator._analyze_transcript(transcript)
        print("🔍 Analysis Results:")
        print(f"Primary Scenario: {context['primary_scenario']}")
        print(f"Detected Scenarios: {context['scenarios']}")
        print(f"Primary Emotion: {context['primary_emotion']}")
        print(f"Sentiment Score: {context['sentiment_score']}")
        print()
        
        # Generate script
        script = generator.generate_human_script("dive+", transcript, gen_z=False)
        print("📝 Generated Script:")
        print(script)
        print(f"Lines: {len(script.split(chr(10)))}")
        print(f"Words: {len(script.split())}")
        print()
        
        # Generate 3 variations
        variations = generator.generate_variations("dive+", transcript, count=3, gen_z=False)
        print("🔄 Variations (3):")
        for i, variation in enumerate(variations, 1):
            print(f"Variation {i}:")
            print(variation["text"])
            print(f"Lines: {len(variation['text'].split(chr(10)))}")
            print(f"Words: {len(variation['text'].split())}")
            print("-" * 50)
        
        # Check if it's actually travel-focused
        is_travel = "airport" in script.lower() or "security" in script.lower() or "travel" in script.lower()
        print(f"✅ Travel-focused: {'YES' if is_travel else 'NO'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_travel_fix()
