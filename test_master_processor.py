#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Master Caption Processor
Tests both English and Bangla captions
"""

import requests
import json
import time

def test_master_processor():
    """Test the master caption processor endpoint"""
    
    # Test 1: English Caption
    print("\n" + "="*70)
    print("TEST 1: ENGLISH CAPTION")
    print("="*70)
    
    english_caption = "Just finished an amazing project! So proud of what our team accomplished together. Hard work and dedication really do pay off!"
    
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/process_caption_master",
            json={"caption": english_caption},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result.get("data", {})
            
            print("\n[SUCCESS] Response received")
            print(f"Language: {data.get('language')}")
            
            # Analysis section
            analysis = data.get("analysis", {})
            print(f"\n[ANALYSIS]")
            print(f"  SEO Score: {analysis.get('seo_score')}/100")
            print(f"  Emotion: {analysis.get('emotion')}")
            print(f"  Authenticity: {analysis.get('authenticity', {}).get('real_percent')}% Real, {analysis.get('authenticity', {}).get('ai_like_percent')}% AI-Like")
            
            # Optimized captions
            opt = data.get("optimized_captions", {})
            print(f"\n[OPTIMIZED CAPTIONS]")
            print(f"  Version A (Professional):\n    {opt.get('version_a_professional', 'N/A')[:80]}...")
            print(f"\n  Version B (Social Friendly):\n    {opt.get('version_b_social_friendly', 'N/A')[:80]}...")
            
            # Hashtags
            hashtags = data.get('hashtags', [])
            print(f"\n[HASHTAGS]")
            print(f"  Count: {len(hashtags)}")
            print(f"  Sample: {' '.join(hashtags[:5])}")
            
            # Reach insights
            reach = data.get('reach_insights', {})
            print(f"\n[REACH INSIGHTS]")
            for key, value in list(reach.items())[:4]:
                print(f"  {key}: {value}")
            
        else:
            print(f"[ERROR] Status {response.status_code}")
            print(f"Response: {response.text[:300]}")
            
    except Exception as e:
        print(f"[EXCEPTION] {str(e)}")
    
    # Test 2: Bangla Caption (with ideas)
    print("\n" + "="*70)
    print("TEST 2: BANGLA CAPTION WITH IDEAS")
    print("="*70)
    
    bangla_caption = "নতুন প্রোডাক্ট লঞ্চ করতে যাচ্ছি। অনেক কঠোর পরিশ্রম করেছি এই প্রজেক্টে। সবাই সাপোর্ট দিয়েছে।"
    
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/process_caption_master",
            json={
                "caption": bangla_caption,
                "generate_ideas": True,
                "topic_for_ideas": "নতুন পণ্য লঞ্চ"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            data = result.get("data", {})
            
            print("\n[SUCCESS] Response received")
            print(f"Language: {data.get('language')}")
            
            # Analysis section
            analysis = data.get("analysis", {})
            print(f"\n[ANALYSIS]")
            print(f"  SEO Score: {analysis.get('seo_score')}/100")
            print(f"  Emotion: {analysis.get('emotion')}")
            
            # Hashtags
            hashtags = data.get('hashtags', [])
            print(f"\n[HASHTAGS]")
            print(f"  Count: {len(hashtags)}")
            
            # Ideas (if generated)
            if "caption_ideas" in data:
                ideas = data.get("caption_ideas", {})
                print(f"\n[CAPTION IDEAS]")
                print(f"  Short captions: {len(ideas.get('short_captions', []))}")
                print(f"  Emotional captions: {len(ideas.get('emotional_alert_captions', []))}")
            
        else:
            print(f"[ERROR] Status {response.status_code}")
            print(f"Response: {response.text[:300]}")
            
    except Exception as e:
        print(f"[EXCEPTION] {str(e)}")
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_master_processor()
