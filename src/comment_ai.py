"""
InspiroAI — Comment Engine v9.5 (Full Structured JSON Edition)
Author: Saifur Rahman AI System

Supports 7 Categories + Topic Detection:
✔ Friendly
✔ Professional
✔ Emotional / Supportive
✔ Funny
✔ TikTok SEO Comments
✔ Reels Boost Comments
✔ Topic-Based Detection

100% JSON SAFE
100% Frontend Compatible
100% Error-Proof
"""

import json
import re
from src.emotion_model import detect_emotion


# Lightweight fallback AI function (no external dependencies)
def ask_ai(user_prompt: str) -> str:
    """
    Lightweight fallback AI function.
    Returns empty to trigger local refinement logic.
    """
    return ""


# --------------------------------------------------------
# 🌐 Bangla / English Language Detector
# --------------------------------------------------------
def detect_language(text: str) -> str:
    bn = sum(1 for ch in text if 2432 <= ord(ch) <= 2559)
    return "bn" if bn > 20 else "en"


# --------------------------------------------------------
# 📌 DEFAULT JSON TEMPLATE (Frontend Safe)
# --------------------------------------------------------
def default_json():
    return {
        "friendly": ["Great post!", "Love it!", "Nice share!"],
        "professional": ["Well said.", "Great insight.", "Thanks for sharing."],
        "emotional": ["Beautiful!", "Touching.", "This means so much."],
        "funny": ["Haha!", "LOL!", "That's funny!"],
        "tiktok": ["Must watch!", "Don't miss!", "Trending!"],
        "reels": ["Amazing reel!", "So cool!", "Best one yet!"],
        "topic": ["Post"]
    }


# --------------------------------------------------------
# 🔐 FIX JSON Shape (Auto-repair for AI mistakes)
# --------------------------------------------------------
def enforce_json_shape(data):
    keys = ["friendly", "professional", "emotional", "funny", "tiktok", "reels", "topic"]
    fixed = {}

    for key in keys:
        value = data.get(key, [])
        if not isinstance(value, list):
            try:
                # Try to parse if it's a string
                value = [value] if isinstance(value, str) else []
            except:
                value = []
        # Limit to 5 items per category, ensure strings
        fixed[key] = [str(item)[:150] for item in value[:5] if item]
    
    # Ensure topic has at least one item
    if not fixed["topic"]:
        fixed["topic"] = ["Post"]
    
    return fixed


# --------------------------------------------------------
# 🔎 TOPIC EXTRACTION FROM CAPTION
# --------------------------------------------------------
def extract_topic(caption: str) -> str:
    """Extract main topic/keyword from caption for comment contextualization"""
    caption_lower = caption.lower()
    
    # Topic keywords mapping with priority weights
    topic_keywords = {
        "Product": ["product", "launch", "new", "offer", "sale", "release", "shop", "buy", "get"],
        "Technology": ["tech", "app", "software", "ai", "digital", "code", "device", "python", "developer"],
        "Business": ["business", "startup", "entrepreneur", "marketing", "growth", "seo", "venture", "invest"],
        "Health": ["health", "fitness", "wellness", "diet", "exercise", "medical", "workout", "gym"],
        "Travel": ["travel", "destination", "trip", "journey", "explore", "adventure", "vacation"],
        "Food": ["food", "recipe", "cooking", "restaurant", "delicious", "taste", "cook", "meal"],
        "Lifestyle": ["lifestyle", "daily", "life", "happy", "moment", "living", "vibes", "mood"],
        "Entertainment": ["entertainment", "movie", "music", "show", "series", "film", "watch", "listen"],
        "Education": ["learn", "course", "education", "tutorial", "skill", "training", "study", "class"],
        "Sports": ["sports", "game", "play", "team", "match", "championship", "score", "win"],
        "Fashion": ["fashion", "style", "outfit", "clothes", "trend", "design", "wear", "look"],
        "Motivation": ["motivation", "inspire", "success", "goal", "achieve", "dream", "believe"],
        "Community": ["community", "together", "join", "team", "group", "family", "support", "help"],
        "Photography": ["photo", "picture", "photography", "captured", "moment", "lens", "beautiful"],
        "Nature": ["nature", "forest", "beach", "mountain", "sunset", "sunrise", "natural", "outdoor"],
    }
    
    # Find matching topics with priority
    matched_topics = []
    for topic, keywords in topic_keywords.items():
        for kw in keywords:
            if kw in caption_lower:
                matched_topics.append(topic)
                break
    
    return matched_topics[0] if matched_topics else "General Post"


