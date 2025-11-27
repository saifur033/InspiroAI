#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test caption variations endpoint"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_caption_variations():
    """Test the /api/caption_variations endpoint"""
    
    # Test caption from user example
    caption_bangla = "ঢাকা'য় আবারো ভূমিকম্প.!!"
    
    test_cases = [
        ("professional", caption_bangla),
        ("friendly", caption_bangla),
        ("emotional", caption_bangla),
        ("trendy", caption_bangla),
        ("funny", caption_bangla),
    ]
    
    print("\n" + "="*70)
    print("CAPTION VARIATIONS TEST")
    print("="*70)
    
    for tone, caption in test_cases:
        print(f"\n📝 Testing tone: {tone.upper()}")
        print(f"Caption: {caption}")
        print("-" * 70)
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/caption_variations",
                json={"caption": caption, "tone": tone},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Status: {response.status_code}")
                print(f"✓ Total variations: {data.get('total_variations', 0)}")
                
                variations = data.get('variations', [])
                for i, variation in enumerate(variations, 1):
                    print(f"\n  Variation {i}:")
                    print(f"    Caption: {variation['caption'][:80]}...")
                    print(f"    SEO Score: {variation['seo_score']}/100")
                    print(f"    Emotion: {variation['emotion']} ({variation['emotion_confidence']}%)")
                    
            else:
                print(f"✗ Status: {response.status_code}")
                print(f"✗ Error: {response.json()}")
                
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_caption_variations()
