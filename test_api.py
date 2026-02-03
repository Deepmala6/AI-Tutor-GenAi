#!/usr/bin/env python3
"""
Test the AI Tutor Generator API
Run this script to test the application without opening a browser
"""

import requests
import json
import time
from typing import Dict, Any

def test_api(grade: int, topic: str) -> None:
    """Test the API with a request."""
    
    print(f"\n{'='*60}")
    print(f"Testing: Grade {grade} - {topic}")
    print(f"{'='*60}\n")
    
    url = "http://localhost:5000/api/generate"
    payload = {
        "grade": grade,
        "topic": topic
    }
    
    print(f"📤 Sending request to: {url}")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}\n")
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=30)
        elapsed_time = time.time() - start_time
        
        print(f"⏱️  Response time: {elapsed_time:.2f}s\n")
        
        if response.status_code == 200:
            result = response.json()
            display_results(result)
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Flask server")
        print("   Make sure Flask is running: python app.py")
        return
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return

def display_results(result: Dict[str, Any]) -> None:
    """Display the results nicely."""
    
    print("\n" + "="*60)
    print("📝 GENERATED CONTENT")
    print("="*60)
    
    generated = result.get("generated_content", {})
    
    # Explanation
    explanation = generated.get("explanation", "No explanation")
    print(f"\n📖 Explanation:\n{explanation}\n")
    
    # MCQs
    mcqs = generated.get("mcqs", [])
    if mcqs:
        print("❓ Questions:\n")
        for i, mcq in enumerate(mcqs, 1):
            print(f"Q{i}: {mcq.get('question', 'No question')}")
            for j, option in enumerate(mcq.get('options', []), 1):
                marker = "✓" if option == mcq.get('answer') else " "
                print(f"   [{marker}] {option}")
            print()
    
    # Review Status
    print("\n" + "="*60)
    print("✓ REVIEW RESULTS")
    print("="*60)
    
    review_status = result.get("review_status", "unknown").upper()
    status_symbol = "✅" if review_status == "PASS" else "⚠️"
    
    print(f"\nStatus: {status_symbol} {review_status}")
    
    feedback = result.get("review_feedback", [])
    if feedback:
        print("\n📌 Feedback:")
        for item in feedback:
            print(f"   • {item}")
    else:
        print("\n📌 Feedback: No issues found! ✨")
    
    # Refinement
    if result.get("refinement_applied"):
        print("\n" + "="*60)
        print("🔄 REFINED CONTENT")
        print("="*60)
        
        refined = result.get("refined_content", {})
        explanation = refined.get("explanation", "No explanation")
        print(f"\n📖 Refined Explanation:\n{explanation}\n")
        
        mcqs = refined.get("mcqs", [])
        if mcqs:
            print("❓ Refined Questions:\n")
            for i, mcq in enumerate(mcqs, 1):
                print(f"Q{i}: {mcq.get('question', 'No question')}")
                for j, option in enumerate(mcq.get('options', []), 1):
                    marker = "✓" if option == mcq.get('answer') else " "
                    print(f"   [{marker}] {option}")
                print()

def test_health() -> bool:
    """Test if the server is healthy."""
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is healthy!")
            return True
    except:
        pass
    return False

def main():
    """Main test function."""
    
    print("\n" + "🎓 "*20)
    print("   AI TUTOR GENERATOR - API Test Script")
    print("🎓 "*20 + "\n")
    
    print("🔍 Checking server status...\n")
    
    if not test_health():
        print("\n❌ Server is not responding!")
        print("   Please start Flask: python app.py")
        return
    
    print("\n✅ Server is ready!\n")
    
    # Test cases
    test_cases = [
        (4, "Types of angles"),
        (6, "Photosynthesis"),
        (8, "Fractions"),
        (10, "Quadratic equations"),
    ]
    
    print("Starting API tests...\n")
    
    for grade, topic in test_cases:
        test_api(grade, topic)
        time.sleep(1)  # Small delay between requests
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
