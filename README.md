#  InspiroAI – Context-Aware Facebbok Caption Optimization System
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

**InspiroAI** is an intelligent ML-powered system built to help content creators and social media managers evaluate and optimize Facebook captions. The system provides:

* Fake/Real caption detection
* Emotion detection across six categories
* ML-powered reach prediction and optimal posting times
* Automated scheduling and Facebook posting

**This project was developed as an academic Capstone under East West University.**

**Team:** Saifur Rahman, Mumtahina Akter, Arpita Saha , Ishmat Zaman 
**Supervisor:** Dr. Anisur Rahman, Associate Professor, Department of CSE, East West University

---

# ✨ Features

##  1. Status Analyzer

* Fake/Real classification
* Six-emotion detection: **Anger, Fear, Joy, Neutral, Sadness, Surprise**
* Confidence scores


##  2. Post Reach Optimizer

* Predicts the best posting hour for a selected day
* Ensemble ML scoring for expected reach
* “Target reach auto-posting” if score meets threshold

##  3. Schedule Post

* Schedule caption posting to Facebook
* Auto-publishing via Graph API
* Local persistent JSON storage
* Live countdown timer

---

# 🔧 Technical Stack

| Component   | Technology                               |
| ----------- | ---------------------------------------- |
| Frontend    | Streamlit 1.52.1                         |
| Backend     | Python 3.13                              |
| ML Models   | Scikit-learn, XGBoost, LightGBM          |
| Embeddings  | Sentence-Transformers (all-MiniLM-L6-v2) |
| API         | Facebook Graph API v18.0                 |
| Storage     | JSON                                     |
| Environment | Git, Virtualenv                          |

---

# 🤖 Machine Learning Models

| Task                | Model                                       | Performance     |
| ------------------- | ------------------------------------------- | --------------- |
| Fake/Real Detection | Random Forest                               | 85% accuracy   |
| Emotion Detection   | DistilRoBERTa (zero-shot + TF-IDF pipeline) | 85–90%          |
| Reach Prediction    | SVM + XGB + RF Ensemble                     | R²: 0.65–0.75   |
| Embeddings          | all-MiniLM-L6-v2                            | 384-dim vectors |

### Feature Engineering Includes

* Text features: length, punctuation, emoji count, sentiment, hashtags
* Temporal features: posting hour/day (sin/cos encoding)
* Engagement features: likes, comments, shares

---

# 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/saifur033/InspiroAI.git
cd InspiroAI
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Facebook API

Get from Meta Developer:

* Page Access Token
* Page ID

Enter these inside the app sidebar.

### 4. Run the Application

```bash
cd production
streamlit run app.py
```

App runs at:
`http://localhost:8501`

---

# 📖 Usage Guide

### ✔ Status Analyzer

Type caption → Press Analyze → View:

* Emotion breakdown
* Fake/Real classification
* AI recommendations

### ✔ Post Reach Optimizer

Caption → Select Day → Suggest Best Time → View reach score

### ✔ Schedule Post

Caption → Select date/time → Schedule → Auto-posts at target time

---

# 📁 Project Structure

```
InspiroAI/
├── production/
│   ├── app.py
│   ├── models/
│   ├── utils/
│   ├── config.py
│   ├── requirements.txt
│
├── Notebook/
│   ├── EMOTION_DETECTION_cap_C.ipynb
│   ├── reach_prediction_cap_C_final.ipynb
│   └── status_final_cap_C.ipynb
│
├── README.md
└── .gitignore
```

---

# 📊 Performance Metrics

| Metric              | Value         |
| ------------------- | ------------- |
| Fake/Real Detection | ~85%          |
| Emotion Detection   | 85–90%        |
| Reach Prediction    | R²: 0.65–0.75 |
| Model Load Time     | 5–10 sec      |
| Response Time       | <100 ms       |

---

# 🔒 Security

* No cloud storage
* Data not logged externally
* Credentials are temporary
* Facebook API uses HTTPS

---

# 🚧 Known Limitations

* English-only caption support
* Reach prediction varies by page
* No image/video ML analysis
* Manual model retraining needed

---

# 🚀 Future Enhancements

* [ ] Multi-language support (Bangla, Hindi, etc.)
* [ ] Image/video understanding
* [ ] Personalized models per user
* [ ] Advanced analytics dashboard
* [ ] A/B caption testing
* [ ] Cloud deployment
* [ ] PostgreSQL database integration

---

### 🔒 Credit & Usage Policy

**Lead Developer & Core Implementer:** Saifur Rahman  
**Team Members:** Mumtahina, Arpita, Ishrmat  
**Supervisor:** Dr. Anisur Rahman
**Institution:** East West University

---

# 📬 Contact

* Email: **[saifur033@gmail.com](mailto:saifur033@gmail.com)**
* Issues: GitHub Issue Tracker

---

# 🙏 Acknowledgments

* Facebook Graph API
* HuggingFace Transformers
* Streamlit Community
* Open-source ML community

---

<p align="center"><b>Made with passion to improve social media content </b></p>


