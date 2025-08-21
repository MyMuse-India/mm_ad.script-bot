#!/usr/bin/env python3
"""
Test script for the updated variations generation system.
"""

from generate import generate_variations
from analysis import analyze_agent

def test_variations():
    """Test the variations generation with the airport transcript using Groove+."""
    
    # The original transcript
    transcript = """I am on my way to the airport and look who's coming with me on my trip. It's Mini-Jadukar. Time for security check. Got a love Digi-Astra. Got to get through with my Mini-Jadukar. I will see you on the other side. Let's just say Mini-Jadukar and I, we really like to take each other places."""
    
    print("Testing Variations Generation System with GROOVE+")
    print("=" * 50)
    print(f"Original transcript: {transcript}")
    print("\n" + "=" * 50)
    
    try:
        # Analyze the transcript
        print("1. Analyzing transcript...")
        analysis = analyze_agent(transcript)
        print(f"   Analysis completed. Transcript type: {analysis.get('transcript_type', 'unknown')}")
        
        # Generate variations with GROOVE+ (not dive+)
        print("\n2. Generating variations with GROOVE+...")
        result = generate_variations('groove+', transcript, analysis)
        
        variations = result.get('variations', [])
        print(f"   Generated {len(variations)} variations")
        
        # Show each variation
        print("\n3. Generated Variations:")
        print("-" * 50)
        
        for i, variation in enumerate(variations, 1):
            text = variation.get('text', 'No text')
            evaluation = variation.get('evaluation', {})
            
            print(f"\nVariation {i}:")
            print(f"Text: {text[:200]}{'...' if len(text) > 200 else ''}")
            print(f"Passes evaluation: {evaluation.get('pass', 'Unknown')}")
            
            if 'scores' in evaluation:
                scores = evaluation['scores']
                print(f"  - Cosine similarity: {scores.get('cosine', 'N/A')}")
                print(f"  - 4-gram overlap: {scores.get('overlap4', 'N/A')}")
                print(f"  - BLEU score: {scores.get('bleu', 'N/A')}")
            
            if 'reasons' in evaluation and evaluation['reasons']:
                print(f"  - Issues: {', '.join(evaluation['reasons'])}")
        
        print(f"\n4. Summary: {result.get('summary', 'No summary')}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_variations()
