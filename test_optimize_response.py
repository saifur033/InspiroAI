#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test optimize endpoint response structure"""

import requests
import json
import sys
import os

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:5000"

def test_optimize():
    """Test the optimize endpoint"""
    
    caption = "ঢাকা'য় আবারো ভূমিকম্প.!!"
    tone = "professional"
    
    print("\n" + "="*80)
    print("OPTIMIZE ENDPOINT TEST")
    print("="*80)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/process_caption",
            json={"caption": caption, "tone": tone},
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ Response Structure:")
            print(f"  • Optimized Caption: {data.get('optimized_caption', 'MISSING')[:50]}...")
            print(f"  • Original SEO: {data.get('original_seo_score', 'MISSING')}")
            print(f"  • Optimized SEO: {data.get('optimized_seo_score', 'MISSING')}")
            print(f"  • SEO Improvement: {data.get('seo_improvement', 'MISSING')}")
            print(f"  • Original Emotion: {data.get('original_emotion', 'MISSING')}")
            print(f"  • Optimized Emotion: {data.get('optimized_emotion', 'MISSING')}")
            print(f"  • Emotion Change: {data.get('emotion_change', 'MISSING')[:50]}...")
            print(f"  • Original Real%: {data.get('original_real_percent', 'MISSING')}")
            print(f"  • Original Fake%: {data.get('original_fake_percent', 'MISSING')}")
            print(f"  • Optimized Real%: {data.get('optimized_real_percent', 'MISSING')}")
            print(f"  • Optimized Fake%: {data.get('optimized_fake_percent', 'MISSING')}")
            print(f"  • Authenticity Change: {data.get('authenticity_change', 'MISSING')[:50]}...")
            print(f"  • Hashtags Count: {len(data.get('hashtags', []))}")
            print(f"  • Caption Styles: {len(data.get('caption_styles', {})) if isinstance(data.get('caption_styles'), dict) else 'N/A'} styles")
            
            # Check for any None or empty values
            print("\n🔍 Field Value Check:")
            for field in ['original_seo_score', 'optimized_seo_score', 'seo_improvement', 
                         'original_emotion', 'optimized_emotion', 'emotion_change',
                         'original_real_percent', 'optimized_real_percent',
                         'optimized_fake_percent', 'authenticity_change']:
                val = data.get(field)
                status = "✓" if val is not None and val != "" else "✗"
                print(f"  {status} {field}: {val}")
            
            print("\n" + "="*80)
            print("Full Response (JSON):")
            print("="*80)
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
        else:
            print(f"\n❌ Error Response:")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Exception: {str(e)}")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    test_optimize()
