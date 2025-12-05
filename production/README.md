# InspiroAI - Context-Aware Facebook Caption Optimization System

A production-ready machine learning system that analyzes Facebook captions and provides intelligent optimization, emotion detection, reach prediction, and automated posting capabilities.

## 🎯 Features

### **1. Status Analyzer (Tab 1)**
- **Authenticity Detection**: Classifies captions as Fake/Real using ensemble ML models
- **Emotion Analysis**: Detects 6 emotions (anger, fear, joy, neutral, sadness, surprise)
- **Confidence Scores**: Shows prediction confidence for transparency
- **Model Threshold**: 0.73 for balanced Fake/Real detection

### **2. Post Reach Optimizer (Tab 2)**
- **Reach Prediction**: Predicts potential post reach based on content
- **Smart Timing**: Data-driven best posting times by day and ad type
- **Auto-Share Feature**: Automatically posts when predicted reach meets target
- **Custom Target Reach**: Set goals from 100 to 1000+ impressions

### **3. Schedule Post (Tab 3)**
- **Date & Time Selection**: Schedule posts for future dates
- **Caption Management**: Save and manage multiple captions
- **Facebook Integration**: Direct posting with credentials

### **4. Tools & Utilities (Tab 4)**
- **Caption Generator**: AI-generated captions with 15+ hashtags (topic-based)
  - Templates for: graduation, project, internship, learning
- **Caption Optimizer**: Intelligent rewriting with CTAs and hashtags
  - Removes repetitive phrases
  - Adds powerful opening lines
  - Generates varied call-to-action questions
  - Adds 15+ engagement hashtags
- **Hashtag Generator**: Theme-based hashtag suggestions
  - Categories: education, career, technology, inspiration, lifestyle
- **Facebook Sharing**: Direct post button with credentials validation

---

## 🏗️ Project Structure

```
production/
├── app.py                      # Main Streamlit web application (720+ lines)
├── main.py                     # Entry point for launching app
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
│
├── utils/
│   ├── __init__.py
│   ├── model_loader.py        # ML model loading & registry
│   └── inference.py           # Prediction functions (emotion, reach, status)
│
├── models/                     # Pre-trained ML model artifacts
│   ├── reach_voting.joblib
│   ├── reach_scaler.joblib
│   ├── reach_ohe.joblib
│   ├── status_xgb.joblib
│   ├── status_rf.joblib
│   └── status_lgb.joblib
│
└── assets/                     # Application assets
```

---

## 🚀 Quick Start

### **1. Installation**

```bash
cd production
pip install -r requirements.txt
```

### **2. Run Application**

```bash
python main.py
```

Or directly with Streamlit:

```bash
streamlit run app.py
```

The app will open at: **http://localhost:8501** (or similar port)

### **3. Setup Facebook Credentials (Optional)**

In the sidebar under **Authentication**:
- Enter your Facebook API Token
- Enter your Facebook Page ID
- Click **SAVE**

---

## 🤖 ML Models Architecture

### **Model 1: Emotion Detection**
- **Type**: HuggingFace DistilRoBERTa Transformer
- **Model ID**: `j-hartmann/emotion-english-distilroberta-base`
- **Classes**: 6 emotions (anger, fear, joy, neutral, sadness, surprise)
- **Input**: Text caption
- **Output**: Emotion label + confidence score + all emotion probabilities
- **Auto-download**: First use downloads model automatically

### **Model 2: Reach Prediction**
- **Type**: VotingClassifier Ensemble
- **Components**: 
  - Logistic Regression (weight: 0.33)
  - CatBoost (weight: 0.33)
  - XGBoost (weight: 0.33)
- **Threshold**: 0.40
- **Input**: Text embeddings (384-dim, all-MiniLM-L6-v2)
- **Output**: Binary classification (High/Low reach)

### **Model 3: Status/Authenticity**
- **Type**: Weighted Ensemble
- **Components**:
  - XGBoost (weight: 0.5)
  - Random Forest (weight: 0.3)
  - LightGBM (weight: 0.2)
- **Threshold**: 0.73
- **Output**: Suspicion score + classification (Real/Fake)
- **Accuracy**: 57.1% on test set (model limitation from training data bias)

### **Text Embeddings**
- **Model**: Sentence-Transformers (all-MiniLM-L6-v2)
- **Dimensions**: 384-dimensional vectors
- **Purpose**: Convert captions to numerical format for ML models

---

## 💻 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend | Streamlit | 1.35.0 |
| ML Framework | Scikit-learn | 1.3.0 |
| Ensemble Models | XGBoost, CatBoost, LightGBM | 2.0.2, 1.2.1, 4.0.0 |
| Text Embeddings | Sentence-Transformers | 2.2.2 |
| Transformer Models | Hugging Face Transformers | Latest |
| Python | Python | 3.10.11 |

---

## 📊 Usage Examples

### **Example 1: Analyze a Caption**

1. Go to **Status Analyzer** tab
2. Enter caption: "Amazing experience with internship! Grateful for this opportunity."
3. Click **Analyze**
4. View:
   - Authenticity: Real/Fake with confidence
   - Emotion: Detected emotion + all 6 emotion scores

