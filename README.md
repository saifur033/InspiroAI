# 🎓 InspiroAI - Context-Aware Facebook Caption Optimization System

> **AI-Powered Facebook Caption Analysis** with Authenticity Detection, Emotion Recognition, and Reach Optimization

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-green?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

---

## 📋 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Localhost Testing](#-localhost-testing)
- [Deployment](#-deployment)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Usage](#-usage)
- [Contributing](#-contributing)

---

## ✨ Features

### 🔍 Status Analyzer
- **Authenticity Detection**: AI detects FAKE vs REAL captions
- **Dynamic Feedback**: Different UI for FAKE vs REAL results
- **Copyable Examples**: Learn by example with proper captions
- **Emotion Recognition**: 6 emotion classes (Joy, Fear, Neutral, Anger, Surprise, Disgust)

### 💰 Post Reach Optimizer  
- **Best Time Suggestions**: Data-driven recommendations for all 7 days
- **Reach Prediction**: ML-based reach estimation
- **Auto-Share Logic**: Automatic posting when reach targets are met
- **Target Settings**: Customize minimum reach thresholds

### 📅 Schedule Post
- **Future Scheduling**: Schedule posts for specific date/time
- **Validation**: Prevents scheduling in the past
- **Facebook Integration**: Direct posting via Graph API

### 🛠️ Tools
- **Caption Generator**: AI generates authentic captions by topic
- **Caption Optimizer**: Improves existing captions
- **Hashtag Generator**: Suggests trending hashtags
- **Batch Tools**: Generate multiple variations

### 📱 Facebook Integration
- **Direct Posting**: Post captions directly to Facebook
- **Secure Credentials**: Safe token/ID storage
- **API v18.0**: Latest Facebook Graph API
- **Error Handling**: Detailed error messages

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/saifur033/InspiroAI.git
cd InspiroAI
```

### 2. Setup Virtual Environment (First Time Only)
```bash
python -m venv .venv
.venv\Scripts\activate.bat          # Windows
source .venv/bin/activate           # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Locally
```bash
cd production
python -m streamlit run app.py
```

**Open browser:** `http://localhost:8501`

### 5. Deploy to Streamlit Cloud
```bash
git push origin main
# Auto-deploys to: https://share.streamlit.io/saifur033/InspiroAI
```

---

## 🧪 Localhost Testing

### Before Deployment, Test All Features:

#### Test Checklist:
- [ ] Status Analyzer (FAKE/REAL detection)
- [ ] Emotion Detection (6 emotions)
- [ ] Reach Prediction
- [ ] Best Time Suggestions
- [ ] Schedule Post
- [ ] Caption Tools
- [ ] Facebook Posting (with credentials)
- [ ] Copyable Examples Work
- [ ] UI/UX responsive

**Detailed Guide:** See [LOCALHOST_TESTING.md](./LOCALHOST_TESTING.md)

### Example Test Captions:

**FAKE Detection:**
```
Check this amazing opportunity! Don't miss out! 
Click here for FREE money! Limited time offer!
Act now before it's gone! #opportunity #money
```
Expected: FAKE (70%+), Shows improvement tips

**REAL Detection:**
```
honestly i still can't believe i graduated lol
spent 4 years and still don't know what i'm doing
grateful for the people who kept me sane 🎓
```
Expected: REAL (20%), Celebration message

---

## 🌐 Deployment

### Option 1: Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Select repository & deploy
4. Add Facebook secrets in settings

**Deployment Status:** ✅ Ready
**App URL:** https://share.streamlit.io/saifur033/InspiroAI

### Option 2: Self-Hosted
```bash
# Install production server (optional)
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 production/app.py
```

**Full Guide:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

---

## 🏗️ Architecture

### System Components:

```
InspiroAI/
├── streamlit_app.py              # Cloud entry point
├── production/
│   ├── app.py                    # Main Streamlit UI (1200+ lines)
│   ├── utils/
│   │   ├── inference.py          # ML predictions
│   │   ├── model_loader.py       # Model registry
│   │   └── __init__.py
│   ├── models/
│   │   ├── emotion_model/        # HuggingFace DistilRoBERTa
│   │   ├── status_model.pkl      # Random Forest
│   │   ├── reach_model.pkl       # VotingClassifier
│   │   └── status_meta.json      # Threshold config
│   ├── config.py                 # Configuration
│   └── requirements.txt           # Dependencies
├── .gitignore                     # Git exclusions
└── README.md                      # This file
```

### ML Models:

| Model | Purpose | Type | Accuracy |
|-------|---------|------|----------|
| **Emotion Detector** | 6-emotion classification | HuggingFace DistilRoBERTa | 95-99% |
| **Status Detector** | FAKE/REAL detection | Random Forest + Sigmoid Calibration | 85%+ |
| **Reach Predictor** | Engagement estimation | VotingClassifier (LR+CB+XGB) | 78%+ |

### Score Distribution:

- **FAKE Captions**: 50-100% (biased language, urgency, generic)
- **REAL Captions**: 0-50% (authentic, personal, genuine)
- **Threshold**: 0.55 (balanced discrimination)

---

## 🛠️ Technologies

### Core Stack:
- **Frontend**: Streamlit 1.35+
- **Backend**: Python 3.10+
- **ML Framework**: scikit-learn, XGBoost, LightGBM, CatBoost
- **NLP**: HuggingFace Transformers, Sentence-Transformers
- **API**: Facebook Graph API v18.0
- **Deployment**: Streamlit Cloud

### Key Libraries:
```python
streamlit              # Web framework
pandas                 # Data processing
numpy                  # Numerical computing
scikit-learn          # ML algorithms
xgboost               # Gradient boosting
catboost              # Advanced boosting
lightgbm              # Light gradient boosting
torch                 # Deep learning
transformers          # NLP models
sentence-transformers # Text embeddings
requests              # HTTP client
```

---

## 📖 Usage

### 1. Analyze Caption
```
Input: Your Facebook caption
↓
Output: 
- FAKE/REAL status (%)
- 6 Emotion scores
- Why FAKE/REAL
- Improvement tips (if FAKE)
- Copyable examples
```

### 2. Optimize for Reach
```
Input: Target reach, day, post type
↓
Output:
- Best time to post
- Reach estimate
- Auto-share trigger
```

### 3. Schedule Post
```
Input: Caption, date, time
↓
Output: Scheduled for future
```

### 4. Generate Captions
```
Input: Topic (e.g., "graduation")
↓
Output: 3 authentic caption options
```

### 5. Post to Facebook
```
Input: Caption + Facebook credentials
↓
Output: Posted to page + confirmation
```

---

## 🔐 Facebook Integration

### Setup:
1. Get Facebook App ID from Meta Developer Dashboard
2. Generate Page Access Token
3. Find your Page ID (numeric)
4. Paste in sidebar or add to Streamlit secrets

### Secure Storage:
```toml
# .streamlit/secrets.toml (Streamlit Cloud)
[facebook]
api_token = "your_token"
page_id = "your_page_id"
```

### Usage:
```python
st.secrets.get("facebook", {}).get("api_token", "")
st.secrets.get("facebook", {}).get("page_id", "")
```

---

## 📊 Model Performance

### Emotion Detection:
- Trained on 16,000+ tweets
- 6 emotion classes
- Accuracy: 95-99%
- Model: DistilRoBERTa-base (66M parameters)

### Status Detection:
- Trained on 5,000+ Facebook captions
- FAKE vs REAL classification
- Accuracy: 85%+
- Calibration: Sigmoid transformation
- Threshold: 0.55 (ROC-optimized)

### Reach Prediction:
- VotingClassifier ensemble
- Components: LogisticRegression, CatBoost, XGBoost
- Predicts engagement rate
- Training data: 3,000+ posts

---

## 🤝 Contributing

### Found a bug?
1. Open an issue on GitHub
2. Describe the problem
3. Provide test case

### Want to add features?
1. Fork repository
2. Create feature branch: `git checkout -b feature/cool-feature`
3. Commit changes: `git commit -m 'Add cool feature'`
4. Push to branch: `git push origin feature/cool-feature`
5. Open pull request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💼 Author

**Saifur Rahman**
- GitHub: [@saifur033](https://github.com/saifur033)
- Email: [Your Email]

---

## 🙏 Acknowledgments

- Facebook Graph API documentation
- HuggingFace community
- Streamlit amazing framework
- All contributors and testers

---

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: [Your email]

---

## 🎯 Roadmap

### v1.1 (Next)
- [ ] Multi-language support
- [ ] Instagram integration
- [ ] Twitter/X posting
- [ ] Analytics dashboard

### v2.0 (Future)
- [ ] Mobile app
- [ ] Advanced A/B testing
- [ ] Team collaboration
- [ ] Content calendar

---

## 📈 Stats

- **Lines of Code**: 1200+
- **ML Models**: 3 (emotion, status, reach)
- **Features**: 15+
- **Test Cases**: 30+
- **Documentation**: 5+ guides
- **Deployment**: Ready for production

---

## ✅ Status

- ✅ Development: Complete
- ✅ Testing: Complete
- ✅ Documentation: Complete
- ✅ Deployment: Ready
- 🚀 Production: Ready

---

**Last Updated:** December 5, 2025  
**Version:** 1.0 Production  
**Status:** 🟢 Active & Maintained

---

## Quick Links

- 📚 [Localhost Testing Guide](./LOCALHOST_TESTING.md)
- 🚀 [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- ⚙️ [Setup Guide (Bengali)](./SETUP_BENGALI.md)
- 📖 [Full Documentation](./START_APP_GUIDE.md)
- 🔗 [GitHub Repository](https://github.com/saifur033/InspiroAI)

---

**Made with ❤️ for authentic Facebook captions**
