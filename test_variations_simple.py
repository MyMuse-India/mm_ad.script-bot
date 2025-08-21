#!/usr/bin/env python3
"""
Simple test for generate_variations function
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate import generate_variations

# Test data
product_name = "Dive+"
transcript_text = "I'm on my way to the airport and look who's coming with me on my trip! It's Mini Jadugar! Time for security check, got a lot of Dijayatra, got to get through with my Mini Jadugar. I will see you on the other side. Let's just say Mini Jadugar and I, we really like to take Jadugar places."

analysis = {
    "sentiment": {"compound": 0.5, "pos": 0.8, "neg": 0.1, "neu": 0.1},
    "keywords": ["airport", "trip", "security", "travel"],
    "themes": ["travel", "adventure"],
    "hook": "airport travel",
    "style_tags": ["energetic", "playful"],
    "structure": {"hook": ["airport"], "proof": ["security"]},
    "tone": "positive"
}

print("=== TESTING generate_variations ===")
print(f"Product: {product_name}")
print(f"Transcript: {transcript_text[:100]}...")
print(f"Analysis keys: {list(analysis.keys())}")

try:
    result = generate_variations(
        product_name=product_name,
        transcript_text=transcript_text,
        analysis=analysis,
        rel_reviews=[],
        instagram_mode=True
    )
    
    print(f"\n✓ SUCCESS!")
    print(f"Result keys: {list(result.keys())}")
    print(f"Variations count: {len(result.get('variations', []))}")
    print(f"Summary: {result.get('summary', 'No summary')}")
    
    if result.get('variations'):
        print(f"\nFirst variation:")
        print(result['variations'][0].get('text', 'No text'))
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed!")