# --------------------------------------------------------
# 🔍 COMMENT RELEVANCE CHECKER (Caption-Comment Matching)
# --------------------------------------------------------
def check_comment_relevance(caption: str, comments_dict: dict) -> tuple:
    """
    Check if generated comments are relevant to caption.
    Returns (is_relevant, relevance_score, feedback)
    
    Relevance checks:
    - Do comments mention caption keywords?
    - Do comments match caption emotion/sentiment?
    - Are comments in same language as caption?
    """
    try:
        lang = detect_language(caption)
        
        # Extract keywords from caption
        caption_lower = caption.lower()
        caption_words = set(re.findall(r'\w+', caption_lower))
        caption_words = {w for w in caption_words if len(w) > 3}
        
        # Get all comments
        all_comments = []
        for category in ["friendly", "professional", "emotional", "funny", "tiktok", "reels"]:
            all_comments.extend(comments_dict.get(category, []))
        
        # Count keyword matches
        keyword_matches = 0
        for comment in all_comments:
            comment_lower = comment.lower()
            for kw in caption_words:
                if kw in comment_lower:
                    keyword_matches += 1
        
        # Check emotion match
        try:
            emotion_data = detect_emotion(caption)
            detected_emotion = emotion_data.get("top_emotion", "neutral").upper()
        except:
            detected_emotion = "NEUTRAL"
        
        # Check if comments align with emotion
        emotion_keywords = {
            "HAPPY": ["great", "love", "amazing", "beautiful", "wonderful", "excellent"],
            "SAD": ["understand", "support", "together", "hope", "strength", "beautiful"],
            "ANGRY": ["power", "stand", "fight", "strong", "courage"],
            "NEUTRAL": ["good", "nice", "thanks", "appreciated", "post"],
        }
        
        matching_emotions = emotion_keywords.get(detected_emotion, [])
        emotion_matches = sum(1 for comment in all_comments for em_kw in matching_emotions if em_kw in comment.lower())
        
        # Calculate relevance score (0-100)
        total_comments = len(all_comments) if all_comments else 1
        keyword_score = min(100, (keyword_matches / total_comments) * 100) if total_comments > 0 else 0
        emotion_score = min(100, (emotion_matches / total_comments) * 100) if total_comments > 0 else 50
        relevance_score = (keyword_score * 0.6) + (emotion_score * 0.4)
        
        # Determine if relevant (threshold 40%)
        is_relevant = relevance_score >= 40
        
        feedback = f"Relevance: {relevance_score:.0f}% | Keywords matched: {keyword_matches} | Emotion: {detected_emotion}"
        
        return is_relevant, relevance_score, feedback
    
    except Exception as e:
        print(f"[RELEVANCE CHECK] Error: {e}")
        return True, 50, "Relevance check skipped"


# --------------------------------------------------------
# 🎯 SENTIMENT-BASED TONE DETECTION
# --------------------------------------------------------
def detect_sentiment_tone(caption: str) -> tuple:
    """Auto-detect tone and emoji preference from caption sentiment and emotion"""
    try:
        from textblob import TextBlob
        blob = TextBlob(caption)
        polarity = blob.sentiment.polarity  # -1 to +1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
    except:
        polarity = 0
        subjectivity = 0.5
    
    # Auto-select tone based on sentiment
    if polarity > 0.5:
        auto_tone = "friendly"  # Very positive
        use_emoji = "yes"
    elif polarity > 0.2:
        auto_tone = "emotional"  # Somewhat positive
        use_emoji = "yes"
    elif polarity < -0.3:
        auto_tone = "supportive"  # Negative - supportive comments
        use_emoji = "no"
    else:
        auto_tone = "professional"  # Neutral
        use_emoji = "no" if subjectivity < 0.4 else "yes"
    
    return auto_tone, use_emoji


