#!/usr/bin/env python3
"""
Test script for Case 2 enforcement
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate import _enforce_case2_structure, _detect_transcript_type

def test_case2():
    # Test transcript
    transcript = """I am on my way to the airport, and look who's coming with me on my trip. It's Mini Jadugar, with 18 speed modes and only 11 inches. Time for security check. Gotta love digi-atra.
Gotta get through with my Mini Jadugar, that comes in black and red color. I will see you on the other side. Everything's all good in here. Full splurge. Let's just say Mini Jadugar and I, we really like to take each other places"""
    
    product_name = "Dive+"
    
    print("=== TESTING CASE 2 ENFORCEMENT ===")
    print(f"Transcript type: {_detect_transcript_type(transcript)}")
    print(f"Product: {product_name}")
    print("\nOriginal transcript:")
    print(transcript)
    
    print("\n" + "="*50)
    
    # Test the enforcement function
    result = _enforce_case2_structure("", transcript, product_name)
    
    print("\nEnforced output:")
    print(result)
    
    print("\n" + "="*50)
    print("Test completed!")

if __name__ == "__main__":
    test_case2()
