# ==========================================================
# caption_variations_engine.py — Advanced Caption Variations
# ==========================================================
# Creates TRULY DIFFERENT caption variations with:
# - Different structures
# - Different emotions
# - Different SEO scores
# - Different approaches (hook, story, CTA, data, etc.)

import random
from .utils import detect_language
from .emotion_model import detect_emotion
from .seo_score import compute_seo_score
from .hashtag_ranker import generate_hashtags


class CaptionVariationsEngine:
    """
    Generate TRULY different caption variations.
    Each variation has unique structure, emotion, and approach.
    """
    
    @staticmethod
    def extract_key_ideas(caption: str) -> dict:
        """Extract main ideas from caption"""
        words = caption.lower().split()
        key_words = [w for w in words if len(w) > 4 and w not in {'that', 'this', 'what', 'have', 'with', 'from', 'about'}]
        return {
            'keywords': key_words[:5],
            'length': len(words),
            'original': caption
        }
    
    @staticmethod
    def generate_hook_based(caption: str) -> str:
        """Hook-based approach - Start with attention-grabber"""
        hooks = [
            "🔥 Here's what you need to know:",
            "⚡ Stop right here - this changes everything:",
            "💡 Breakthrough moment:",
            "🎯 You've been missing this:",
            "✨ The secret nobody talks about:",
            "🚀 Game-changer alert:",
            "📢 Heads up! Important update:",
            "💪 This is exactly what you needed:",
        ]
        hook = random.choice(hooks)
        return f"{hook}\n\n{caption}\n\n👉 Drop a comment below!"
    
    @staticmethod
    def generate_story_based(caption: str) -> str:
        """Story-based approach - Create narrative"""
        stories = [
            f"Today I realized something:\n\n{caption}\n\nNow I share this with you. Your turn to act!",
            f"My journey taught me this:\n\n{caption}\n\nHave you experienced this too? Share below!",
            f"Here's the real truth:\n\n{caption}\n\nDon't keep this to yourself. Spread the word! 📣",
            f"Let me tell you something important:\n\n{caption}\n\nWho else feels the same? Comment now! 👇",
        ]
        return random.choice(stories)
    
    @staticmethod
    def generate_data_based(caption: str) -> str:
        """Data/Stats-based approach - Add context"""
        stats = [
            f"📊 Research shows:\n{caption}\n\n💬 What's your experience?",
            f"📈 The statistics:\n{caption}\n\n✋ Who can relate?",
            f"📋 By the numbers:\n{caption}\n\n❓ Is this true for you?",
            f"🔢 The facts:\n{caption}\n\n💭 Your thoughts?",
        ]
        return random.choice(stats)
    
    @staticmethod
    def generate_question_based(caption: str) -> str:
        """Question-based approach - Engagement focused"""
        questions = [
            f"Here's what I think:\n\n{caption}\n\n❓ But what do YOU think? 🤔",
            f"Let me ask you:\n\n{caption}\n\n💬 Does this resonate with you?",
            f"Honest question:\n\n{caption}\n\n🤷 How would you respond?",
            f"Think about this:\n\n{caption}\n\n❔ Sound familiar?",
        ]
        return random.choice(questions)
    
    @staticmethod
    def generate_cta_based(caption: str) -> str:
        """CTA-focused approach - Action oriented"""
        ctas = [
            f"{caption}\n\n🎬 ACTION TIME:\n➡️ Like this post\n➡️ Share your story\n➡️ Tag someone who needs to see this",
            f"{caption}\n\n⭐ Here's what to do:\n1️⃣ Read carefully\n2️⃣ Think about it\n3️⃣ Take action NOW\n\n💪 Don't delay!",
            f"{caption}\n\n🚀 Ready to take action? Here's how:\n✓ Save this post\n✓ Share with your network\n✓ Start implementing today\n\n📍 Comment DONE when you're ready!",
            f"{caption}\n\n⚡ Your move:\n→ Don't ignore this\n→ Share with 3 people\n→ Transform your approach\n\n👊 Let's go!",
        ]
        return random.choice(ctas)
    
    @staticmethod
    def generate_emoji_enhanced(caption: str) -> str:
        """Emoji-enhanced approach - Visual appeal"""
        emoji_sets = [
            "🌟✨💫",
            "💡🔥⚡",
            "🚀🎯💪",
            "❤️💯✅",
            "🎉🌈🎊",
        ]
        emojis = random.choice(emoji_sets)
        
        lines = caption.split('\n')
        enhanced = f"{emojis}\n\n"
        for line in lines:
            enhanced += f"→ {line}\n"
        enhanced += f"\n{emojis}\n\n🔗 Click the link below! 👇"
        
        return enhanced
    
    @staticmethod
    def generate_benefit_focused(caption: str) -> str:
        """Benefit-focused - What's in it for user"""
        benefits = [
            f"Why you SHOULD care about this:\n\n{caption}\n\n✨ This changes EVERYTHING for you.",
            f"Here's what YOU gain:\n\n{caption}\n\n🎁 This is pure value. Don't miss it!",
            f"Your breakthrough moment:\n\n{caption}\n\n💝 This is exactly what you've been looking for!",
            f"The transformation:\n\n{caption}\n\n🌟 Your life gets better starting NOW!",
        ]
        return random.choice(benefits)
    
    @staticmethod
    def generate_controversy_angle(caption: str) -> str:
        """Controversy/Bold angle - Provocative"""
        angles = [
            f"Everyone's saying the opposite, but here's the REAL truth:\n\n{caption}\n\n🔥 Agree or disagree? Let's discuss!",
            f"Most people don't want to hear this:\n\n{caption}\n\n💬 But I had to share it. Your thoughts?",
            f"This is the hard truth nobody wants to face:\n\n{caption}\n\n❗ Are you brave enough to accept it?",
            f"They won't tell you this:\n\n{caption}\n\n🤫 But I'm spilling the tea. React below!",
        ]
        return random.choice(angles)
    
    @staticmethod
    def generate_short_punchy(caption: str) -> str:
        """Short & Punchy - Maximum impact, minimal words"""
        # Extract key phrase
        sentences = caption.split('.')
        main_idea = sentences[0].strip()
        
        punchy = [
            f"💥 {main_idea}\n\n✅ That's it. That's everything.",
            f"🎯 {main_idea}\n\nNo fluff. Just truth. 🔥",
            f"⚡ {main_idea}\n\nBookmark this. Share this. LIVE this.",
            f"🔥 {main_idea}\n\nThat's the whole game right there.",
        ]
        return random.choice(punchy)


