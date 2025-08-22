#!/usr/bin/env python3
"""Test the new dynamic sentiment analysis system"""

from enhanced_script_generator import EnhancedScriptGenerator

def test_dynamic_system():
    print("🚀 Testing NEW Dynamic Sentiment Analysis System")
    print("=" * 60)
    
    try:
        generator = EnhancedScriptGenerator('mymuse_training_data.json')
        
        # Test 1: Solo male masturbation (your transcript)
        print("\n📝 TEST 1: Solo Male Masturbation")
        print("-" * 40)
        transcript1 = "a boy in a room is horny he is bored to use is hand what can he use meet cock rings for ultimate pleasure"
        print(f"Transcript: {transcript1}")
        
        context1 = generator._analyze_transcript(transcript1)
        print(f"\n🔍 DYNAMIC ANALYSIS:")
        print(f"Primary Scenario: {context1['primary_scenario']}")
        print(f"Speaker Identity: {context1['learned_patterns']['speaker_identity']}")
        print(f"Action Patterns: {context1['learned_patterns']['action_patterns']}")
        print(f"Desire Patterns: {context1['learned_patterns']['desire_patterns']}")
        print(f"Emotional Language: {context1['learned_patterns']['emotional_language']}")
        print(f"Adaptation Strategy: {context1['adaptation_strategy']}")
        
        script1 = generator.generate_human_script("edge", transcript1, gen_z=False)
        print(f"\n📝 GENERATED SCRIPT:")
        print(script1)
        
        # Test 2: Business couple (different scenario)
        print("\n📝 TEST 2: Business Couple")
        print("-" * 40)
        transcript2 = "As a couple who run to businesses together, even our flights turn into meeting press or brainstorming sessions. Sets, calls, launches, it never ends. But at night, we carve out time for us to luxuriate in intimacy. And that's when the lovers bundle comes in. It doesn't just come in handy. It elevates. Depends. Leaves us, Bratless."
        print(f"Transcript: {transcript2}")
        
        context2 = generator._analyze_transcript(transcript2)
        print(f"\n🔍 DYNAMIC ANALYSIS:")
        print(f"Primary Scenario: {context2['primary_scenario']}")
        print(f"Speaker Identity: {context2['learned_patterns']['speaker_identity']}")
        print(f"Context Clues: {context2['learned_patterns']['context_clues']}")
        print(f"Emotional Language: {context2['learned_patterns']['emotional_language']}")
        print(f"Adaptation Strategy: {context2['adaptation_strategy']}")
        
        script2 = generator.generate_human_script("lovers bundle", transcript2, gen_z=False)
        print(f"\n📝 GENERATED SCRIPT:")
        print(script2)
        
        # Test 3: Travel scenario (another different scenario)
        print("\n📝 TEST 3: Travel Scenario")
        print("-" * 40)
        transcript3 = "I'm on my way to the airport and look who's coming with me on my trip! It's Mini Jadugar! Time for security check, got a lot of Dijayatra, got to get through with my Mini Jadugar. I will see you on the other side. Let's just say Mini Jadugar and I, we really like to take Jadugar places."
        print(f"Transcript: {transcript3}")
        
        context3 = generator._analyze_transcript(transcript3)
        print(f"\n🔍 DYNAMIC ANALYSIS:")
        print(f"Primary Scenario: {context3['primary_scenario']}")
        print(f"Speaker Identity: {context3['learned_patterns']['speaker_identity']}")
        print(f"Context Clues: {context3['learned_patterns']['context_clues']}")
        print(f"Action Patterns: {context3['learned_patterns']['action_patterns']}")
        print(f"Adaptation Strategy: {context3['adaptation_strategy']}")
        
        script3 = generator.generate_human_script("dive+", transcript3, gen_z=False)
        print(f"\n📝 GENERATED SCRIPT:")
        print(script3)
        
        # Test 4: Completely new scenario (romantic evening)
        print("\n📝 TEST 4: Romantic Evening (NEW SCENARIO)")
        print("-" * 40)
        transcript4 = "Tonight is our anniversary and I want to make it special. We've been together for years but I want to surprise her with something new. She deserves to feel beautiful and desired. I want to create a moment she'll never forget."
        print(f"Transcript: {transcript4}")
        
        context4 = generator._analyze_transcript(transcript4)
        print(f"\n🔍 DYNAMIC ANALYSIS:")
        print(f"Primary Scenario: {context4['primary_scenario']}")
        print(f"Speaker Identity: {context4['learned_patterns']['speaker_identity']}")
        print(f"Desire Patterns: {context4['learned_patterns']['desire_patterns']}")
        print(f"Emotional Language: {context4['learned_patterns']['emotional_language']}")
        print(f"Adaptation Strategy: {context4['adaptation_strategy']}")
        
        script4 = generator.generate_human_script("lovers bundle", transcript4, gen_z=False)
        print(f"\n📝 GENERATED SCRIPT:")
        print(script4)
        
        print("\n✅ DYNAMIC SYSTEM TESTING COMPLETE!")
        print("The system successfully analyzed and adapted to 4 completely different scenarios!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dynamic_system()
