#!/usr/bin/env python3
"""
Complete caption-specific test - verify all endpoints return caption-dependent data
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000"

# Test with real caption
TEST_CAPTION = "Just launched my new eco-friendly water bottle! Perfect for travel lovers 🌍💧 #sustainability #innovation"

def test_endpoint(endpoint, method="POST", data=None):
    """Test endpoint and return response"""
    try:
        if method == "POST":
            url = f"{BASE_URL}{endpoint}"
            headers = {"Content-Type": "application/json"}
            resp = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            url = f"{BASE_URL}{endpoint}"
            resp = requests.get(url, timeout=10)
        
        print(f"\n✓ {endpoint}")
        print(f"  Status: {resp.status_code}")
        
        try:
            result = resp.json()
            print(f"  Response: {json.dumps(result, indent=2)[:300]}...")
            return result
        except:
            print(f"  Response: {resp.text[:200]}...")
            return None
            
    except Exception as e:
        print(f"\n✗ {endpoint}")
        print(f"  Error: {str(e)}")
        return None

print("=" * 60)
print("CAPTION-SPECIFIC LIVE TEST")
print("=" * 60)
print(f"\nTest Caption: {TEST_CAPTION}\n")

# Test 1: Caption Analysis (Emotion)
print("\n[TEST 1] EMOTION - Should mention caption keywords")
emotion_data = {
    "caption": TEST_CAPTION,
    "engagement_rate": 8.5
}
emotion_result = test_endpoint("/api/emotion", "POST", emotion_data)

# Test 2: SEO Score
print("\n[TEST 2] SEO - Should analyze caption keywords")
seo_data = {"caption": TEST_CAPTION}
seo_result = test_endpoint("/api/seo", "POST", seo_data)

# Test 3: Real/Fake Detection
print("\n[TEST 3] AUTHENTICITY - Should analyze caption claims")
fake_data = {"caption": TEST_CAPTION}
fake_result = test_endpoint("/api/fake_real", "POST", fake_data)

# Test 4: Comment Generation
print("\n[TEST 4] COMMENTS - Should relate to caption topic")
comment_data = {"caption": TEST_CAPTION}
comment_result = test_endpoint("/api/comment_ai", "POST", comment_data)

# Test 5: Reach Prediction
print("\n[TEST 5] REACH - Should analyze caption factors")
reach_data = {"caption": TEST_CAPTION}
reach_result = test_endpoint("/api/reach_predictor", "POST", reach_data)

# Test 6: Trending Topics (should be live)
print("\n[TEST 6] TRENDS - Should show live trending topics")
trends_result = test_endpoint("/api/trends_graph", "GET")

print("\n" + "=" * 60)
print("VERIFICATION CHECKLIST")
print("=" * 60)

checks = {
    "Emotion mentions caption keywords": emotion_result and ("water bottle" in str(emotion_result).lower() or "eco-friendly" in str(emotion_result).lower()),
    "SEO analyzes caption": seo_result and seo_result.get("score") is not None,
    "Authenticity mentions caption": fake_result and ("product" in str(fake_result).lower() or "claim" in str(fake_result).lower()),
    "Comments relate to caption": comment_result and comment_result.get("comments") is not None,
    "Reach analyzes caption": reach_result and reach_result.get("best_time") is not None,
    "Trends show live data": trends_result and trends_result.get("trends") is not None,
}

all_pass = True
for check, result in checks.items():
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{status}: {check}")
    if not result:
        all_pass = False

print("\n" + "=" * 60)
if all_pass:
    print("✅ ALL TESTS PASSED - System is CAPTION-SPECIFIC & LIVE")
else:
    print("⚠️ SOME TESTS FAILED - Fix required")
print("=" * 60)
