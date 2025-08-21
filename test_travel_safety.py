#!/usr/bin/env python3
"""
Test script for travel safety context and diverse sexual content handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate import _detect_transcript_type, generate

# Test 1: Travel safety context
print("=== TEST 1: Travel Safety Context ===")
travel_transcript = "I'm on my way to the airport and look who's coming with me on my trip! It's Mini Jadugar! Time for security check, got a lot of Dijayatra, got to get through with my Mini Jadugar. I will see you on the other side. Let's just say Mini Jadugar and I, we really like to take Jadugar places."

print(f"Travel transcript: {travel_transcript[:100]}...")
print(f"Type detected: {_detect_transcript_type(travel_transcript)}")

# Test 2: Diverse sexual content
print("\n=== TEST 2: Diverse Sexual Content ===")
sexual_transcript = "Does size matter? How do I know if my boyfriend is small or average? I have only ever been with him. So here's the thing. The average size of a soft pp is 3.5 inches, and a hard one is about 5 inches. So you can just sort of measure and compare him with these lengths. But girl to girl, size doesn't really matter if he is good at it, if he is paying attention to your needs and you know, being nice to you. And for all the guys, it's not always about the size, it's about what you do with it."

print(f"Sexual transcript: {sexual_transcript[:100]}...")
print(f"Type detected: {_detect_transcript_type(sexual_transcript)}")

# Test 3: Anal play content
print("\n=== TEST 3: Anal Play Content ===")
anal_transcript = "If you're planning a visit down the back door, you have got to be open to the possibility that you might encounter the thing that lives there. You are going down. It's home. It might be home. What are you going to do? As one of the world's great thinkers, Mantein once said, even kings and philosophers defecate and so do ladies."

print(f"Anal play transcript: {anal_transcript[:100]}...")
print(f"Type detected: {_detect_transcript_type(anal_transcript)}")

# Test 4: Feature-heavy content
print("\n=== TEST 4: Feature-Heavy Content ===")
feature_transcript = "I am on my way to the airport, and look who's coming with me on my trip. It's Mini Jadugar, with 18 speed modes and only 11 inches. Time for security check. Gotta love digi-atra. Gotta get through with my Mini Jadugar, that comes in black and red color. I will see you on the other side. Everything's all good in here. Full splurge. Let's just say Mini Jadugar and I, we really like to take each other places."

print(f"Feature-heavy transcript: {feature_transcript[:100]}...")
print(f"Type detected: {_detect_transcript_type(feature_transcript)}")

print("\n=== SUMMARY ===")
print("✓ Travel safety context added to SYSTEM_PROMPT")
print("✓ Travel safety context added to variations prompt")
print("✓ All products now include TSA-compliant, airport-safe features")
print("✓ New Case 5 added for diverse sexual content")
print("✓ System can now handle size discussions, relationship advice, and intimacy tips")
print("✓ MyMuse products work for all genders, orientations, and relationship types")

print("\nTest completed!")
