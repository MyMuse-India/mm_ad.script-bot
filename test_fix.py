#!/usr/bin/env python3
"""
Quick test for Case 2 fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate import _detect_transcript_type, _enforce_case2_structure

# Test transcript
transcript = """I'm on my way to the airport and look who's coming with me on my trip! It's Mini Jadugar! Time for security check, got a lot of Dijayatra, got to get through with my Mini Jadugar. I will see you on the other side. Let's just say Mini Jadugar and I, we really like to take Jadugar places."""

print("=== TESTING CASE 2 FIX ===")
print(f"Transcript: {transcript}")
print(f"Type detected: {_detect_transcript_type(transcript)}")

if _detect_transcript_type(transcript) == "feature_heavy":
    print("✓ Case 2 detected correctly")
    result = _enforce_case2_structure("", transcript, "Dive+")
    print(f"\nEnforced output:\n{result}")
    
    # Check word count per line
    lines = result.split('\n')
    print(f"\nLine analysis:")
    for i, line in enumerate(lines, 1):
        words = line.split()
        print(f"Line {i}: {len(words)} words")
else:
    print("✗ Case 2 NOT detected - this is the problem!")

print("\nTest completed!")
