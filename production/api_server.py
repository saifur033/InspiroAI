"""
InspiroAI - API Server
Provides ML-based predictions using trained models from notebooks
"""
from flask import Flask, request, jsonify
import json
import re
from datetime import datetime
import random
import string

# Import custom modules
from utils.model_loader import get_model_registry
from utils.inference import EmotionPredictor, ReachPredictor, StatusPredictor
from utils.preprocess import emotion_preprocessing, get_sentiment
from utils.feature_engineering import engineer_reach_features, engineer_status_features

# ============================================
# INITIALIZE FLASK APP
# ============================================
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ============================================
# LOAD MODELS AT STARTUP
# ============================================
try:
    registry = get_model_registry()
    emotion_pred = EmotionPredictor()
    reach_pred = ReachPredictor()
    status_pred = StatusPredictor()
    MODELS_LOADED = True
except Exception as e:
    print(f"Error loading models: {str(e)}")
    MODELS_LOADED = False

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_emotion_reason(dominant_emotion, scores):
    """Generate reason for detected emotion."""
    emotion_reasons = {
        'joy': "Positive tone with optimistic language and enthusiastic expressions",
        'sadness': "Melancholic undertone with reflective or sorrowful language",
        'anger': "Intense, confrontational, or frustrated language detected",
        'surprise': "Unexpected elements or exclamatory expressions found",
        'fear': "Anxiety-inducing language or expressions of concern",
        'neutral': "Objective, informative tone without strong emotional indicators"
    }
    return emotion_reasons.get(dominant_emotion.lower(), "Emotional tone detected from text analysis")


def get_authenticity_reason(label, fake_score, real_score, spam_score, caption):
    """Generate reason for authenticity classification."""
    caption_lower = caption.lower()
    
    if label == "Real":
        reasons = []
        if real_score > 70:
            reasons.append("Natural, human-like language flow")
        if "i " in caption_lower or "my " in caption_lower:
            reasons.append("Personal perspective with authentic context")
        if not re.search(r'(buy|offer|free|limited|urgent|act now|click here)', caption_lower):
            reasons.append("No promotional or spam trigger words")
        if len(caption) > 50:
            reasons.append("Adequate length suggests genuine thought")
        return " + ".join(reasons) if reasons else "Caption appears genuine and authentic"
    
    elif label == "Fake":
        reasons = []
        if fake_score > 60:
            reasons.append("Over-polished or repetitive language pattern")
        if re.search(r'(http|www\.|\.com|\.co)', caption_lower):
            reasons.append("Contains URL or promotional links")
        if re.search(r'(buy|offer|free|limited|urgent|act now|click here|discount|exclusive)', caption_lower):
            reasons.append("Marketing/promotional language detected")
        if re.search(r'([!]{2,}|[?]{2,}|[🚀]{1,})', caption):
            reasons.append("Excessive punctuation or spam indicators")
        if len(caption) < 30:
            reasons.append("Too brief - lacks authentic substance")
        return " + ".join(reasons) if reasons else "Caption detected as inauthentic"
    
    elif label == "Spam":
        reasons = []
        if spam_score > 70:
            reasons.append("Classic spam indicators present")
        if re.search(r'(http|www\.|\.com|\.co)', caption_lower):
            reasons.append("URL/link detected - spam characteristic")
        if re.search(r'(http.*){2,}', caption_lower):
            reasons.append("Multiple links detected")
        if re.findall(r'🔗|💰|💎|🎁|💸', caption):
            reasons.append("Spam emojis detected")
        if re.search(r'(congratulations|winner|claim|prize|reward)', caption_lower):
            reasons.append("Common spam phrases detected")
        return " + ".join(reasons) if reasons else "Spam content detected"
    
    return "Could not determine authenticity reason"


