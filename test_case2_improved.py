#!/usr/bin/env python3
"""
Test script for improved Case 2 enforcement
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate import _enforce_case2_structure, _detect_transcript_type

def test_improved_case2():
    print("=== TESTING IMPROVED CASE 2 ENFORCEMENT ===")
    
    # Test transcript (your exact transcript)
    transcript = """I'm on my way to the airport and look who's coming with me on my trip! It's Mini Jadugar! Time for security check, got a lot of Dijayatra, got to get through with my Mini Jadugar. I will see you on the other side. Let's just say Mini Jadugar and I, we really like to take Jadugar places."""
    
    product_name = "Dive+"
    
    print(f"Transcript: {transcript}")
    print(f"Product: {product_name}")
    print(f"Transcript type: {_detect_transcript_type(transcript)}")
    
    print("\n" + "="*50)
    
    # Test the improved enforcement function
    result = _enforce_case2_structure("", transcript, product_name)
    
    print("\nImproved Case 2 output:")
    print(result)
    
    print("\n" + "="*50)
    
    # Analyze the output
    lines = result.split('\n')
    print(f"Number of lines: {len(lines)}")
    
    for i, line in enumerate(lines, 1):
        words = line.split()
        print(f"Line {i}: {len(words)} words - {line}")
    
    print("\n" + "="*50)
    print("Test completed!")

if __name__ == "__main__":
    test_improved_case2()
