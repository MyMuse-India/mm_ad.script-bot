#!/usr/bin/env python3
"""
Test script for anal_play detection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate import _detect_transcript_type

# Test transcript (the one that was failing)
transcript = """If you're planning a visit down the back door, you have got to be open to the possibility that you might encounter the thing that lives there. You are going down. It's home. It might be home. What are you going to do? As one of the world's great thinkers, Mantein once said, even kings and philosophers defecate and so do ladies."""

print("=== TESTING ANAL PLAY DETECTION ===")
print(f"Transcript: {transcript[:100]}...")
print(f"Type detected: {_detect_transcript_type(transcript)}")

if _detect_transcript_type(transcript) == "anal_play":
    print("✓ Anal play detected correctly!")
    print("✓ System should now generate appropriate content for this context")
else:
    print("✗ Anal play NOT detected - this is still the problem!")

print("\nTest completed!")
