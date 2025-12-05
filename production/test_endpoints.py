#!/usr/bin/env python
"""
Test script for new Flask API endpoints
"""
import json
import requests
import sys

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_analyze_caption():
    """Test new analyze_caption endpoint"""
    print("\n🔍 Testing /api/analyze_caption endpoint...")
    
    test_cases = [
        {
            "name": "Real Caption",
            "caption": "Just had the most amazing coffee at my favorite cafe this morning! The atmosphere is so peaceful and the barista remembered my usual order. Sometimes the simple moments are the best ones. ☕😊"
        },
        {
            "name": "Fake Caption",
            "caption": "🚨 LIMITED TIME OFFER! 🚨 Click here NOW to get 90% OFF on premium products! Don't miss out! Act now!!! Link in bio! www.spamsite.com"
        },
        {
            "name": "Spam Caption",
            "caption": "CHECK THIS OUT! Free money waiting for you! Visit http://sketchy-link.com RIGHT NOW! Limited offer!!! 💰💰💰"
        }
    ]
    
    for test in test_cases:
        print(f"\n  Testing: {test['name']}")
        print(f"  Caption: {test['caption'][:60]}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/analyze_caption",
                json={"caption": test['caption']},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Status: {response.status_code}")
                print(f"     Emotion: {data['emotion']['dominant']} ({data['emotion']['scores'][data['emotion']['dominant']]:.0f}%)")
                print(f"     Auth: {data['authenticity']['label']} (Real:{data['authenticity']['real']}%, Fake:{data['authenticity']['fake']}%, Spam:{data['authenticity']['spam']}%)")
                if data['optimized_real_caption']:
                    print(f"     Suggested: {data['optimized_real_caption'][:60]}...")
            else:
                print(f"  ❌ Status: {response.status_code}")
                print(f"     Error: {response.json()}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

def test_recheck_caption():
    """Test new recheck_caption endpoint"""
    print("\n🔍 Testing /api/recheck_caption endpoint...")
    
    test_caption = "I discovered something interesting today. Would love to hear what you think about it!"
    
    print(f"  Caption: {test_caption}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/recheck_caption",
            json={"caption": test_caption},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Status: {response.status_code}")
            print(f"     Label: {data['authenticity']['label']}")
            print(f"     Real: {data['authenticity']['real']}%")
            print(f"     Fake: {data['authenticity']['fake']}%")
            print(f"     Spam: {data['authenticity']['spam']}%")
            print(f"     Reason: {data['authenticity']['reason']}")
        else:
            print(f"  ❌ Status: {response.status_code}")
            print(f"     Error: {response.json()}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def main():
    print("=" * 60)
    print("InspiroAI Flask API Tests")
    print("=" * 60)
    print(f"Testing endpoints at: {BASE_URL}")
    print("\nMake sure the Flask server is running:")
    print("  python api_server.py")
    
    print("\n" + "-" * 60)
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except:
        print("\n❌ Server is not running!")
        print("Start it with: python api_server.py")
        return
    
    print("\n✅ Server is running!")
    
    # Run tests
    test_health()
    test_analyze_caption()
    test_recheck_caption()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