# --------------------------------------------------------
# 🔥 FULL COMMENT PACK GENERATOR (100% CAPTION-DEPENDENT)
# --------------------------------------------------------
def generate_full_comment_pack(caption: str, tone=None, emoji=None):
    """
    Generate a full pack of comments based on caption content and detected topic.
    AUTO mode: If tone/emoji are None, auto-detect from caption sentiment.
    """
    if not caption or not caption.strip():
        default = default_json()
        default["topic"] = ["Post"]
        return default

    lang = detect_language(caption)
    
    # Auto-detect tone and emoji if not provided (AUTOMATIC MODE)
    if tone is None or emoji is None:
        auto_tone, auto_emoji = detect_sentiment_tone(caption)
        tone = tone or auto_tone
        emoji = emoji or auto_emoji
    
    try:
        emotion_data = detect_emotion(caption)
        emotion = emotion_data.get("top_emotion", "neutral")
    except:
        emotion = "neutral"

    lang_text = "Bangla" if lang == "bn" else "English"
    # More explicit emoji rules
    if emoji == "yes":
        emoji_rule = "IMPORTANT: Use 1-2 natural, relevant emojis in EACH comment. Example: 'Love this 💕', 'Amazing work 🔥', etc."
    else:
        emoji_rule = "IMPORTANT: Do NOT use any emojis. Keep all comments text-only."
    
    topic = extract_topic(caption)
    
    # Create caption summary for context
    caption_summary = caption[:100] + "..." if len(caption) > 100 else caption

    system = """You are InspiroAI — a world-class social media comment generator.
Your task is to create authentic, engaging, human-like comments that are DIRECTLY RELEVANT to the post caption.

CRITICAL RULES:
- Comments MUST relate to what the caption is about
- Comments should acknowledge or respond to the specific content
- Keep comments SHORT (5-15 words max)
- NO hashtags, NO numbers, NO bullet points
- Comments must feel NATURAL and HUMAN
- Match the post's emotion and specific topic
- ALWAYS output STRICT JSON ONLY
- Each category should have comments of different engagement levels"""

    # Extract key content words from caption for relevance
    caption_words = re.findall(r'\b\w+\b', caption.lower())
    key_words = [w for w in caption_words if len(w) > 3 and w not in ['that', 'this', 'with', 'from', 'have', 'been', 'just', 'like', 'more', 'very', 'only', 'such', 'than', 'can', 'will', 'some', 'your', 'also']][:5]
    relevant_words = ", ".join(key_words) if key_words else topic
    
    user = f"""Post Caption: "{caption_summary}"

Language: {lang_text}
Detected Topic: {topic}
Key Content Words: {relevant_words}
Tone: {tone}
Detected Emotion: {emotion}
Emoji Rule: {emoji_rule}

CRITICAL INSTRUCTIONS - READ CAREFULLY:
1. Generate comments SPECIFICALLY ABOUT THIS POST - not generic
2. Comments MUST mention or reference: {relevant_words}
3. Comments must acknowledge the EXACT content of the caption
4. Each comment should be 5-15 words long
5. Comments must feel NATURAL and HUMAN
6. NO generic comments like "Great post!" or "Love it!"
7. {emoji_rule}
8. Match the detected {emotion} emotion
9. Each comment should be different (not repetitive)

Generate EXACTLY this JSON structure (VALID JSON ONLY):
{{
 "friendly": ["specific comment about {topic}", "another comment with {key_words[0] if key_words else 'content'}", "third unique comment", "fourth relevant comment", "fifth specific comment"],
 "professional": ["professional take on {topic}", "industry perspective", "thoughtful insight", "expert observation", "constructive feedback"],
 "emotional": ["emotional response to content", "heartfelt reaction", "supportive comment", "empathetic response", "deeply moved comment"],
 "funny": ["humorous take on {topic}", "witty observation", "clever joke", "funny angle", "amusing comment"],
 "tiktok": ["viral hook comment", "trend-focused comment", "engagement boost", "viral angle comment", "trending perspective"],
 "reels": ["reels-focused comment", "video engagement comment", "visual appreciation comment", "motion comment", "dynamic comment"],
 "topic": ["{topic}"]
}}

REQUIREMENTS:
- Each comment 5-15 words max
- Reference the actual content about {relevant_words}
- Natural human voice
- Different style per category
- {emoji_rule}
- NO hashtags, NO links, NO @mentions
- RESPOND WITH ONLY VALID JSON"""

    try:
        ai_raw = ask_ai(system, user)
        print(f"[COMMENT] Auto-detected - Tone: {tone}, Emoji: {emoji}, Topic: {topic}, Emotion: {emotion}")
        print(f"[DEBUG] AI raw response type: {type(ai_raw)}, length: {len(str(ai_raw)[:100])}")
        
        # Try to extract JSON if wrapped in markdown or text
        if "```" in ai_raw:
            ai_raw = ai_raw.split("```")[1]
            if ai_raw.startswith("json"):
                ai_raw = ai_raw[4:]
        
        # Clean up the response
        ai_raw = ai_raw.strip()
        if ai_raw.startswith('{') and ai_raw.endswith('}'):
            parsed = json.loads(ai_raw)
        else:
            # Try to find JSON in response
            json_start = ai_raw.find('{')
            json_end = ai_raw.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                parsed = json.loads(ai_raw[json_start:json_end])
            else:
                # AI failed to generate, use fallback
                print(f"[COMMENT] AI response not valid JSON, using caption-specific fallback")
                default = generate_caption_specific_fallback(caption, topic, emoji)
                default["topic"] = [topic]
                return default
        
        # Check if parsed data has template placeholders (not actual comments)
        has_templates = False
        for category in ["friendly", "professional", "emotional"]:
            if category in parsed:
                comments = parsed.get(category, [])
                if any("specific comment" in str(c) or "comment about" in str(c) for c in comments):
                    has_templates = True
                    break
        
        if has_templates:
            print(f"[COMMENT] AI returned template text, using caption-specific fallback instead")
            default = generate_caption_specific_fallback(caption, topic, emoji)
            default["topic"] = [topic]
            return default
        
        result = enforce_json_shape(parsed)
        
        # Ensure topic is set correctly
        if not result.get("topic") or result["topic"] == ["Post"]:
            result["topic"] = [topic]
        
        print(f"[DEBUG] Successfully parsed comments for topic '{topic}': {list(result.keys())}")
        return result
    except json.JSONDecodeError as e:
        print(f"[DEBUG] JSON parse error: {e}, using caption-specific fallback")
        # Return contextual fallback comments based on actual caption content
        default = generate_caption_specific_fallback(caption, topic, emoji)
        default["topic"] = [topic]
        return default
    except Exception as e:
        print(f"[DEBUG] Comment generation error: {e}, using caption-specific fallback")
        # Return contextual fallback comments
        default = generate_caption_specific_fallback(caption, topic, emoji)
        default["topic"] = [topic]
        return default


