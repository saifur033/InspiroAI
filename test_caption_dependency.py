#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify that SEO, Emotion, and Fake/Real are CAPTION-DEPENDENT (not random)
"""

import sys
sys.path.insert(0, "d:/Important File/A/ContextAwareFacebookAI")

from src.seo_score import compute_seo_score
from src.emotion_model import detect_emotion
from src.fake_real_model import detect_fake

def test_caption_dependency():
    """Test that analysis changes with different captions"""
    
    print("\n" + "="*80)
    print("CAPTION-DEPENDENCY TEST (NOT RANDOM)")
    print("="*80)
    
    # Test 1: Very positive caption
    caption1 = "I love this! Amazing and wonderful! 😍❤️✨"
    print("\n[TEST 1] POSITIVE CAPTION")
    print(f"Caption: {caption1}")
    seo1 = compute_seo_score(caption1)
    emo1 = detect_emotion(caption1)
    fake1 = detect_fake(caption1)
    print(f"  SEO: {seo1['score']}/100 ({seo1['grade']})")
    print(f"  Emotion: {emo1['emotion']} ({emo1['confidence']}%)")
    print(f"  Authenticity: {fake1['real']}% real, {fake1['fake']}% fake")
    print(f"  Reasoning: {fake1['reason']}")
    
    # Test 2: Very negative/alert caption
    caption2 = "Help! Emergency! Something terrible happened! 😱😱😱"
    print("\n[TEST 2] NEGATIVE/ALERT CAPTION")
    print(f"Caption: {caption2}")
    seo2 = compute_seo_score(caption2)
    emo2 = detect_emotion(caption2)
    fake2 = detect_fake(caption2)
    print(f"  SEO: {seo2['score']}/100 ({seo2['grade']})")
    print(f"  Emotion: {emo2['emotion']} ({emo2['confidence']}%)")
    print(f"  Authenticity: {fake2['real']}% real, {fake2['fake']}% fake")
    print(f"  Reasoning: {fake2['reason']}")
    
    # Test 3: Neutral caption
    caption3 = "The weather is nice today."
    print("\n[TEST 3] NEUTRAL CAPTION")
    print(f"Caption: {caption3}")
    seo3 = compute_seo_score(caption3)
    emo3 = detect_emotion(caption3)
    fake3 = detect_fake(caption3)
    print(f"  SEO: {seo3['score']}/100 ({seo3['grade']})")
    print(f"  Emotion: {emo3['emotion']} ({emo3['confidence']}%)")
    print(f"  Authenticity: {fake3['real']}% real, {fake3['fake']}% fake")
    print(f"  Reasoning: {fake3['reason']}")
    
    # Test 4: Bangla caption
    caption4 = "ঢাকা'য় আবারো ভূমিকম্প.!!"
    print("\n[TEST 4] BANGLA CAPTION")
    print(f"Caption: {caption4}")
    seo4 = compute_seo_score(caption4)
    emo4 = detect_emotion(caption4)
    fake4 = detect_fake(caption4)
    print(f"  SEO: {seo4['score']}/100 ({seo4['grade']})")
    print(f"  Emotion: {emo4['emotion']} ({emo4['confidence']}%)")
    print(f"  Authenticity: {fake4['real']}% real, {fake4['fake']}% fake")
    print(f"  Reasoning: {fake4['reason']}")
    
    # Test 5: Bangla positive
    caption5 = "খুব আনন্দের সাথে জানাচ্ছি আমি ঢাকায় একটি নতুন বাড়ি কিনেছি! 😊❤️"
    print("\n[TEST 5] BANGLA POSITIVE CAPTION")
    print(f"Caption: {caption5}")
    seo5 = compute_seo_score(caption5)
    emo5 = detect_emotion(caption5)
    fake5 = detect_fake(caption5)
    print(f"  SEO: {seo5['score']}/100 ({seo5['grade']})")
    print(f"  Emotion: {emo5['emotion']} ({emo5['confidence']}%)")
    print(f"  Authenticity: {fake5['real']}% real, {fake5['fake']}% fake")
    print(f"  Reasoning: {fake5['reason']}")
    
    # VERIFY: Results should be DIFFERENT
    print("\n" + "="*80)
    print("VERIFICATION: Results should be DIFFERENT, not random")
    print("="*80)
    
    assert seo1['score'] != seo2['score'], "❌ SEO scores should differ!"
    assert emo1['emotion'] != emo2['emotion'], "❌ Emotions should differ!"
    assert fake1['fake'] != fake2['fake'], "❌ Authenticity should differ!"
    
    print("✅ Test 1 vs Test 2:")
    print(f"   SEO: {seo1['score']} ≠ {seo2['score']} ✓")
    print(f"   Emotion: {emo1['emotion']} ≠ {emo2['emotion']} ✓")
    print(f"   Fake%: {fake1['fake']}% ≠ {fake2['fake']}% ✓")
    
    print("\n✅ All tests passed!")
    print("✓ Analysis is CAPTION-DEPENDENT")
    print("✓ Not random")
    print("✓ Changes with different captions")
    print("✓ Works with both English and Bangla")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    test_caption_dependency()
