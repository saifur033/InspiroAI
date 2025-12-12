# InspiroAI - AI-Based Caption Optimization & Facebook Auto-Posting System

**An intelligent Streamlit application for optimizing Facebook captions using Machine Learning**

---

## 📋 Overview

InspiroAI is a comprehensive solution for content creators and social media managers to:
- Analyze caption quality (Fake/Real detection)
- Predict optimal posting times using ML models
- Automatically schedule and post to Facebook
- Detect emotions in captions and track engagement

**Developed for:** EWU CSE Capstone Project  
**Supervisor:** Dr. Anisur Rahman  
**Team:** Saifur Rahman, Mumtahina, Arpita, Ishrmat  
**Status:** Production Ready ✅

---

## ✨ Features

### Tab 1: Status Analyzer
- **Fake/Real Detection** - Identifies suspicious or fake captions
- **Emotion Analysis** - Detects 6 emotions: Anger, Fear, Joy, Neutral, Sadness, Surprise
- **Confidence Scores** - Shows probability for each prediction
- **Improvement Tips** - Suggestions for fake captions

### Tab 2: Post Reach Optimizer
- **Best Time Prediction** - Analyzes all 24 hours for optimal posting time
- **ML-Based Reach Scoring** - Ensemble model predicting engagement
- **Day-Specific Analysis** - Different recommendations for different days

### Tab 3: Schedule Post
- **Auto-Scheduling** - Schedule posts for future dates/times
- **Countdown Timer** - Track time until auto-posting
- **Persistent Storage** - Posts remain saved across sessions
- **Auto-Posting** - Posts automatically publish at scheduled time

---

## 🔧 Technical Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit 1.52.1 |
| **Backend** | Python 3.13 |
| **ML Framework** | Scikit-learn, XGBoost, LightGBM |
| **Embeddings** | Sentence-Transformers (all-MiniLM-L6-v2) |
| **API** | Facebook Graph API v18.0 |
| **Storage** | JSON (Local) |
| **Version Control** | Git |

---

## 🤖 Machine Learning Models

### Models Used

| Task | Model | Accuracy |
|------|-------|----------|
| Fake/Real Detection | Random Forest | ~85% |
| Emotion Detection | DistilRoBERTa | Pretrained |
| Reach Prediction | Ensemble (SVM+XGBoost+RF) | 0.65-0.75 R² |
| Text Embeddings | all-MiniLM-L6-v2 | 384-dimensional |

### Feature Engineering

**Text Features:**
- Character count, Word count, Average word length
- Emoji count, Hashtag presence, Readability grade

**Time Features:**
- Hour encoding (Sin/Cos transformation)
- Day of week encoding (Sin/Cos transformation)
- Weekend flag

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.10+
- pip or conda
- Facebook Developer Account

### Step 1: Clone Repository
```bash
git clone https://github.com/saifur033/InspiroAI.git
cd InspiroAI
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Get Facebook Credentials
1. Go to [Meta Developer](https://developers.facebook.com/)
2. Create an app and get:
   - **Facebook API Token**
   - **Facebook Page ID**

### Step 4: Run Application
```bash
cd production
streamlit run app.py
```

App will be available at: `http://localhost:8501`

---

## 📖 Usage Guide

### Tab 1: Status Analyzer
1. Enter your caption in the text area
2. Click "Analyze" button
3. View results:
   - Real/Fake classification
   - Emotion breakdown
   - Confidence scores

### Tab 2: Post Reach Optimizer
1. Enter caption text
2. Select desired day (Monday-Sunday)
3. Click "Suggest Best Time"
4. View predicted reach score for best posting time

### Tab 3: Schedule Post
1. Enter caption
2. Select date and time
3. Click "Schedule"
4. Post will auto-post at scheduled time
5. Track pending posts with countdown timer

---

## 📁 Project Structure

```
InspiroAI/
├── production/
│   ├── app.py                 # Main Streamlit application
│   ├── config.py              # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── models/                # Trained ML models
│   │   ├── status_rf.joblib
│   │   ├── status_xgb.joblib
│   │   ├── reach_voting.joblib
│   │   └── ...
│   └── utils/
│       ├── inference.py       # Model prediction functions
│       ├── feature_engineering.py
│       ├── facebook_posting.py
│       ├── post_storage.py    # Persistent storage
│       └── ...
├── Notebbok/                  # Jupyter notebooks for training
│   ├── EMOTION_DETECTION_cap_C.ipynb
│   ├── reach_prediction_cap_C_final.ipynb
│   └── status_final_cap_C.ipynb
├── README.md                  # This file
├── requirements.txt           # Root dependencies
└── .gitignore
```