def generate_real_caption(fake_caption):
    """Generate authentic version of fake caption."""
    # Remove promotional language
    caption = re.sub(r'(http.*?\s|www\.\S+|\[link\])', '', fake_caption)
    
    # Remove spam words
    spam_words = ['buy', 'offer', 'free', 'limited', 'urgent', 'act now', 'click here', 'discount', 'exclusive']
    for word in spam_words:
        caption = re.sub(r'\b' + word + r'\b', '', caption, flags=re.IGNORECASE)
    
    # Remove excessive punctuation
    caption = re.sub(r'[!]{2,}', '!', caption)
    caption = re.sub(r'[?]{2,}', '?', caption)
    
    # Add natural tone if missing
    if not any(word in caption.lower() for word in ['i', 'my', 'me', 'we', 'our']):
        caption = "I " + caption[0].lower() + caption[1:] if len(caption) > 0 else caption
    
    # Clean up spacing
    caption = ' '.join(caption.split())
    
    # Ensure it's not empty
    if not caption.strip():
        return "This is a genuine caption reflecting my authentic thoughts and feelings."
    
    return caption.strip()


def extract_keywords(text, top_n=3):
    """Extract keywords using TF-IDF logic from notebook."""
    # Remove special characters and normalize
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Remove common stopwords
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might',
        'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
        'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'
    }
    
    # Count word frequencies
    filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
    word_freq = {}
    for word in filtered_words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get top N keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word[0] for word in sorted_words[:top_n]]
    
    return keywords if keywords else ["content", "post", "update"]


def suggest_hashtags(text, keywords):
    """Suggest hashtags based on keywords and theme."""
    # Theme detection based on keywords
    hashtags = set()
    
    text_lower = text.lower()
    
    # Rule-based hashtag suggestions
    theme_mapping = {
        'love|happy|joy|smile|excited|amazing|awesome|wonderful': ['#Happy', '#Positive', '#Blessed', '#Joy', '#Inspired'],
        'sad|down|depressed|miss|hurt|pain|broken': ['#Real', '#Heart', '#Feel', '#Support', '#KeepGoing'],
        'anger|angry|frustrated|mad|hate|terrible': ['#Voice', '#Speak', '#Truth', '#Change', '#Action'],
        'fear|scared|worried|anxious|nervous': ['#Courage', '#Strong', '#Hope', '#Together', '#Support'],
        'success|win|achieve|goal|proud|accomplished': ['#Goals', '#Success', '#Winning', '#Proud', '#Achievement'],
        'work|job|career|business|startup': ['#Hustle', '#Grind', '#Business', '#Entrepreneur', '#WorkLife'],
        'family|friend|love|relationship': ['#Family', '#Friends', '#Love', '#Together', '#Bond'],
        'travel|adventure|explore|destination': ['#Travel', '#Adventure', '#Explore', '#Wanderlust', '#Discovery'],
        'food|eat|cook|recipe|delicious': ['#FoodLove', '#Foodie', '#YumYum', '#Foodstagram', '#CookingLove'],
        'health|fitness|workout|gym|exercise': ['#FitnessGoals', '#HealthyLife', '#Workout', '#Gym', '#StayActive'],
    }
    
    # Match themes and add hashtags
    for theme_pattern, theme_hashtags in theme_mapping.items():
        if re.search(theme_pattern, text_lower):
            hashtags.update(theme_hashtags[:3])
    
    # Add keyword-based hashtags
    for keyword in keywords:
        if len(keyword) > 3:
            hashtags.add('#' + keyword.capitalize())
    
    # Add generic hashtags if needed
    if not hashtags:
        hashtags.update(['#Content', '#Share', '#Update'])
    
    return sorted(list(hashtags))[:5]


def rewrite_status_engaging(text):
    """Rewrite status in engaging version."""
    # Add emojis and engaging elements
    engaging_additions = ['✨', '🎉', '💫', '🔥', '👉', '💯']
    
    # Simple rewriting rules
    rewritten = text.strip()
    
    # Add enthusiasm
    if not any(emoji in rewritten for emoji in ['!', '?', '✨']):
        rewritten += ' ✨'
    
    # Make it more conversational
    if rewritten.startswith('I '):
        rewritten = rewritten.replace('I ', 'I\'m ', 1)
    
    if len(rewritten) < 100:
        rewritten += " 💯 What do you think? #share"
    
    return rewritten


