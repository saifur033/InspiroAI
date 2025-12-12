<p align="center">
  <h1 align="center">🔥 InspiroAI – AI-Based Caption Optimization & Facebook Auto-Posting System</h1>
  <h3 align="center">Machine Learning • Streamlit • Facebook Graph API</h3>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Project-InspiroAI-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/ML-Scikit--learn%20%7C%20XGBoost%20%7C%20LightGBM-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-Academic-lightgrey?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Emotion%20Detection-85--90%25-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Fake%2FReal%20Detection-~85%25-yellow?style=flat-square" />
  <img src="https://img.shields.io/badge/Reach%20Prediction-R²%200.65--0.75-success?style=flat-square" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Capstone-EWU%20CSE-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Supervisor-Dr.%20Anisur%20Rahman-lightgrey?style=flat-square" />
  <img src="https://img.shields.io/badge/Semester-Fall%202024--Spring%202025-purple?style=flat-square" />
</p>

---

# 📌 Overview  

**InspiroAI** is a production-ready system designed for content creators and social media managers. It provides:  
- Fake/Real caption detection  
- Emotion analysis  
- Reach prediction and optimal posting time  
- Automatic scheduled posting to Facebook  

**Capstone Project – East West University (CSE)**  
**Supervisor:** Dr. Anisur Rahman  
**Team:** Saifur Rahman, Mumtahina, Arpita, Ishrmat  

---

# ✨ Features  

## 🔹 Tab 1: Status Analyzer  
- Fake/Real detection  
- Emotion classification (Anger, Fear, Joy, Neutral, Sadness, Surprise)  
- Confidence scores  
- Improvement suggestions for fake captions  

## 🔹 Tab 2: Post Reach Optimizer  
- Predicts optimal posting times  
- ML-based reach scoring  
- Day-specific recommendations  
- Target reach auto-posting  

## 🔹 Tab 3: Schedule Post  
- Schedule future posts  
- Countdown timer  
- Persistent storage (JSON)  
- Auto-posting via Facebook API  

---

# 🔧 Technical Stack  

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit 1.52.1 |
| Backend | Python 3.13 |
| ML | Scikit-learn, XGBoost, LightGBM |
| Embeddings | Sentence-Transformers (all-MiniLM-L6-v2) |
| API | Facebook Graph API v18.0 |
| Storage | JSON |
| Version Control | Git |

---

# 🤖 Machine Learning Models  

| Task | Model | Performance |
|------|--------|-------------|
| Fake/Real Detection | Random Forest | ~85% accuracy |
| Emotion Detection | DistilRoBERTa | Pretrained |
| Reach Prediction | Ensemble (SVM + XGB + RF) | R²: 0.65–0.75 |
| Embeddings | all-MiniLM-L6-v2 | 384-dim vector |

### Feature Engineering  
- Text features: character/word count, avg word length, emoji count, hashtags, readability  
- Time features: sin/cos hour encoding, weekday encoding, weekend flag  

---

# 📦 Installation  

### 1. Clone Repository  
```bash
git clone https://github.com/saifur033/InspiroAI.git
cd InspiroAI

2. Install Dependencies
pip install -r requirements.txt
3. Configure Facebook API

Create an app → generate:

Page Access Token

Facebook Page ID

4. Run Application
cd production
streamlit run app.py
App URL: http://localhost:8501
📖 Usage Guide
✔ Status Analyzer

Enter caption → Analyze →  View Emotion and Fake or Real 

✔ Post Reach Optimizer

Caption → Select day → Suggest Best Time

✔ Schedule Post

Caption → Date + Time → Schedule → Auto-post

📁 Project Structure
InspiroAI/
├── production/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── status_rf.joblib
│   │   ├── status_xgb.joblib
│   │   ├── reach_voting.joblib
│   │   └── ...
│   └── utils/
│       ├── inference.py
│       ├── feature_engineering.py
│       ├── facebook_posting.py
│       ├── post_storage.py
│       └── ...
│
├── Notebook/
│   ├── EMOTION_DETECTION_cap_C.ipynb
│   ├── reach_prediction_cap_C_final.ipynb
│   └── status_final_cap_C.ipynb
│
├── README.md
└── requirements.txt

📊 Performance Metrics
| Metric              | Value        |
| ------------------- | ------------ |
| Fake/Real Detection | ~85%         |
| Emotion Detection   | 85–90%       |
| Reach Prediction R² | 0.65–0.75    |
| Model Load Time     | 5–10 seconds |
| Prediction Time     | <100 ms      |

🔒 Security

No cloud storage — local-only

No caption logging

Credentials temporary and session-based

HTTPS-secured API communication

🚧 Limitations

English-only captions

Reach prediction varies per Facebook page

No image/video analysis

Manual retraining required

🚀 Future Enhancements

Multi-language support

Image/video ML analysis

User-personalized models

Analytics dashboard

A/B testing

Cloud deployment

Database integration

👥 Team

Saifur Rahman 
Mumtahina 
Arpita
Ishrmat

Supervisor: Dr. Anisur Rahman
Institution: East West University
📬 Contact

Email: saifur033@gmail.com

GitHub Issues: Submit bugs & suggestions
🙏 Acknowledgments

Facebook Graph API

HuggingFace Transformers

Streamlit Community

Open-source ML ecosystem

<p align="center"><b>Made  to improve social media content</b></p>