def create_truly_different_variations(caption: str, tone: str = "professional") -> dict:
    """
    Create 7 TRULY DIFFERENT variations using different approaches.
    Each one has different structure, emotion, and strategy.
    """
    
    if not caption or not caption.strip():
        return {"error": "Caption is empty", "variations": []}
    
    engine = CaptionVariationsEngine()
    lang = detect_language(caption)
    
    # Generate variations using different approaches
    approaches = [
        engine.generate_hook_based,
        engine.generate_story_based,
        engine.generate_data_based,
        engine.generate_question_based,
        engine.generate_cta_based,
        engine.generate_emoji_enhanced,
        engine.generate_benefit_focused,
    ]
    
    if random.random() > 0.6:  # Add controversy angle 40% of the time
        approaches.append(engine.generate_controversy_angle)
    
    if random.random() > 0.7:  # Add punchy version 30% of the time
        approaches.append(engine.generate_short_punchy)
    
    variations = []
    seen_captions = set()
    
    # Generate unique variations
    for approach in approaches[:7]:  # Take first 7 variations
        try:
            new_caption = approach(caption)
            
            # Skip if duplicate
            if new_caption in seen_captions:
                continue
            
            seen_captions.add(new_caption)
            
            # Calculate metrics for this variation
            seo = compute_seo_score(new_caption) or {}
            emotion = detect_emotion(new_caption) or {}
            hashtags = generate_hashtags(new_caption) or []
            
            variations.append({
                "caption": new_caption,
                "approach": approach.__name__.replace('generate_', '').replace('_', ' ').title(),
                "seo_score": int(seo.get("score", 50)),
                "seo_grade": seo.get("grade", "C"),
                "emotion": emotion.get("emotion", emotion.get("top_emotion", "NEUTRAL")).upper(),
                "emotion_confidence": int(emotion.get("confidence", 0)),
                "hashtags": hashtags[:5] if hashtags else [],
                "length": len(new_caption.split()),
            })
        except Exception as e:
            continue
    
    return {
        "success": True,
        "original_caption": caption,
        "tone": tone,
        "language": lang,
        "total_variations": len(variations),
        "variations": variations,
        "insight": f"Created {len(variations)} completely different approaches with unique SEO scores and emotions. Each one is optimized differently!"
    }


# Example usage:
# result = create_truly_different_variations("Check out my new product!", "professional")
# print(result)