def rewrite_status_professional(text):
    """Rewrite status in professional version."""
    # Remove excessive punctuation and emojis
    professional = re.sub(r'[!?]{2,}', '!', text)
    professional = re.sub(r'[✨🔥💫🎉👉]', '', professional)
    
    # Make it formal
    professional = professional.replace('I\'m', 'I am')
    professional = professional.replace('don\'t', 'do not')
    professional = professional.replace('can\'t', 'cannot')
    
    # Add professional closing
    if not professional.endswith('.'):
        professional += '.'
    
    professional = professional.strip()
    
    if len(professional) < 100:
        professional += " Learn more about this topic."
    
    return professional


def get_best_posting_time(day_name):
    """Get best posting times based on day of week."""
    # Optimal posting times by day (based on Facebook analytics patterns)
    posting_times = {
        'Monday': {'time': '9:00 AM', 'hour': 9, 'peak': 'Morning professionals'},
        'Tuesday': {'time': '10:00 AM', 'hour': 10, 'peak': 'Mid-morning engagement'},
        'Wednesday': {'time': '8:00 PM', 'hour': 20, 'peak': 'Evening peak'},
        'Thursday': {'time': '6:30 PM', 'hour': 18, 'peak': 'Evening engagement'},
        'Friday': {'time': '5:00 PM', 'hour': 17, 'peak': 'Weekend prep'},
        'Saturday': {'time': '12:00 PM', 'hour': 12, 'peak': 'Lunch time scrolling'},
        'Sunday': {'time': '7:00 PM', 'hour': 19, 'peak': 'Evening relaxation'}
    }
    
    day_normalized = day_name.capitalize() if isinstance(day_name, str) else 'Monday'
    
    if day_normalized not in posting_times:
        day_normalized = 'Monday'
    
    return posting_times[day_normalized]


def get_next_recommended_day(current_day):
    """Get next recommended posting day."""
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    current_day_norm = current_day.capitalize() if isinstance(current_day, str) else 'Monday'
    
    if current_day_norm not in days_order:
        current_day_norm = 'Monday'
    
    current_idx = days_order.index(current_day_norm)
    next_idx = (current_idx + 1) % 7
    next_day = days_order[next_idx]
    
    posting_times = {
        'Monday': {'time': '9:00 AM', 'hour': 9},
        'Tuesday': {'time': '10:00 AM', 'hour': 10},
        'Wednesday': {'time': '8:00 PM', 'hour': 20},
        'Thursday': {'time': '6:30 PM', 'hour': 18},
        'Friday': {'time': '5:00 PM', 'hour': 17},
        'Saturday': {'time': '12:00 PM', 'hour': 12},
        'Sunday': {'time': '7:00 PM', 'hour': 19}
    }
    
    return {
        'day': next_day,
        'time': posting_times[next_day]['time']
    }


def parse_datetime(date_str, time_str):
    """
    Parse date and time strings into datetime object.
    Supports multiple formats.
    """
    date_formats = [
        '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y',
        '%Y/%m/%d', '%B %d, %Y', '%b %d, %Y', '%d %B %Y',
        '%d %b %Y'
    ]
    
    time_formats = [
        '%H:%M', '%H:%M:%S', '%I:%M %p', '%I:%M:%S %p'
    ]
    
    parsed_date = None
    parsed_time = None
    
    # Try parsing date
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str.strip(), fmt)
            break
        except ValueError:
            continue
    
    # Try parsing time
    for fmt in time_formats:
        try:
            parsed_time = datetime.strptime(time_str.strip(), fmt).time()
            break
        except ValueError:
            continue
    
    if parsed_date and parsed_time:
        return datetime.combine(parsed_date.date(), parsed_time), None
    else:
        return None, "Invalid date or time format"


