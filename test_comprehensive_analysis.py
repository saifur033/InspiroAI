#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Comprehensive Caption Analysis Engine
Verify structured NLP analysis output
"""

import sys
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

from src.comprehensive_analysis import comprehensive_caption_analysis, format_comprehensive_output

# Test Cases
test_captions = [
    {
        "caption": "আমরা ঢাকায় ভূমিকম্প অনুভব করেছি। সবাই সাবধান থাকুন! 🚨",
        "tone": "breaking_news",
        "description": "Bangla Alert/Breaking News"
    },
    {
        "caption": "I absolutely love this amazing product! 😍💯 Best purchase ever! #blessed",
        "tone": "emotional",
        "description": "English Positive/Emotional"
    },
    {
        "caption": "আজকের দিনটি সত্যিই অসাধারণ ছিল। আমরা অনেক কিছু শিখেছি এবং আরও এগিয়ে যাওয়ার জন্য প্রস্তুত।",
        "tone": "professional",
        "description": "Bangla Professional"
    },
    {
        "caption": "Just found the craziest hack that'll change your life! MUST READ! 🔥🔥🔥",
        "tone": "viral",
        "description": "English Viral/Clickbait"
    },
    {
        "caption": "খুশি হয়ে জানাচ্ছি যে আমি এই প্রজেক্টে যোগদান করছি। এটি আমার জীবনের সেরা সিদ্ধান্ত।",
        "tone": "friendly",
        "description": "Bangla Friendly/Positive"
    }
]

print("\n" + "=" * 80)
print("🧠 COMPREHENSIVE CAPTION ANALYSIS ENGINE TEST")
print("=" * 80)

for i, test in enumerate(test_captions, 1):
    print(f"\n\n{'#' * 80}")
    print(f"TEST {i}: {test['description']}")
    print(f"Tone: {test['tone']}")
    print(f"{'#' * 80}")
    
    # Run analysis
    result = comprehensive_caption_analysis(test['caption'], test['tone'])
    
    # Display formatted output
    formatted = format_comprehensive_output(result)
    print(formatted)
    
    # Also show raw JSON for verification
    if result.get("success"):
        print("\n📋 ANALYSIS SUMMARY:")
        a = result.get("analysis", {})
        print(f"  • SEO Score: {a.get('seo', {}).get('score')}/100")
        print(f"  • Emotion: {a.get('emotion', {}).get('type')} ({a.get('emotion', {}).get('confidence_percent')}%)")
        print(f"  • Real%: {a.get('authenticity', {}).get('real_percent')}%")
        print(f"  • Hashtags Generated: {len(a.get('hashtags', []))} tags")
        print(f"  • Rewrite Categories: {len(a.get('rewrites', {}))} types with 3 captions each")

print("\n" + "=" * 80)
print("✅ ALL TESTS COMPLETED")
print("=" * 80 + "\n")
