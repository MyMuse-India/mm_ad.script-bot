#!/usr/bin/env python3
"""
Test script for UGC Evaluator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evaluator import UGCScriptEvaluator

def test_evaluator():
    print("=== TESTING UGC EVALUATOR ===")
    
    evaluator = UGCScriptEvaluator()
    
    # Test Case 2 transcript
    transcript = """I am on my way to the airport, and look who's coming with me on my trip. It's Mini Jadugar, with 18 speed modes and only 11 inches. Time for security check. Gotta love digi-atra.
Gotta get through with my Mini Jadugar, that comes in black and red color. I will see you on the other side. Everything's all good in here. Full splurge. Let's just say Mini Jadugar and I, we really like to take each other places"""
    
    # Generated script (Case 2)
    script = """ACTOR/MODEL: I'm on my way to the airport, and guess who's coming along on my flight!
ACTOR/MODEL: It's my Dive+ with 10+ vibration modes and compact design.
ACTOR/MODEL: Time for security check - but no worries, it's discreet and portable.
ACTOR/MODEL: Everything's smooth sailing from here.
ACTOR/MODEL: Let's just say Dive+ and I love taking each other places.
ACTOR/MODEL: Tap to shop MyMuse Dive+."""
    
    print(f"Transcript: {transcript[:100]}...")
    print(f"Generated Script: {script}")
    print(f"Product: Dive+")
    print(f"Case Type: feature_heavy")
    
    print("\n" + "="*50)
    
    # Test evaluation
    result = evaluator.evaluate_script(
        transcript=transcript,
        product_name="Dive+",
        generated_script=script,
        channel="Reels/TikTok",
        case_type="feature_heavy",
        true_features=["10+ vibration modes", "compact design", "discreet", "portable"]
    )
    
    print(f"Total Score: {result.total_score}/100")
    print(f"Pass: {result.pass_status}")
    print(f"Human Talk Score: {result.humantalk_score:.2f}/1.00")
    
    print("\nScores Breakdown:")
    for category, score in result.scores.items():
        print(f"  {category.replace('_', ' ').title()}: {score}")
    
    print(f"\nFlags: {result.flags}")
    
    if result.notes:
        print(f"\nNotes:")
        for note in result.notes:
            print(f"  ✓ {note}")
    
    if result.fixes:
        print(f"\nFixes:")
        for fix in result.fixes:
            print(f"  → {fix}")
    
    if result.suggested_rewrite:
        print(f"\nSuggested Rewrite:")
        print(result.suggested_rewrite)
    
    print("\n" + "="*50)
    print("Test completed!")

if __name__ == "__main__":
    test_evaluator()