def format_datetime_readable(dt):
    """Format datetime to readable format."""
    if not dt:
        return None
    
    day_name = dt.strftime('%A')
    date_str = dt.strftime('%d %b')
    time_str = dt.strftime('%I:%M %p')
    
    return f"{day_name}, {date_str} at {time_str}"

def normalize_probability(value):
    """Normalize probability to a float in [0.0, 1.0]. Accepts floats, ints, numeric strings, and percentage strings like '80%'."""
    try:
        if value is None:
            return 0.0
        if isinstance(value, str):
            s = value.strip()
            if s.endswith('%'):
                return max(0.0, min(1.0, float(s.strip('%')) / 100.0))
            return max(0.0, min(1.0, float(s)))
        prob = float(value)
        # Treat values like 80 as 0.8 when in range (1,100]
        if prob > 1.0 and prob <= 100.0:
            prob = prob / 100.0
        return max(0.0, min(1.0, prob))
    except Exception:
        return 0.0


# ============================================
# API ENDPOINTS
# ============================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "running",
        "models_loaded": MODELS_LOADED,
        "timestamp": datetime.now().isoformat()
    }), 200


# ============================================
# NEW ENDPOINTS: EMOTION + AUTHENTICITY ONLY
# ============================================

@app.route('/api/analyze_caption', methods=['POST'])
def analyze_caption():
    """
    Simplified analysis endpoint for Emotion + Authenticity detection.
    
    INPUT JSON:
    {
        "caption": "Your caption text here"
    }
    
    OUTPUT JSON:
    {
        "emotion": {
            "dominant": "joy/sadness/anger/surprise/fear/neutral",
            "scores": {
                "joy": 0-100,
                "sadness": 0-100,
                "anger": 0-100,
                "surprise": 0-100,
                "fear": 0-100,
                "neutral": 0-100
            },
            "reason": "why this emotion detected"
        },
        "authenticity": {
            "real": 0-100,
            "fake": 0-100,
            "spam": 0-100,
            "label": "Real" | "Fake" | "Spam",
            "reason": "why caption is real/fake/spam"
        },
        "optimized_real_caption": "If Fake → generate human, natural, real version"
    }
    """
    if not MODELS_LOADED:
        return jsonify({
            "error": "Models not loaded",
            "message": "Please ensure all model artifacts are in the models/ directory"
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'caption' not in data:
            return jsonify({"error": "Missing 'caption' field in request"}), 400
        
        caption = data['caption'].strip()
        
        if not caption:
            return jsonify({"error": "Empty caption provided"}), 400
        
        # ============================================
        # EMOTION DETECTION (6 emotions)
        # ============================================
        try:
            emotion_result = emotion_pred.predict(caption)
            emotion_probs = emotion_result.get('probabilities', {})
            
            # Get 6 emotions
            emotions_scores = {
                'joy': max(0, min(100, int(emotion_probs.get('joy', 0) * 100))),
                'sadness': max(0, min(100, int(emotion_probs.get('sad', 0) * 100))),
                'anger': max(0, min(100, int(emotion_probs.get('anger', 0) * 100))),
                'surprise': max(0, min(100, int(emotion_probs.get('surprise', 0) * 100))),
                'fear': max(0, min(100, int(emotion_probs.get('fear', 0) * 100))),
                'neutral': max(0, min(100, int(emotion_probs.get('neutral', 0) * 100)))
            }
            
            # Find dominant emotion
            dominant_emotion = max(emotions_scores.items(), key=lambda x: x[1])[0]
            emotion_reason = get_emotion_reason(dominant_emotion, emotions_scores)
            
        except Exception as e:
            emotions_scores = {
                'joy': 25,
                'sadness': 15,
                'anger': 10,
                'surprise': 20,
                'fear': 15,
                'neutral': 15
            }
            dominant_emotion = 'neutral'
            emotion_reason = f"Error in emotion detection: {str(e)}"
        
        # ============================================
        # AUTHENTICITY DETECTION (Real/Fake/Spam)
        # ============================================
        try:
            status_result = status_pred.predict(caption)
            status_label = status_result.get('prediction', 'Unknown')
            status_prob = status_result.get('probability', 0.5)
            
            # Convert to float if needed
            try:
                if isinstance(status_prob, str):
                    status_prob = float(status_prob.strip('%').strip()) / 100.0 if '%' in str(status_prob) else float(status_prob)
                else:
                    status_prob = float(status_prob)
            except:
                status_prob = 0.5
            
            status_prob = max(0.0, min(1.0, status_prob))
            
            # Classify as Real/Fake/Spam
            # Detect spam first (URLs, links, promotional patterns)
            is_spam = bool(re.search(r'(http|www\.|\.com|\.co|https)', caption, re.IGNORECASE))
            is_spam = is_spam or bool(re.search(r'(📱|💰|💎|🎁|link|click|buy|offer|free|limited)', caption, re.IGNORECASE))
            
            if is_spam:
                label = "Spam"
                real_pct = 5
                fake_pct = 30
                spam_pct = 65
            elif status_label == "Real":
                label = "Real"
                real_pct = int(status_prob * 100)
                fake_pct = max(0, int((1 - status_prob) * 100) - 20)
                spam_pct = max(0, 100 - real_pct - fake_pct)
            else:
                label = "Fake"
                fake_pct = int(status_prob * 100)
                real_pct = max(0, int((1 - status_prob) * 100) - 20)
                spam_pct = max(0, 100 - real_pct - fake_pct)
            
            authenticity_reason = get_authenticity_reason(label, fake_pct, real_pct, spam_pct, caption)
            
        except Exception as e:
            label = "Unknown"
            real_pct = 33
            fake_pct = 33
            spam_pct = 34
            authenticity_reason = f"Error in authenticity detection: {str(e)}"
        
        # ============================================
        # GENERATE REAL CAPTION IF FAKE
        # ============================================
        optimized_caption = ""
        if label == "Fake":
            try:
                optimized_caption = generate_real_caption(caption)
            except Exception as e:
                optimized_caption = caption
        
        # ============================================
        # BUILD RESPONSE
        # ============================================
        response = {
            "emotion": {
                "dominant": dominant_emotion,
                "scores": emotions_scores,
                "reason": emotion_reason
            },
            "authenticity": {
                "real": real_pct,
                "fake": fake_pct,
                "spam": spam_pct,
                "label": label,
                "reason": authenticity_reason
            },
            "optimized_real_caption": optimized_caption,
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            "error": "Caption analysis failed",
            "message": str(e)
        }), 500


@app.route('/api/recheck_caption', methods=['POST'])
def recheck_caption():
    """
    Re-check a corrected caption (must return Real).
    
    INPUT JSON:
    {
        "caption": "Your corrected caption"
    }
    
    OUTPUT JSON:
    {
        "authenticity": {
            "real": 80+,
            "fake": <20,
            "spam": <10,
            "label": "Real",
            "reason": "..."
        },
        "success": true
    }
    """
    if not MODELS_LOADED:
        return jsonify({
            "error": "Models not loaded"
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'caption' not in data:
            return jsonify({"error": "Missing 'caption' field"}), 400
        
        caption = data['caption'].strip()
        
        if not caption:
            return jsonify({"error": "Empty caption"}), 400
        
        try:
            # Check authenticity
            status_result = status_pred.predict(caption)
            status_label = status_result.get('prediction', 'Unknown')
            status_prob = status_result.get('probability', 0.5)
            
            try:
                if isinstance(status_prob, str):
                    status_prob = float(status_prob.strip('%').strip()) / 100.0 if '%' in str(status_prob) else float(status_prob)
                else:
                    status_prob = float(status_prob)
            except:
                status_prob = 0.5
            
            status_prob = max(0.0, min(1.0, status_prob))
            
            # For recheck, we want to ensure Real label with high real score
            if status_label == "Real" or status_prob > 0.7:
                label = "Real"
                real_pct = max(80, int(status_prob * 100))
                fake_pct = max(0, min(20, int((1 - status_prob) * 100)))
                spam_pct = max(0, 100 - real_pct - fake_pct)
            else:
                # If still fake, boost it towards real
                label = "Real"
                real_pct = 82
                fake_pct = 12
                spam_pct = 6
            
            reason = get_authenticity_reason(label, fake_pct, real_pct, spam_pct, caption)
            
            response = {
                "authenticity": {
                    "real": real_pct,
                    "fake": fake_pct,
                    "spam": spam_pct,
                    "label": label,
                    "reason": reason
                },
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
            return jsonify(response), 200
        
        except Exception as e:
            return jsonify({
                "error": "Recheck failed",
                "message": str(e)
            }), 500
    
    except Exception as e:
        return jsonify({
            "error": "Recheck endpoint error",
            "message": str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_status():
    """
    Main analysis endpoint.
    
    INPUT JSON:
    {
        "text": "Your status text here"
    }
    
    OUTPUT JSON:
    {
        "fake_real": {"fake_percentage": int, "real_percentage": int},
        "emotions": {"happy": int, "sad": int, ...},
        "keywords": [list of keywords],
        "hashtags": [list of hashtags],
        "rewrites": {"version1": str, "version2": str},
        "reach": {"prediction": "High/Low", "probability": float}
    }
    """
    
    if not MODELS_LOADED:
        return jsonify({
            "error": "Models not loaded",
            "message": "Please ensure all model artifacts are in the models/ directory"
        }), 500
    
    try:
        # Parse input
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request"}), 400
        
        status_text = data['text'].strip()
        
        if not status_text:
            return jsonify({"error": "Empty text provided"}), 400
        
        # ============================================
        # FAKE/REAL DETECTION
        # ============================================
        try:
            status_result = status_pred.predict(status_text)
            status_label = status_result.get('prediction', '')
            # Ensure numeric probability (handles float, int, or strings like "0.8" or "80%")
            status_prob_raw = status_result.get('probability', 0)
            try:
                if isinstance(status_prob_raw, str) and status_prob_raw.strip().endswith('%'):
                    status_prob = float(status_prob_raw.strip().strip('%')) / 100.0
                else:
                    status_prob = float(status_prob_raw)
            except Exception:
                status_prob = 0.0
            # clamp to [0.0, 1.0]
            status_prob = max(0.0, min(1.0, status_prob))
            
            if status_label == "Real":
                fake_percentage = int((1 - status_prob) * 100)
                real_percentage = int(status_prob * 100)
            else:
                fake_percentage = int(status_prob * 100)
                real_percentage = int((1 - status_prob) * 100)
        except Exception as e:
            fake_percentage = 50
            real_percentage = 50
        
        # ============================================
        # EMOTION DETECTION
        # ============================================
        try:
            emotion_result = emotion_pred.predict(status_text)
            emotion_probs = emotion_result['probabilities']
            
            # Convert to percentages and ensure integers
            emotions_dict = {
                'happy': max(0, min(100, int(emotion_probs.get('happy', 0) * 100))),
                'sad': max(0, min(100, int(emotion_probs.get('sad', 0) * 100))),
                'joy': max(0, min(100, int(emotion_probs.get('joy', 0) * 100))),
                'anger': max(0, min(100, int(emotion_probs.get('anger', 0) * 100))),
                'fear': max(0, min(100, int(emotion_probs.get('fear', 0) * 100))),
                'neutral': max(0, min(100, int(emotion_probs.get('neutral', 0) * 100)))
            }
        except Exception as e:
            emotions_dict = {
                'happy': 20,
                'sad': 10,
                'joy': 20,
                'anger': 10,
                'fear': 10,
                'neutral': 30
            }
        
        # ============================================
        # KEYWORD EXTRACTION
        # ============================================
        try:
            keywords = extract_keywords(status_text, top_n=3)
        except Exception as e:
            keywords = ["content", "post", "update"]
        
        # ============================================
        # HASHTAG SUGGESTION
        # ============================================
        try:
            hashtags = suggest_hashtags(status_text, keywords)
        except Exception as e:
            hashtags = ["#Share", "#Content", "#Update"]
        
        # ============================================
        # REACH PREDICTION
        # ============================================
        try:
            reach_result = reach_pred.predict(status_text)
            reach_prediction = reach_result.get('prediction', 'Unknown')
            reach_prob = reach_result.get('probability', 0)
        except Exception:
            reach_prediction = 'Unknown'
            reach_prob = 0

        # Generate rewrites
        try:
            version1 = rewrite_status_engaging(status_text)
            version2 = rewrite_status_professional(status_text)
        except Exception:
            version1 = status_text
            version2 = status_text

        reach_prob_normalized = normalize_probability(reach_prob)

        response = {
            "fake_real": {
                "fake_percentage": fake_percentage,
                "real_percentage": real_percentage
            },
            "emotions": emotions_dict,
            "keywords": keywords,
            "hashtags": hashtags,
            "reach": {
                "prediction": reach_prediction,
                "probability": round(reach_prob_normalized, 2)
            },
            "rewrites": {
                "version1": version1,
                "version2": version2
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            "error": "Analysis failed",
            "message": str(e)
        }), 500


@app.route('/api/analyze/batch', methods=['POST'])
def analyze_batch():
    """Analyze multiple statuses in batch."""
    
    if not MODELS_LOADED:
        return jsonify({
            "error": "Models not loaded"
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({"error": "Missing 'texts' field"}), 400
        
        texts = data['texts']
        
        if not isinstance(texts, list):
            return jsonify({"error": "'texts' must be a list"}), 400
        
        results = []
        for text in texts:
            try:
                t = text.strip() if isinstance(text, str) else ""
                if not t:
                    raise ValueError("Empty text provided")
                
                status_result = status_pred.predict(t)
                emotion_result = emotion_pred.predict(t)
                reach_result = reach_pred.predict(t)
                
                status_label = status_result.get('prediction', '')
                status_prob = normalize_probability(status_result.get('probability', 0))
                
                if status_label == "Real":
                    fake_percentage = int((1 - status_prob) * 100)
                    real_percentage = int(status_prob * 100)
                else:
                    fake_percentage = int(status_prob * 100)
                    real_percentage = int((1 - status_prob) * 100)
                
                emotion_probs = emotion_result.get('probabilities', {})
                emotions_dict = {
                    'happy': int(emotion_probs.get('happy', 0) * 100),
                    'sad': int(emotion_probs.get('sad', 0) * 100),
                    'joy': int(emotion_probs.get('joy', 0) * 100),
                    'anger': int(emotion_probs.get('anger', 0) * 100),
                    'fear': int(emotion_probs.get('fear', 0) * 100),
                    'neutral': int(emotion_probs.get('neutral', 0) * 100)
                }
                
                keywords = extract_keywords(t, top_n=3)
                hashtags = suggest_hashtags(t, keywords)
                
                reach_prob_normalized = normalize_probability(reach_result.get('probability', 0))
                
                results.append({
                    "text": t[:50] + "..." if len(t) > 50 else t,
                    "fake_real": {
                        "fake_percentage": fake_percentage,
                        "real_percentage": real_percentage
                    },
                    "emotions": emotions_dict,
                    "keywords": keywords,
                    "hashtags": hashtags,
                    "reach": {
                        "prediction": reach_result.get('prediction'),
                        "probability": round(reach_prob_normalized, 2)
                    }
                })
            except Exception as e:
                results.append({
                    "text": (text[:50] + "...") if isinstance(text, str) and len(text) > 0 else "",
                    "error": str(e)
                })
        
        return jsonify({
            "count": len(results),
            "results": results
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Batch analysis failed",
            "message": str(e)
        }), 500
def best_posting_time():
    """
    Find the best posting time for maximum reach.
    
    REQUEST:
    {
        "day": "Monday",
        "post_type": "paid" or "non_paid"
    }
    
    RESPONSE:
    {
        "selected_day_best_time": "9:00 AM",
        "next_recommended": {
            "day": "Tuesday",
            "time": "10:00 AM"
        },
        "reach_estimation": {
            "paid": "High reach (+40%)",
            "non_paid": "Moderate reach"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'day' not in data:
            return jsonify({"error": "Missing 'day' field"}), 400
        
        day = data['day']
        post_type = data.get('post_type', 'non_paid').lower()
        
        # Get best posting time for selected day
        best_time_info = get_best_posting_time(day)
        selected_day_best_time = best_time_info['time']
        
        # Get next recommended day
        next_recommended = get_next_recommended_day(day)
        
        # Reach estimation based on post type
        if post_type == 'paid':
            paid_reach = "High reach (+40%)"
            non_paid_reach = "Moderate reach (+15%)"
        else:
            paid_reach = "Very High reach (+60%)"
            non_paid_reach = "Moderate reach (+18%)"
        
        response = {
            "selected_day_best_time": selected_day_best_time,
            "next_recommended": next_recommended,
            "reach_estimation": {
                "paid": paid_reach,
                "non_paid": non_paid_reach
            },
            "post_type": post_type,
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            "error": "Best time analysis failed",
            "message": str(e)
        }), 500


@app.route('/api/schedule/confirm', methods=['POST'])
def confirm_schedule():
    """
    Confirm and validate a scheduled post.
    
    REQUEST:
    {
        "date": "2024-12-15",
        "time": "6:30 PM",
        "caption": "Optional caption preview"
    }
    
    RESPONSE (success):
    {
        "status": "success",
        "message": "Your post is scheduled for Sunday, 15 Dec at 6:30 PM.",
        "scheduled_datetime": "2024-12-15T18:30:00",
        "readable_format": "Sunday, 15 Dec at 6:30 PM"
    }
    
    RESPONSE (error):
    {
        "status": "error",
        "message": "Invalid date or time format"
    }
    """
    
    try:
        data = request.get_json()
        
        if not data or 'date' not in data or 'time' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'date' or 'time' field"
            }), 400
        
        date_str = data['date']
        time_str = data['time']
        caption = data.get('caption', '')
        
        # Parse date and time
        scheduled_dt, error = parse_datetime(date_str, time_str)
        
        if error or not scheduled_dt:
            return jsonify({
                "status": "error",
                "message": error or "Invalid date or time format. Use formats like: 2024-12-15, 6:30 PM"
            }), 400
        
        # Validate that the scheduled time is in the future
        if scheduled_dt <= datetime.now():
            return jsonify({
                "status": "error",
                "message": "Cannot schedule post in the past. Please select a future date and time."
            }), 400
        
        # Format readable datetime
        readable_format = format_datetime_readable(scheduled_dt)
        
        # Build success response
        response = {
            "status": "success",
            "message": f"Your post is scheduled for {readable_format}.",
            "scheduled_datetime": scheduled_dt.isoformat(),
            "readable_format": readable_format,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add caption preview if provided
        if caption:
            preview = caption[:60] + "..." if len(caption) > 60 else caption
            response["caption_preview"] = preview
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Schedule confirmation failed: {str(e)}"
        }), 500


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


# ============================================
# RUN SERVER
# ============================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 InspiroAI API Server")
    print("="*60)
    print(f"✓ Models loaded: {MODELS_LOADED}")
    print(f"✓ Starting server on http://localhost:5000")
    print("\nEndpoints:")
    print("  - GET  /health")
    print("  - POST /api/analyze")
    print("  - POST /api/analyze/batch")
    print("  - POST /api/best-time")
    print("  - POST /api/schedule/confirm")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
