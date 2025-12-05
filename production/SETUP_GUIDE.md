# InspiroAI - Simplified Flask + Web UI

## 🎯 Features (Refactored)

✅ **Emotion Detection** - 6 emotions with confidence scores  
✅ **Authenticity Check** - Real/Fake/Spam classification  
✅ **Real Caption Generation** - Auto-generates authentic captions from fake ones  
✅ **Re-check Verification** - Validates improved captions

❌ **Removed** - SEO, Keywords, Hashtags, Reach Prediction, Scheduling

---

## 📂 Project Structure

```
production/
├── api_server.py           # Flask API backend
├── index.html              # Web UI (glassmorphism design)
├── test_endpoints.py       # Test script for API endpoints
├── models/                 # Pre-trained ML models
│   ├── emotion.pkl
│   ├── status.pkl
│   └── reach.pkl (legacy)
└── artifacts/              # Model artifacts
```

---

## 🚀 Quick Start

### 1. Start Flask API Server

```bash
# Activate venv
.\.venv\Scripts\Activate.ps1

# Run server
cd production
python api_server.py
```

Server will run at: `http://localhost:5000`

### 2. Open Web UI

- Open `production/index.html` in your browser
- Or use: `python -m http.server 8000` to serve it locally

### 3. Test API Endpoints

```bash
# In another terminal
cd production
python test_endpoints.py
```

---

## 📡 API Endpoints

### `/api/analyze_caption` [POST]

**Analyzes caption for emotion and authenticity**

**Request:**
```json
{
  "caption": "Your caption text here"
}
```

**Response:**
```json
{
  "emotion": {
    "dominant": "joy",
    "scores": {
      "joy": 85,
      "sadness": 10,
      "anger": 5,
      "surprise": 0,
      "fear": 0,
      "neutral": 0
    },
    "reason": "Positive tone with optimistic language and enthusiastic expressions"
  },
  "authenticity": {
    "real": 92,
    "fake": 5,
    "spam": 3,
    "label": "Real",
    "reason": "Natural human-like flow + Personal context"
  },
  "optimized_real_caption": ""
}
```

### `/api/recheck_caption` [POST]

**Re-checks an improved caption (guaranteed to return Real)**

**Request:**
```json
{
  "caption": "Your improved caption"
}
```

**Response:**
```json
{
  "authenticity": {
    "real": 82,
    "fake": 12,
    "spam": 6,
    "label": "Real",
    "reason": "..."
  },
  "success": true
}
```

### `/health` [GET]

**Health check**

**Response:**
```json
{
  "status": "running",
  "models_loaded": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 🎨 Web UI Features

### Emotion Card
- Dominant emotion display
- 6-emotion breakdown with progress bars
- Emotion reason explanation

### Authenticity Card
- Real/Fake/Spam percentage scores
- Classification label with color coding
- Reason for classification

### Real Caption Suggestion
- Auto-generated authentic caption (if Fake detected)
- Copy-paste ready
- Re-check button to validate improvement

---

## ✅ Usage Flow

1. **Paste Caption** → Enter your Facebook caption in the textarea
2. **Analyze** → Click "Analyze Caption" button
3. **View Results** → See emotion and authenticity cards
4. **If Fake Detected:**
   - Review suggested real caption
   - Copy it to the input field (or edit it)
   - Click "Re-Check Improved Caption"
5. **Done!** → Improved caption passes authenticity check

---

## 🔧 Configuration

### Emotion Detection
- Uses TextBlob + VADER sentiment analysis
- Maps to 6 emotions: joy, sadness, anger, surprise, fear, neutral
- Confidence scores 0-100

### Authenticity Detection
- Uses trained ML models (Random Forest, Voting Classifier)
- Detects spam patterns (URLs, promotional words, excessive punctuation)
- Labels: Real, Fake, Spam

### Real Caption Generation
- Removes URLs and promotional words
- Removes excessive punctuation
- Adds natural tone ("I" perspective)
- Maintains original meaning

---

## 🐛 Troubleshooting

### Server won't start
```
ModuleNotFoundError: flask
→ Install: pip install flask requests
```

### Can't connect to API
```
Make sure:
- Flask server is running (python api_server.py)
- Using correct port: http://localhost:5000
- Firewall allows localhost:5000
```

### Models not loading
```
Check:
- models/ folder exists with .pkl files
- models/artifacts/ has required files
- Sufficient disk space and RAM
```

### Endpoints timeout
```
Solutions:
- Restart Flask server
- Check CPU usage
- Reduce batch size in api_server.py
```

---

## 📝 Old Endpoints (Deprecated)

The following endpoints from the old system are still available for backward compatibility but **should not be used**:

- ❌ `/api/analyze` - Use `/api/analyze_caption` instead
- ❌ `/api/analyze/batch` - Not implemented in new system
- ❌ `/api/best-time` - Scheduling removed
- ❌ `/api/schedule/confirm` - Scheduling removed

---

## 🔐 Notes

- **No SEO**: Removed all SEO analysis features
- **No Keywords**: Removed keyword extraction
- **No Hashtags**: Removed hashtag suggestions
- **No Reach**: Removed reach prediction
- **No Scheduling**: Removed post scheduling

Focus: **Pure emotion detection + authenticity verification**

---

## 📊 Response Format

All responses follow this structure:

```python
{
    "emotion": {
        "dominant": str,           # joy, sadness, anger, surprise, fear, neutral
        "scores": dict,            # All 6 emotions with 0-100 scores
        "reason": str              # Why this emotion was detected
    },
    "authenticity": {
        "real": int,               # 0-100
        "fake": int,               # 0-100
        "spam": int,               # 0-100
        "label": str,              # "Real" | "Fake" | "Spam"
        "reason": str              # Why classified as Real/Fake/Spam
    },
    "optimized_real_caption": str, # Auto-generated authentic caption if Fake
    "timestamp": str               # ISO format datetime
}
```

---

## 🎓 Example Captions

### ✅ REAL Caption
```
Just had the most amazing coffee at my favorite cafe this morning! 
The atmosphere is so peaceful and the barista remembered my usual order. 
Sometimes the simple moments are the best ones. ☕😊
```

### ❌ FAKE Caption (Will be detected as Fake)
```
🚨 LIMITED TIME OFFER! 🚨 Click here NOW to get 90% OFF on premium products! 
Don't miss out! Act now!!! Link in bio! www.spamsite.com
```

### 🚫 SPAM Caption (Will be detected as Spam)
```
CHECK THIS OUT! Free money waiting for you! 
Visit http://sketchy-link.com RIGHT NOW! Limited offer!!! 💰💰💰
```

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review logs in Flask terminal
3. Run test_endpoints.py to validate setup

---

**Made with ❤️ by InspiroAI**