---

## 🎯 Key Features Explained

### 1. Persistent Storage
- Scheduled posts saved to `scheduled_posts.json`
- Posts persist across app restarts
- Auto-posting checks every render cycle

### 2. Model Ensemble
- 3 independent models for reach prediction
- Voting mechanism for better accuracy
- Reduces false positives/negatives

### 3. Auto-Posting Logic
```
1. App loads scheduled posts from JSON
2. Every render checks: is scheduled_dt <= now?
3. If yes → posts via Facebook API
4. Updates status: Pending → Posted
5. Saves to JSON file
6. Refreshes UI
```

### 4. Feature Encoding
- **Sin/Cos Encoding** for hours (circular nature)
- **Sparse Matrix** for embeddings + features
- **Scaling** for numeric features

---

## ⚙️ Configuration

### Facebook API Setup
1. Create `.env` file (optional):
```
FACEBOOK_TOKEN=your_token_here
FACEBOOK_PAGE_ID=your_page_id
```

2. Or use Sidebar in app to enter credentials

### Model Parameters
Edit `production/config.py`:
```python
REACH_THRESHOLD = 0.40
STATUS_THRESHOLD = 0.55
MAX_CAPTION_LENGTH = 512
```

---

## 🧪 Testing

### Manual Testing
1. Start app: `streamlit run app.py`
2. Test each tab with sample captions
3. Verify auto-posting with scheduled posts

**Example Test Captions:**

**FAKE Detection:**
```
Check this amazing opportunity! Don't miss out! 
Click here for FREE money! Limited time offer!
Act now before it's gone! #opportunity #money
```

**REAL Detection:**
```
honestly i still can't believe i graduated lol
spent 4 years and still don't know what i'm doing
grateful for the people who kept me sane
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Status Detection Accuracy | ~85% |
| Emotion Detection Accuracy | 85-90% |
| Reach Prediction R² | 0.65-0.75 |
| Model Loading Time | ~5-10 seconds |
| Prediction Time (per caption) | <100ms |

---

## 🔒 Security & Privacy

- **No Cloud Storage** - Data stored locally only
- **No Data Logging** - Posts not logged anywhere
- **Credentials Temporary** - Session-based, not saved
- **Clear Button** - Remove credentials anytime
- **HTTPS Only** - Facebook API uses HTTPS

---

## 🚧 Known Limitations

1. **Reach Prediction**: Medium accuracy (varies by account size)
2. **English Only**: No multi-language support yet
3. **Text Only**: Image/video analysis not included
4. **Account Specific**: Models trained on specific data
5. **Manual Training**: Requires retraining for new accounts

---

## 🚀 Future Enhancements

- [ ] Multi-language support (Bengali, Hindi, etc.)
- [ ] Image/Video content analysis
- [ ] User-specific personalized models
- [ ] Analytics dashboard
- [ ] A/B testing suggestions
- [ ] Batch posting
- [ ] Database integration (PostgreSQL)
- [ ] Cloud deployment (Streamlit Cloud/Heroku)

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open Pull Request

---

## 📝 License

This project is part of an academic capstone project. For usage rights, contact the team.

---

## 👥 Team Members

- **Saifur Rahman** - Lead Developer
- **Mumtahina** - ML Engineer
- **Arpita** - Frontend Developer
- **Ishrmat** - Testing & Documentation

**Supervisor:** Dr. Anisur Rahman  
**Institution:** East West University, Dhaka, Bangladesh

---

## 📞 Support & Contact

- **GitHub Issues:** [Report bugs here](https://github.com/saifur033/InspiroAI/issues)
- **Email:** saifur033@gmail.com
- **Documentation:** See `production/` folder for detailed docs

---

## 🎓 Academic Context

**Capstone Project:** InspiroAI - Context-Aware Facebook Caption Optimization System  
**Course:** CSE Capstone Project  
**University:** East West University  
**Semester:** Fall 2024 - Spring 2025

---

**Last Updated:** December 12, 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅

---

## 🙏 Acknowledgments

- Meta/Facebook for Graph API
- HuggingFace for pretrained models
- Streamlit for amazing framework
- Open-source ML community

---

**Made with ❤️ for better social media content**
