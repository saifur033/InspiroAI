#!/usr/bin/env python
"""
Quick test to verify ML-based reach prediction is working
Tests that predictions vary by caption, day, and hour
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    print("=" * 60)
    print("Testing ML-Based Reach Prediction")
    print("=" * 60)
    
    # Import models
    print("\n1. Loading models...")
    from utils.model_loader import get_model_registry
    from sentence_transformers import SentenceTransformer
    from utils.feature_engineering import predict_reach_for_hours
    
    registry = get_model_registry()
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("   ✓ Models loaded successfully")
    
    # Test 1: Same caption, different days
    print("\n2. Testing: Same caption, different days")
    caption1 = "Check out this amazing offer! Limited time only. Don't miss out! 🎉"
    
    print(f"\n   Caption: '{caption1}'")
    
    days_to_test = ["Monday", "Wednesday", "Friday"]
    results_by_day = {}
    
    for day in days_to_test:
        predictions = predict_reach_for_hours(caption1, day, embedder, registry)
        best_hour, best_prob, _ = predictions[0]
        results_by_day[day] = best_prob
        print(f"   • {day:12} → Best: {best_hour:8} (Score: {best_prob:.2%})")
    
    # Check if predictions vary by day
    unique_scores = len(set(f"{v:.4f}" for v in results_by_day.values()))
    if unique_scores > 1:
        print("   ✓ Predictions VARY by day (different scores)")
    else:
        print("   ⚠ Predictions are the SAME for all days (check model)")
    
    # Test 2: Different captions, same day
    print("\n3. Testing: Different captions, same day (Friday)")
    
    captions = [
        "Check out this amazing offer! Limited time only. Don't miss out! 🎉",
        "Just woke up, time for coffee ☕",
        "The weather is so nice today!"
    ]
    
    results_by_caption = {}
    for i, caption in enumerate(captions, 1):
        predictions = predict_reach_for_hours(caption, "Friday", embedder, registry)
        best_hour, best_prob, _ = predictions[0]
        results_by_caption[i] = best_prob
        print(f"   • Caption {i}: Best: {best_hour:8} (Score: {best_prob:.2%})")
    
    # Check if predictions vary by caption
    unique_caption_scores = len(set(f"{v:.4f}" for v in results_by_caption.values()))
    if unique_caption_scores > 1:
        print("   ✓ Predictions VARY by caption (different scores)")
    else:
        print("   ⚠ Predictions are the SAME for all captions (check model)")
    
    # Test 3: Hour variation for a single day/caption
    print("\n4. Testing: Hour variation (Friday with engaging caption)")
    caption_test = "🔥 Hot deal alert! Save 50% on everything. Shop now! 🛍️"
    predictions = predict_reach_for_hours(caption_test, "Friday", embedder, registry)
    
    print(f"\n   All 24-hour predictions for Friday:")
    for hour_str, prob, _ in predictions:
        bar = "█" * int(prob * 50)  # Visual bar
        print(f"   {hour_str:8} │ {bar:50} {prob:.2%}")
    
    # Get best and worst hours
    best = max(predictions, key=lambda x: x[1])
    worst = min(predictions, key=lambda x: x[1])
    
    print(f"\n   • Best hour: {best[0]} ({best[1]:.2%})")
    print(f"   • Worst hour: {worst[0]} ({worst[1]:.2%})")
    print(f"   • Spread: {(best[1] - worst[1]):.2%}")
    
    if best[1] != worst[1]:
        print("   ✓ Hour variation detected (different predictions across hours)")
    else:
        print("   ⚠ No hour variation (all hours have same prediction)")
    
    print("\n" + "=" * 60)
    print("✅ ML Reach Prediction Test Complete")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
