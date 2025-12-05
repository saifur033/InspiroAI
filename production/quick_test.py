"""
QUICK START - Enhanced InspiroAI
================================

✨ What's New:
- AI-powered caption rewriter (transforms fake → real)
- Intelligent fakeness analysis with specific issues
- Dual Facebook posting (original or rewritten)
- All existing features 100% intact

🚀 To Test:
"""

# 1. Start the Streamlit app
import subprocess
import sys

def start_app():
    """Start InspiroAI app"""
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--logger.level=error'
    ], cwd='production')

# 2. Test the rewriter directly
def test_rewriter():
    """Quick test of caption rewriter"""
    from utils.caption_rewriter import CaptionRewriter
    
    test_captions = [
        "I am a student from East West University looking for opportunities. Connect with me! #Success",
        "honestly not sure what im doing lol but at least its friday",
        "🚨 LIMITED OFFER! Click here NOW!!! http://spamsite.com #BuyNow"
    ]
    
    print("=" * 70)
    print("CAPTION REWRITER TEST")
    print("=" * 70)
    
    for caption in test_captions:
        print(f"\n❌ FAKE: {caption}")
        print(f"✅ REAL: {CaptionRewriter.rewrite(caption)}")
        
        issues = CaptionRewriter.analyze_fakeness(caption)
        if issues['issues']:
            print(f"   Issues: {', '.join(issues['issues'])}")
        print()

# 3. Test emotion detection
def test_emotions():
    """Quick test of emotion detection"""
    from utils.inference import EmotionPredictor
    
    captions = [
        "I'm so happy today! Everything is amazing!",
        "Really sad about what happened",
        "This is shocking and unexpected"
    ]
    
    print("=" * 70)
    print("EMOTION DETECTION TEST")
    print("=" * 70)
    
    for caption in captions:
        result = EmotionPredictor.predict(caption)
        print(f"\nCaption: {caption}")
        print(f"Emotion: {result.get('emotion', 'Unknown').upper()}")
        print(f"Confidence: {result.get('confidence', 0):.1%}")
    print()

# 4. Test fake/real detection
def test_status():
    """Quick test of fake/real detection"""
    from utils.inference import StatusPredictor
    from utils.model_loader import get_model_registry
    from sentence_transformers import SentenceTransformer
    
    captions = [
        "honestly just vibing today lol no idea what im doing",
        "I am a student from XYZ University looking for opportunities",
        "Check out this amazing LIMITED TIME OFFER! #BuyNow"
    ]
    
    print("=" * 70)
    print("AUTHENTICITY DETECTION TEST")
    print("=" * 70)
    
    # Load models
    model_registry = get_model_registry()
    embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    for caption in captions:
        result = StatusPredictor.predict(caption, embedder=embedder, model_registry=model_registry)
        status = "🟢 REAL" if result['suspicion_score'] < 0.55 else "🔴 FAKE"
        print(f"\nCaption: {caption}")
        print(f"Status: {status}")
        print(f"Score: {result['suspicion_score']:.1%}")
    print()

if __name__ == "__main__":
    import os
    os.chdir('production')
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                       🎯 InspiroAI - Enhanced                             ║
    ║                                                                            ║
    ║  ✨ NEW: AI-Powered Caption Rewriter                                      ║
    ║  ✅ ENHANCED: Detailed Fakeness Analysis                                  ║
    ║  🚀 IMPROVED: Dual Facebook Posting                                       ║
    ║                                                                            ║
    ║  Choose an option:                                                        ║
    ║  1. Test Rewriter      - See fake captions converted to real              ║
    ║  2. Test Emotions      - Detect 6 emotions                               ║
    ║  3. Test Status        - Detect fake/real authenticity                   ║
    ║  4. Start App          - Launch full Streamlit app                       ║
    ║  5. Exit               - Close                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            test_rewriter()
        elif choice == "2":
            test_emotions()
        elif choice == "3":
            test_status()
        elif choice == "4":
            print("\n🚀 Starting InspiroAI app...")
            print("Open your browser: http://localhost:8501")
            start_app()
            break
        elif choice == "5":
            print("\nGoodbye! 👋")
            break
        else:
            print("❌ Invalid option. Try again.")