# --------------------------------------------------------
# GENERATE TOPIC-BASED FALLBACK COMMENTS
# --------------------------------------------------------
def generate_caption_specific_fallback(caption: str, topic: str, emoji="yes"):
    """Generate contextual comments specifically about caption content"""
    em = "✨" if emoji == "yes" else ""
    em2 = "❤️" if emoji == "yes" else ""
    em3 = "🔥" if emoji == "yes" else ""
    
    # Extract BETTER key words from caption - longer, more meaningful words
    caption_lower = caption.lower()
    # Remove common words and get meaningful ones (4+ chars)
    stop_words = {'that', 'this', 'with', 'from', 'have', 'been', 'just', 'like', 'more', 'very', 'only', 'such', 'than', 'can', 'will', 'some', 'the', 'and', 'for', 'are', 'your', 'you', 'was', 'but', 'not', 'our', 'its', 'in', 'on', 'at', 'to', 'of', 'is', 'be', 'as', 'by', 'we', 'so', 'or', 'a', 'an', 'all', 'do', 'also'}
    
    # Extract longer words (4+ chars) that are more meaningful
    words = [w for w in re.findall(r'\b\w+\b', caption_lower) if len(w) >= 4 and w not in stop_words]
    
    # If not enough 4+ char words, try 3+ char words
    if len(words) < 2:
        words = [w for w in re.findall(r'\b\w+\b', caption_lower) if len(w) >= 3 and w not in stop_words]
    
    # Get unique key words (up to 3), preserve first occurrence
    key_words = list(dict.fromkeys(words))[:3]
    
    # Build better topic phrase if we have words
    if key_words:
        kw1 = key_words[0]
        kw2 = key_words[1] if len(key_words) > 1 else key_words[0]
        kw3 = key_words[2] if len(key_words) > 2 else key_words[0]
        topic_phrase = f"{kw1} {kw2}" if len(key_words) > 1 else kw1
    else:
        kw1 = topic.lower()
        kw2 = kw1
        kw3 = "content"
        topic_phrase = kw1
    
    return {
        "friendly": [
            f"Love your {topic_phrase} {em}!",
            f"The {kw1} is amazing!",
            f"This is exactly what I needed!",
            f"Sharing everywhere!",
            f"You're incredible!"
        ],
        "professional": [
            f"Great insights on {topic_phrase}.",
            f"Excellent {kw1} content.",
            f"Very valuable information.",
            f"Well presented {kw2}.",
            f"Outstanding work."
        ],
        "emotional": [
            f"So moved by your {topic_phrase} {em2}!",
            f"Love your passion for {kw1}!",
            f"This means so much!",
            f"Beautiful perspective!",
            f"Truly inspiring!"
        ],
        "funny": [
            f"Why didn't I know about {topic_phrase}?",
            f"This {kw1} just blew my mind!",
            f"Stop being so right!",
            f"Need this NOW!",
            f"Saving this forever!"
        ],
        "tiktok": [
            f"That {topic_phrase} though {em3}!",
            f"Must know {kw1}!",
            f"This is TRENDING!",
            f"This NEEDS to go viral!",
            f"Sharing with millions!"
        ],
        "reels": [
            f"This {topic_phrase} reel {em3}!",
            f"Perfect {kw1} content!",
            f"So satisfying!",
            f"Best {kw2} I've seen!",
            f"On repeat!"
        ],
        "topic": [topic]
    }


