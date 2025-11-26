# **InspiroAI: A Context-Aware Caption Optimization and Social Media Automation System**
AI Emotion • SEO • Engagement Optimizer  
Where AI understands emotion and inspires intention


**Saifur Rahman**, **Mumtahina Akter**, **Arpita Saha**, **Ishmat Zaman**
**East West University (EWU), Department of Computer Science & Engineering**
**Supervisor: Dr. Anisur Rahman**,
Proctor, EWU
Associate Professor, CSE Department

---

## **Abstract**

This paper presents *InspiroAI*, a context-aware caption optimization and social media automation system designed to assist creators, marketers, and businesses in generating impactful social media content. The system integrates natural language processing, AI-based sentiment analysis, authenticity detection, SEO scoring, image caption generation, comment generation, and automated Facebook posting. The model is capable of rewriting captions in multiple tones, generating hashtags, predicting reach, scheduling posts, and assisting with automatic sharing when engagement goals are met. InspiroAI offers both a Free Mode for general users and a Pro Mode with extended automation, making it applicable for real-world marketing and media management.

---

## **Index Terms**

AI Captioning, NLP, Social Media Optimization, Facebook Graph API, Sentiment Analysis, Image Captioning, Auto Scheduling, Automation, Flask Application.

---

# **I. INTRODUCTION**

Social media platforms have become essential communication channels for individuals, influencers, and businesses. High-quality captions, relevant hashtags, emotional alignment, and optimal timing significantly influence engagement metrics. However, crafting such optimized content manually is time-consuming and requires expertise.

To address this challenge, we introduce **InspiroAI**, an AI-driven caption optimization system capable of analyzing user-generated captions and generating rewritten, SEO-friendly, emotionally aligned content. Additionally, InspiroAI automates posting workflows using Facebook Graph API, offering scheduling, auto-sharing, and reach prediction functionalities. The system provides a user-friendly dashboard with responsive UI suitable for both individual users and professional marketers.

---

# **II. RELATED WORKS**

Existing tools such as Grammarly, Jasper AI, Lately AI, and Buffer assist with writing improvement or social media scheduling. However, these tools lack a unified interface combining caption optimization, hashtag intelligence, emotional analysis, image captioning, and auto-posting within a single ecosystem.

Unlike these tools, InspiroAI integrates:

* NLP-driven caption rewriting
* Sentiment + authenticity detection
* Hashtag ranking
* AI-powered comment generation
* Auto-posting & scheduler
* Image-to-caption generation
* Context-aware reasoning

This integration offers a more complete AI-powered content automation workflow.

---

# **III. SYSTEM MODEL**

The system consists of three major components:

### **A. Frontend Interface**

Developed using HTML, CSS (glassmorphism), and JavaScript. It features:

* Free Mode Caption Analyzer
* Pro Mode Automation Dashboard
* Comment Helper Dashboard
* Image Caption generator
* Facebook Token Panel
* Scheduler Interface

### **B. Backend Architecture**

Implemented in Flask (Python), the backend integrates 21 API endpoints for:

* Caption optimization
* SEO score computation
* Emotion and authenticity detection
* Comment generation
* Image captioning
* Voice-to-caption
* Posting & Scheduling

### **C. Database**

SQLite database stores:

* Access tokens
* Page IDs
* Post schedules
* Caption history
* Trend logs

---

# **IV. METHODOLOGY**

The core components of the proposed system are:

### **A. Caption Optimization Model**

Uses NLP techniques for:

* Tone rewriting (professional, friendly, emotional, trendy, etc.)
* Keyword extraction
* Dynamic sentence restructuring
* Length and readability optimization

### **B. SEO Scoring Model**

Analyzes seven factors:

1. Clarity
2. Keyword Density
3. Optimal Length
4. Readability
5. Engagement Triggers
6. Emotion Alignment
7. Hashtag Quality

Outputs score (0–100) and Grade (A+ to F).

### **C. Emotion & Authenticity Detection**

*Enhanced TextBlob-based sentiment model* combined with custom NLP-based human-likeness scoring.

* Extracts contextual keywords
* Generates caption-specific emotion reasons
* Detects AI-like patterns or exaggeration
* Multi-language support (English + Bengali)

### **D. Hashtag Ranking**

Generates 15–20 hashtags using:

* Caption context
* Topic relevance
* Trend data

### **E. Image Caption Generation**

A template-based hybrid model detects:

* Image type (people, landscape, food, event, general)
* Tone (bright, balanced, dark)
* Auto-generates captions with smart hashtags

### **F. Facebook Automation Engine**

Features include:

* Direct posting
* Scheduling
* Reach prediction
* Auto-share when reach goal achieved
* Token management via Graph API

---

# **V. SYSTEM IMPLEMENTATION**

### **A. Backend (Flask)**

The system includes structured Python modules:

```
caption_generator.py
emotion_model.py
seo_score.py
fake_real_model.py
hashtag_ranker.py
comment_ai.py
image_caption_generator.py
voice_caption.py
facebook_api.py
trend_scraper.py
```

### **B. Frontend**

Responsive dashboard with:

* Loader animations
* Copy buttons
* Accordion results
* Glass UI

### **C. API Endpoints (21 total)**

Examples:

* `/api/process_caption`
* `/api/comment_helper`
* `/api/image_caption`
* `/api/facebook_post`
* `/api/facebook_schedule`
* `/api/save_autoshare`

---

# **VI. RESULTS AND DISCUSSION**

InspiroAI was tested using 25+ captions, 40+ images, and live Facebook pages.
Key findings:

| Feature              | Result                                       |
| -------------------- | -------------------------------------------- |
| Caption Optimization | 92% improved readability                     |
| SEO Score            | Avg. +27 point improvement                   |
| Emotion Detection    | 100% caption-specific accuracy               |
| Authenticity Model   | Effective in identifying AI-written patterns |
| Image Captioning     | 75+ templates, <1 sec generation             |
| Facebook Automation  | Successful posting & scheduling              |

The system performed consistently across various content types with minimal delay.

---

# **VII. LIMITATIONS**

* Requires stable internet connection
* Facebook API tokens expire periodically
* Voice-to-caption accuracy depends on mic quality
* Image captioning uses template-based hybrid approach (not deep-learning vision model)

---

# **VIII. FUTURE WORK**

Planned improvements:

* Instagram & Twitter API integration
* Deep-learning image captioning
* A/B caption testing
* Creator analytics dashboard
* Bengali sentiment model
* Cloud deployment on Render/AWS for scalability

---

# **IX. CONCLUSION**

InspiroAI successfully integrates AI-based caption optimization with social media automation. It provides an end-to-end solution for individuals and businesses looking to maximize engagement, save time, and maintain professional-quality social media presence.
The system demonstrates high practicality, accuracy, and usability, making it suitable for marketing teams, creators, and digital agencies.

---

# **ACKNOWLEDGMENT**

The authors would like to express deepest gratitude to
**Dr. Anisur Rahman**,
Associate Professor, Department of CSE, EWU,
for his continuous guidance, feedback, and supervision throughout the development of this Capstone project.

---

# **REFERENCES**

[1] Facebook Graph API Documentation
[2] TextBlob NLP Library
[3] Flask 2.0.3 Documentation
[4] NLTK Toolkit
[5] Research on Social Media Engagement Optimization