### **Example 2: Optimize & Share**

1. Go to **Tools & Utilities** → **Caption Optimizer**
2. Paste your caption
3. Click **Optimize**
4. View rewritten caption with 15+ hashtags
5. Click **Share to Facebook** (if credentials provided)

### **Example 3: Generate Captions**

1. Go to **Tools & Utilities** → **Caption Generator**
2. Enter topic: "graduation"
3. Click **Generate Captions**
4. Select from 3 AI-generated options
5. Click **Save Caption** or **Share** directly

---

## 🔐 Configuration

Edit `config.py` to customize:

```python
# Model paths
MODEL_PATHS = {
    'reach': 'models/reach_voting.joblib',
    'status_xgb': 'models/status_xgb.joblib',
    # ... etc
}

# Thresholds
REACH_THRESHOLD = 0.40
STATUS_THRESHOLD = 0.73

# Streamlit config
STREAMLIT_PORT = 8501
```

---

## 📈 Performance Metrics

| Model | Metric | Value |
|-------|--------|-------|
| Emotion Detection | Coverage | 6 emotions |
| Emotion Detection | Confidence | Model-dependent |
| Reach Prediction | Threshold | 0.40 |
| Status Detection | Threshold | 0.73 |
| Status Detection | Test Accuracy | 57.1% |

**Note on Status Model**: The 57.1% accuracy is due to inherent bias in the training data (Facebook posts tend to cluster in similar score ranges). This is a limitation of the original notebook's training methodology.

---

## 🎨 Design Features

- **Glass Morphism**: Modern frosted glass UI elements
- **Gradient Backgrounds**: Professional purple-to-pink gradient theme
- **Responsive Layout**: Works on desktop and tablet
- **Card Design**: Enhanced cards with shadows and hover effects
- **No Emojis**: Clean professional appearance
- **Session State**: Persistent state management for seamless UX

---

## 📝 Input/Output Examples

### **Status Analyzer**
```
Input: "I am a student from East West University looking for opportunities"
Output:
  Authenticity: Fake (73.1% confidence)
  Emotion: Neutral (confidence: 0.85)
  Emotions: {anger: 0.05, fear: 0.02, joy: 0.08, neutral: 0.85, sadness: 0.02, surprise: 0.01}
```

### **Caption Optimizer**
```
Input: "Great day at work today"
Output: "Excited to share: Great day at work today! What are your thoughts on this? 
         #Growth #Success #Achievement #Inspired #Grateful #Motivation #Learning 
         #Community #Development #Empowered #Journey #Goals #Dreams #ProudMoment 
         #LivingMyBestLife"
```

---

## 🔧 Troubleshooting

### **App won't start**
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart with verbose logging
streamlit run app.py --logger.level=debug
```

### **Models not loading**
```bash
# Verify model files exist
ls -la models/

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### **Facebook share not working**
- Verify token format is correct
- Ensure page ID is numerical
- Check that token has appropriate permissions

---

## 📚 Files Guide

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application (720+ lines) |
| `main.py` | Entry point with dependency checking |
| `config.py` | Configuration & settings |
| `utils/model_loader.py` | ML model loading & registry |
| `utils/inference.py` | Prediction functions |
| `requirements.txt` | Python package dependencies |

---

## 🎓 For Research/Paper

### **Key Contributions**
1. **Multi-model Ensemble**: Combines XGBoost, Random Forest, LightGBM for robust predictions
2. **Transformer-based Emotion**: Uses state-of-the-art HuggingFace DistilRoBERTa
3. **Automated Optimization**: Intelligently rewrites captions for engagement
4. **Production Ready**: Full-stack web application with Facebook integration

### **Citation**
If using this system for research, cite the original notebook authors and mention:
- Models trained on Facebook social media data
- Threshold calibrated for balanced classification
- Ensemble approach for improved robustness

---

## 📞 Support

For issues or questions:
1. Check the logs: `streamlit run app.py --logger.level=debug`
2. Verify model files in `models/` directory
3. Ensure all dependencies installed: `pip list`

---

## ✅ Verification Checklist

- [x] All 3 ML models loading correctly
- [x] Emotion detection with 6 classes
- [x] Reach prediction functional
- [x] Status/Authenticity detection working
- [x] Caption generation & optimization
- [x] Hashtag suggestions working
- [x] Facebook integration ready
- [x] UI design polished
- [x] Session state management
- [x] Production-ready deployment

---

## 📄 License & Attribution

This system is based on research models and includes:
- HuggingFace DistilRoBERTa (Apache 2.0)
- Sentence-Transformers (Apache 2.0)
- Original notebook implementations

---

**Last Updated**: December 5, 2025  
**Status**: Production Ready  
**Version**: 1.0

---

## 🚀 Next Steps

1. **Test the System**: Visit http://localhost:8501
2. **Try Examples**: Use sample captions from the "View Examples" section
3. **Configure Facebook**: Add your credentials in sidebar (optional)
4. **Generate Content**: Use Tools tab to optimize your own captions
5. **Submit for Paper**: Include this README and system screenshots

Happy optimizing! 🎉