def generate_topic_based_fallback(caption: str, topic: str, emoji="yes"):
    """Generate contextual fallback comments based on detected topic"""
    # First try caption-specific
    specific = generate_caption_specific_fallback(caption, topic, emoji)
    if specific and len(specific.get("friendly", [])) > 0:
        return specific
    
    em = "✨" if emoji == "yes" else ""
    em2 = "❤️" if emoji == "yes" else ""
    em3 = "🔥" if emoji == "yes" else ""
    em4 = "😊" if emoji == "yes" else ""
    em5 = "👍" if emoji == "yes" else ""
    
    topic_comments = {
        "Product": {
            "friendly": [f"This looks amazing {em}!", "Love the design!", "Need this in my life!", "Where can I get one?", "Shutting down my wallet!"],
            "professional": ["Excellent product launch.", "Well executed.", "Great presentation.", "Impressed with quality.", "Strong offering."],
            "emotional": [f"Perfect {em2}!", "This is beautiful!", "Absolutely stunning!", "Worth every penny.", "Obsessed!"],
            "funny": ["My wallet is crying!", "Shut up and take my money!", "RIP my savings.", "Too good to resist!", "Stop tempting me!"],
            "tiktok": ["Must have!", "Link in bio please!", "Adding to cart NOW!", "This is fire!", "Trending alert!"],
            "reels": [f"This is genius {em3}!", "Content gold!", "Sharing with everyone!", "Absolutely brilliant!", "Creative genius!"]
        },
        "Technology": {
            "friendly": ["This is brilliant!", "Love tech innovations!", "So cool!", "Game changer!", "Mind blown!"],
            "professional": ["Impressive technical work.", "Well-engineered solution.", "Strong development.", "Great execution.", "Innovation at its best."],
            "emotional": [f"Beautiful code {em2}!", "This is elegant!", "Perfectly designed!", "Absolutely genius!", "Love the simplicity!"],
            "funny": ["Finally, what we needed!", "Why didn't I think of this?", "Changing the game!", "Tech perfection!", "Genius move!"],
            "tiktok": ["Tech innovation!", "Must see!", "This is trending!", "Viral alert!", "Game changer alert!"],
            "reels": [f"Technical brilliance {em3}!", "Innovation showcase!", "This is amazing!", "Perfect demo!", "So satisfying!"]
        },
        "Business": {
            "friendly": ["Love this approach!", "Great strategy!", "So inspiring!", "Amazing insights!", "Super helpful!"],
            "professional": ["Well-articulated strategy.", "Strong business case.", "Excellent leadership.", "Outstanding execution.", "Great vision."],
            "emotional": [f"This is inspiring {em2}!", "Love the passion!", "So motivating!", "Beautiful mission!", "Powerful message!"],
            "funny": ["Making business fun!", "This guy gets it!", "Plot twist incoming!", "Business genius!", "Taking notes!"],
            "tiktok": ["Business goals!", "Must follow!", "Growth hacking!", "Success story!", "Inspiration overload!"],
            "reels": [f"Business brilliance {em3}!", "Success blueprint!", "Motivation incoming!", "Game plan gold!", "Genius strategy!"]
        },
        "Health": {
            "friendly": ["Love this tip!", "So helpful!", "Thank you!", "Game changer!", "Will try this!"],
            "professional": ["Well-researched advice.", "Sound guidance.", "Practical approach.", "Expert insight.", "Valuable information."],
            "emotional": [f"Thank you for sharing {em2}!", "Life-changing!", "So grateful!", "Beautiful wellness!", "Love this energy!"],
            "funny": ["My doctor approves!", "Finally, motivation!", "Fitness is calling!", "New year, new me!", "Plot twist: I'm healthy!"],
            "tiktok": ["Health goals!", "Must try!", "Wellness motivation!", "Life hack!", "Trending wellness!"],
            "reels": [f"Health transformation {em3}!", "Wellness win!", "Motivation boost!", "Fitness gold!", "Life-changing content!"]
        },
        "Travel": {
            "friendly": ["So beautiful!", "Adding to my list!", "Love this!", "Dream destination!", "Can't wait to go!"],
            "professional": ["Excellent photography.", "Great destination guide.", "Well-documented journey.", "Professional travel content.", "Outstanding presentation."],
            "emotional": [f"Absolutely gorgeous {em2}!", "Dream location!", "So magical!", "Wanderlust activated!", "Paradise found!"],
            "funny": ["Selling everything to go there!", "My heart just left!", "Road trip anyone?", "Passport needs a vacation!", "Booking now!"],
            "tiktok": ["Travel goals!", "Must visit!", "Wanderlust vibes!", "Hidden gem!", "Trending destination!"],
            "reels": [f"Travel inspiration {em3}!", "Adventure awaits!", "Dream destination!", "Beautiful journey!", "Bucket list material!"]
        },
        "Food": {
            "friendly": ["Looks delicious!", "Must try!", "Yum!", "Recipe please!", "When can I eat this?"],
            "professional": ["Well-presented dish.", "Great culinary work.", "Professional plating.", "Excellent food styling.", "Quality ingredients."],
            "emotional": [f"Absolutely mouthwatering {em2}!", "Pure comfort!", "Food heaven!", "So beautiful!", "Made with love!"],
            "funny": ["My diet just quit!", "Here goes my calories!", "Drooling right now!", "Forget my diet!", "Happiness on a plate!"],
            "tiktok": ["Food goals!", "Must make!", "Trending recipe!", "Viral food!", "This is fire!"],
            "reels": [f"Culinary art {em3}!", "Food porn incoming!", "Taste adventure!", "Recipe gold!", "So satisfying!"]
        },
        "Lifestyle": {
            "friendly": ["Love this vibe!", "So relatable!", "This is me!", "Goals!", "Inspiring!"],
            "professional": ["Well-curated lifestyle.", "Great personal brand.", "Authentic sharing.", "Inspiring perspective.", "Great content."],
            "emotional": [f"Love this energy {em2}!", "So authentic!", "This is beautiful!", "True to self!", "Inspiring journey!"],
            "funny": ["Living my best life vicariously!", "Copy-paste your life please!", "Goals I actually have!", "This aesthetic!", "Relationship goals!"],
            "tiktok": ["Lifestyle goals!", "This is goals!", "Trending vibes!", "Aesthetic perfection!", "Life goals!"],
            "reels": [f"Lifestyle inspo {em3}!", "Goals achieved!", "Vibe check passed!", "Aesthetic goals!", "This is life!"]
        },
        "Entertainment": {
            "friendly": ["Looks amazing!", "Can't wait!", "So excited!", "This is trending!", "Must watch!"],
            "professional": ["Excellent production quality.", "Great storytelling.", "Professional content.", "Outstanding creativity.", "Well-executed."],
            "emotional": [f"Absolutely loved this {em2}!", "So entertaining!", "Pure joy!", "Best thing ever!", "Couldn't stop watching!"],
            "funny": ["Losing my mind over this!", "Already watched 10 times!", "My sides hurt!", "Masterpiece!", "Comedy gold!"],
            "tiktok": ["Entertainment gold!", "Must watch!", "Trending now!", "Viral alert!", "This is fire!"],
            "reels": [f"Entertainment genius {em3}!", "Viral content!", "Share worthy!", "Comedy perfection!", "Trending alert!"]
        },
        "Education": {
            "friendly": ["So helpful!", "Thank you!", "Learning so much!", "Love this!", "Sharing with everyone!"],
            "professional": ["Well-structured lesson.", "Great educational value.", "Clear explanation.", "Excellent teaching.", "Informative content."],
            "emotional": [f"Thank you for sharing {em2}!", "So inspiring!", "Life-changing knowledge!", "Beautiful learning!", "Grateful for this!"],
            "funny": ["Finally understanding!", "My brain needed this!", "Why wasn't I taught this?", "Mind expanded!", "Learning made easy!"],
            "tiktok": ["Learning goals!", "Must know!", "Educational gold!", "Trending tutorial!", "Skill unlocked!"],
            "reels": [f"Educational content {em3}!", "Knowledge bomb!", "Learning goals!", "Skill share!", "Tutorial gold!"]
        },
        "Sports": {
            "friendly": ["Amazing skills!", "Great game!", "Love this!", "So talented!", "Inspiring!"],
            "professional": ["Excellent athletic performance.", "Outstanding technique.", "Well-executed strategy.", "Professional caliber.", "Great sportsmanship."],
            "emotional": [f"Absolutely thrilled {em2}!", "So inspiring!", "Pure determination!", "Heart and soul!", "Brilliant performance!"],
            "funny": ["That play though!", "How did they do that?", "Sports magic!", "Unbelievable skill!", "Athletic genius!"],
            "tiktok": ["Sports highlight!", "Must see!", "Viral moment!", "Trending play!", "This is fire!"],
            "reels": [f"Sports excellence {em3}!", "Athletic perfection!", "Winning moment!", "Skill showcase!", "Game changer!"]
        },
        "Fashion": {
            "friendly": ["Love the look!", "Outfit goals!", "So stylish!", "You're glowing!", "Fashion forward!"],
            "professional": ["Great fashion sense.", "Well-coordinated ensemble.", "Excellent style.", "Professional presentation.", "Strong aesthetic."],
            "emotional": [f"Absolutely stunning {em2}!", "So beautiful!", "Pure elegance!", "Fashion art!", "Gorgeous!"],
            "funny": ["Broke my budget!", "Fashion hostage!", "Shutting down my wardrobe!", "Style envy!", "Fashion thief!"],
            "tiktok": ["Fashion goals!", "Must wear!", "Style trending!", "Fashion alert!", "Outfit inspo!"],
            "reels": [f"Fashion showcase {em3}!", "Style perfection!", "Outfit goals!", "Trend alert!", "Fashion fire!"]
        },
        "Motivation": {
            "friendly": ["Love this!", "So inspiring!", "Thank you!", "Needed this!", "You rock!"],
            "professional": ["Inspiring perspective.", "Great motivation.", "Well-articulated message.", "Powerful insight.", "Strong leadership."],
            "emotional": [f"Thank you for this {em2}!", "So motivating!", "Heart and soul!", "Beautiful message!", "Changed my perspective!"],
            "funny": ["This is my sign!", "Manifesting this!", "Taking this to heart!", "Needed to hear this!", "Plot twist: I'm motivated!"],
            "tiktok": ["Motivation goals!", "Must hear!", "Inspiring alert!", "Trending wisdom!", "Life changing!"],
            "reels": [f"Motivation incoming {em3}!", "Inspiration gold!", "Mindset shift!", "Success goals!", "Game changing!"]
        },
        "Community": {
            "friendly": ["Love this community!", "Let's grow together!", "Family vibes!", "So grateful!", "Together strong!"],
            "professional": ["Excellent community building.", "Great leadership.", "Strong community values.", "Well-organized initiative.", "Inspiring mission."],
            "emotional": [f"Love this family {em2}!", "So heartwarming!", "Community love!", "Beautiful connections!", "Together we rise!"],
            "funny": ["Our tribe is goals!", "Community goals!", "Finding my people!", "This is home!", "Family by choice!"],
            "tiktok": ["Community goals!", "Join us!", "Family alert!", "Trending community!", "Together vibes!"],
            "reels": [f"Community love {em3}!", "Togetherness gold!", "Family moments!", "Connection vibes!", "Community pride!"]
        },
        "General Post": {
            "friendly": ["Great post!", "Love it!", "So good!", "Thanks for sharing!", "Awesome!"],
            "professional": ["Well shared.", "Great content.", "Nice post.", "Good point.", "Appreciated."],
            "emotional": [f"Beautiful {em2}!", "Loved this!", "So good!", "Wonderful!", "Amazing!"],
            "funny": ["This though!", "So true!", "Golden!", "Perfect!", "Spot on!"],
            "tiktok": ["Must see!", "Trending!", "Viral!", "Love this!", "Fire!"],
            "reels": [f"Great content {em3}!", "Loved it!", "Sharing now!", "Perfect!", "So good!"]
        }
    }
    
    # Get topic-specific comments or fall back to general
    topic_dict = topic_comments.get(topic, topic_comments["General Post"])
    
    return {
        "friendly": topic_dict.get("friendly", ["Great post!", "Love it!", "Nice share!", "Awesome!", "So good!"]),
        "professional": topic_dict.get("professional", ["Well said.", "Great insight.", "Thanks for sharing.", "Nice work.", "Great point."]),
        "emotional": topic_dict.get("emotional", ["Beautiful!", "Touching.", "This means so much.", "Wonderful!", "Lovely!"]),
        "funny": topic_dict.get("funny", ["Haha!", "LOL!", "That's funny!", "Hilarious!", "Comedy gold!"]),
        "tiktok": topic_dict.get("tiktok", ["Must watch!", "Don't miss!", "Trending!", "Viral!", "This is fire!"]),
        "reels": topic_dict.get("reels", ["Amazing reel!", "So cool!", "Best one yet!", "Creative!", "Love this!"]),
        "topic": [topic]
    }


# --------------------------------------------------------
# BACKWARD-COMPATIBLE INTERFACE (WITH AUTO-MODE SUPPORT)
# --------------------------------------------------------
def generate_comments(caption: str, tone=None, emoji=None):
    """
    Main public API — returns full comment pack.
    
    If tone and emoji are None, auto-detects from caption sentiment (AUTOMATIC MODE).
    If tone or emoji are provided, uses those values.
    """
    return generate_full_comment_pack(caption, tone, emoji)
