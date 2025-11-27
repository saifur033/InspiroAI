#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5000"

# Test caption
test_caption = "Just launched my new eco-friendly water bottle! Perfect for travel lovers 🌍💧 #sustainability #innovation"

print("=" * 80)
print("TEST 1: OPTIMIZE Caption")
print("=" * 80)

payload = {
    "caption": test_caption,
    "tone": "professional"
}

response = requests.post(f"{BASE_URL}/api/process_caption", json=payload)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ OPTIMIZED CAPTION:\n{data.get('optimized_caption', 'N/A')}")
    print(f"\n📊 METRICS:")
    print(f"  • Original SEO: {data.get('original_seo_score', 'N/A')}/100")
    print(f"  • Optimized SEO: {data.get('optimized_seo_score', 'N/A')}/100")
    print(f"  • Improvement: +{data.get('seo_improvement', 0)}")
    print(f"\n😊 EMOTION:")
    print(f"  • Original: {data.get('original_emotion', 'N/A')}")
    print(f"  • Optimized: {data.get('optimized_emotion', 'N/A')}")
    print(f"  • Change: {data.get('emotion_change', 'N/A')}")
    print(f"\n✔️ AUTHENTICITY:")
    print(f"  • Original Real: {data.get('original_real_percent', 'N/A')}% | Fake: {data.get('original_fake_percent', 'N/A')}%")
    print(f"  • Optimized Real: {data.get('optimized_real_percent', 'N/A')}% | Fake: {data.get('optimized_fake_percent', 'N/A')}%")
    print(f"  • Change: {data.get('authenticity_change', 'N/A')}")
    print(f"\n#️⃣ HASHTAGS: {len(data.get('hashtags', []))} tags")
    print(f"  {', '.join(data.get('hashtags', [])[:5])}...")
    print(f"\n📱 FACEBOOK READY:\n{data.get('ready_for_facebook', 'N/A')}")
    print(f"\n💡 User caption used? {data.get('user_caption_used', 'N/A')}")
else:
    print(f"❌ Error: {response.text}")

print("\n" + "=" * 80)
print("TEST 2: ANALYZE Caption (No tone)")
print("=" * 80)

payload = {
    "caption": test_caption
}

response = requests.post(f"{BASE_URL}/api/process_caption", json=payload)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"  • SEO Score: {data.get('seo_score', 'N/A')}/100 ({data.get('seo_grade', 'N/A')})")
    print(f"  • Emotion: {data.get('emotion', 'N/A')} ({data.get('emotion_confidence', 'N/A')}%)")
    print(f"  • Emotion Details: {data.get('emotion_details', 'N/A')}")
    print(f"  • Authenticity: {data.get('real_percent', 'N/A')}% real | {data.get('fake_percent', 'N/A')}% fake")
    print(f"  • Details: {data.get('fake_real_details', 'N/A')}")
else:
    print(f"❌ Error: {response.text}")

print("\n" + "=" * 80)
print("✅ Tests Complete!")
print("=" * 80)
