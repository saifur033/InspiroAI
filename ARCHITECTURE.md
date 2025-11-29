# InspiroAI - System Architecture

## 🏗️ High-Level Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                    INSPIROAI ARCHITECTURE DIAGRAM                                ║
║                                         (InspiroAI v10.0)                                        ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝


┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         🎨 USER LAYER                                            │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                   │
│     ┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌────────────────┐  │
│     │   Pro Mode      │    │   Free Mode      │    │ Comment Helper   │    │   Scheduler    │  │
│     │  Dashboard      │    │  Dashboard       │    │   Page           │    │    Page        │  │
│     │ (pro_dash.html) │    │(free_dash.html)  │    │(comment_hlp.html)│    │(scheduler.html)│  │
│     └────────┬────────┘    └────────┬─────────┘    └────────┬─────────┘    └────────┬───────┘  │
│              │                      │                       │                       │           │
│              └──────────────────────┼───────────────────────┼───────────────────────┘           │
│                                     │ HTTP/REST            │                                    │
│                                     │ (AJAX/Fetch)         │                                    │
│                                     ▼                      ▼                                    │
│                    ┌─────────────────────────────────────────────┐                             │
│                    │  Static Assets (JS/CSS)                     │                             │
│                    │  • js/pro_dashboard.js                      │                             │
│                    │  • js/toast.js                              │                             │
│                    │  • css/style_pro.css                        │                             │
│                    └─────────────────────────────────────────────┘                             │
│                                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              │ HTTP Requests
                                              ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              🚀 BACKEND / FLASK SERVER                                          │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                         (main.py)                                                │
│                                                                                                   │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                           31 API ENDPOINTS & ROUTES                                       │  │
│  │                                                                                            │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │  │
│  │  │ Page Routes    │  │ Caption Routes │  │ Analysis Routes│  │ Media Routes   │        │  │
│  │  ├────────────────┤  ├────────────────┤  ├────────────────┤  ├────────────────┤        │  │
│  │  │ /pro           │  │ /api/process   │  │ /api/analyze   │  │ /api/image_    │        │  │
│  │  │ /free          │  │ /api/optimize  │  │ /api/reach     │  │   caption      │        │  │
│  │  │ /comment-helper│  │ /api/voice     │  │ /api/emotion   │  │ /api/facebook_ │        │  │
│  │  │ /scheduler     │  │ /api/hashtag   │  │ /api/seo       │  │   post         │        │  │
│  │  │ /token-dash    │  │ /api/generate  │  │               │  │               │        │  │
│  │  └────────────────┘  │   _comments    │  └────────────────┘  └────────────────┘        │  │
│  │                      └────────────────┘                                                  │  │
│  │                                                                                            │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │  │
│  │  │ Master Routes  │  │ Schedule Routes│  │ Settings Routes│  │ Admin Routes   │        │  │
│  │  ├────────────────┤  ├────────────────┤  ├────────────────┤  ├────────────────┤        │  │
│  │  │ /api/process   │  │ /api/schedule  │  │ /api/save_     │  │ /admin-json    │        │  │
│  │  │   _caption     │  │   _post        │  │   settings     │  │ /admin/save_   │        │  │
│  │  │ /api/facebook  │  │ /api/facebook  │  │ /api/get_      │  │   json         │        │  │
│  │  │   _schedule    │  │   _schedule    │  │   token        │  │               │        │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘        │  │
│  │                                                                                            │  │
│  └────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                   │
│  Request Flow:  User Input → Route Handler → AI Module → Database → Response JSON             │
│                                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                              │                           │                           │
                              ▼                           ▼                           ▼
        ┌─────────────────────────────┐    ┌───────────────────────────┐    ┌─────────────────┐
        │   🤖 AI MODULES (src/)      │    │   💾 DATABASE (SQLite)    │    │  🔌 EXTERNAL    │
        └─────────────────────────────┘    │                           │    │    SERVICES     │
        │                                   └───────────────────────────┘    └─────────────────┘
        │
        ├─── Caption Analysis & Generation
        │    ├─ caption_analyzer.py ────────────► Lightweight deterministic analysis
        │    ├─ caption_generator.py ──────────► Caption variations & optimization
        │    ├─ caption_styler.py ─────────────► Style-based transformations
        │    └─ master_caption_processor.py ──► 5-section human-quality analysis
        │
        ├─── Emotion & Authenticity Detection
        │    ├─ emotion_model.py ─────────────► 9 emotion categories + scoring
        │    ├─ fake_real_model.py ──────────► AI vs Real detection (%)
        │    └─ seo_score.py ─────────────────► SEO scoring (0-100)
        │
        ├─── Media Processing
        │    ├─ image_caption_generator.py ───► Image → Caption conversion
        │    ├─ voice_caption.py ─────────────► Voice → Text transcription
        │    └─ facebook_api.py ──────────────► Facebook Graph API integration
        │
        ├─── Content Intelligence
        │    ├─ hashtag_ranker.py ───────────► Hashtag generation & ranking
        │    ├─ trend_scraper.py ────────────► Trend detection & analysis
        │    ├─ comment_ai.py ────────────────► Comment suggestion engine
        │    └─ comprehensive_analysis.py ───► Full-spectrum analysis
        │
        ├─── Database & Scheduling
        │    ├─ db_manager.py ────────────────► Database operations & queries
        │    ├─ scheduler_engine.py ─────────► Post scheduling system
        │    └─ worker_*.py ──────────────────► Background job processing
        │
        └─── Utilities
             ├─ utils.py ────────────────────► Helper functions & decorators
             └─ caption_templates.json ─────► Pre-built caption templates

┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              💾 DATABASE LAYER (database.db)                                    │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                   │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│  │   captions      │  │   tokens         │  │ auto_share_rules │  │   trends         │       │
│  ├─────────────────┤  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤       │
│  │ • id (PK)       │  │ • id (PK)        │  │ • id (PK)        │  │ • id (PK)        │       │
│  │ • text          │  │ • user_id        │  │ • user_id        │  │ • keyword        │       │
│  │ • seo_score     │  │ • platform_token │  │ • metric         │  │ • trend_score    │       │
│  │ • emotion       │  │ • page_id        │  │ • target_value   │  │ • category       │       │
│  │ • timestamp     │  │ • expires_at     │  │ • caption        │  │ • updated_at     │       │
│  │ • language      │  │ • created_at     │  │ • active         │  │                  │       │
│  └─────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘       │
│                                                                                                   │
│  ┌──────────────────────────────────────────────────────────────────────────────────────┐     │
│  │                         scheduler (Version: 10.0 - Fully Migrated)                    │     │
│  ├──────────────────────────────────────────────────────────────────────────────────────┤     │
│  │ • id (PK) • caption • scheduled_time • status • facebook_post_id • created_at         │     │
│  └──────────────────────────────────────────────────────────────────────────────────────┘     │
│                                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              │ SQLite3
                                              │ (Persistent Storage)
                                              ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                          🔌 EXTERNAL SERVICES & INTEGRATIONS                                   │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                   │
│  ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐ │
│  │  📱 Facebook API         │    │  🗣️ Speech Recognition  │    │  🌐 Google Services     │ │
│  ├──────────────────────────┤    ├──────────────────────────┤    ├──────────────────────────┤ │
│  │ • Graph API v18.0        │    │ • Google Cloud Speech   │    │ • Custom Search (optional)
│  │ • Post Publishing        │    │ • Audio to Text         │    │ • Language API          │ │
│  │ • Page Feed Access       │    │ • Multi-language        │    │ • NLP Services (optional)
│  │ • Token Management       │    │ • Fallback Mode         │    │                          │ │
│  └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘ │
│                                                                                                   │
│  ┌──────────────────────────┐    ┌──────────────────────────┐                                 │
│  │  📊 Analytics (Optional) │    │  🔐 Security Services   │                                 │
│  ├──────────────────────────┤    ├──────────────────────────┤                                 │
│  │ • Facebook Insights      │    │ • Token Encryption      │                                 │
│  │ • Custom Metrics         │    │ • CORS Protection       │                                 │
│  │ • Performance Tracking   │    │ • Input Validation      │                                 │
│  └──────────────────────────┘    └──────────────────────────┘                                 │
│                                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                     DATA FLOW DIAGRAM                                           ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  CAPTION INPUT FLOW (Pro Dashboard Workflow)                                                    │
│                                                                                                  │
│    User Input                                                                                   │
│       │                                                                                         │
│       ├── Manual Caption Entry ──────┐                                                         │
│       ├── Voice Recording ────────────┼─► /api/voice_caption ─► Google Speech API             │
│       ├── Image Upload ──────────────┼─► /api/image_caption ──► Vision Processing             │
│       └── Template Selection ────────┘                                                         │
│                                                                                                  │
│       ▼ (Caption Text Available)                                                               │
│                                                                                                  │
│    Master Processing (/api/process_caption_master)                                             │
│       ├─► Section 1: Analysis                                                                  │
│       │   ├─ SEO Score (0-100) via seo_score.py                                               │
│       │   ├─ Emotion Detection via emotion_model.py (9 types)                                 │
│       │   └─ Authenticity Check via fake_real_model.py                                        │
│       │                                                                                         │
│       ├─► Section 2: Optimization                                                              │
│       │   ├─ Professional Version (caption_styler.py)                                         │
│       │   └─ Social Media Version (caption_generator.py)                                      │
│       │                                                                                         │
│       ├─► Section 3: Hashtags                                                                  │
│       │   └─ 12-20 Context-aware hashtags (hashtag_ranker.py)                               │
│       │                                                                                         │
│       ├─► Section 4: Reach Insights                                                            │
│       │   ├─ Best Posting Time (Dynamic)                                                      │
│       │   ├─ Engagement Prediction                                                             │
│       │   └─ Audience Type Analysis                                                            │
│       │                                                                                         │
│       └─► Section 5: Caption Ideas (Optional)                                                  │
│           ├─ 5 Short Captions                                                                  │
│           └─ 3 Emotional/Alert Captions                                                        │
│                                                                                                  │
│       ▼ (Display Results)                                                                      │
│                                                                                                  │
│    Action Selection                                                                             │
│       ├─► Share to Facebook ──► /api/facebook_post ──► Facebook Graph API                    │
│       ├─► Schedule Post ─────► /api/facebook_schedule ──► db (scheduler table)               │
│       ├─► Copy Caption ───────► Clipboard                                                      │
│       ├─► Generate Comments ──► /api/generate_comments ──► comment_ai.py                    │
│       └─► Save Draft ────────► database (captions table)                                      │
│                                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                  DEPLOYMENT ARCHITECTURE                                       ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                   │
│                              ┌─────────────────────────┐                                        │
│                              │   GitHub Repository     │                                        │
│                              │   (saifur033/InspiroAI) │                                        │
│                              │   • main branch         │                                        │
│                              │   • Version: 10.0       │                                        │
│                              └────────────┬────────────┘                                        │
│                                           │                                                     │
│                                           ▼                                                     │
│                              ┌─────────────────────────┐                                        │
│                              │   Local Environment     │                                        │
│                              │   • Python 3.10.11      │                                        │
│                              │   • Virtual Env (.venv) │                                        │
│                              │   • Flask Server        │                                        │
│                              │   • SQLite Database     │                                        │
│                              └─────────────────────────┘                                        │
│                              http://127.0.0.1:5000                                              │
│                                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                  TECHNOLOGY STACK SUMMARY                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                   │
│  FRONTEND                      BACKEND                    DATABASE            EXTERNAL          │
│  ═════════════════════════════════════════════════════════════════════════════════════════════  │
│                                                                                                   │
│  • HTML5                       • Flask 2.x               • SQLite 3.x         • Facebook API    │
│  • CSS3 (Responsive)           • Python 3.10             • 4 Tables           • Google Speech   │
│  • JavaScript (Vanilla)        • RESTful API             • v10.0 Schema       • Vision API      │
│  • AJAX/Fetch API              • 31 Routes              • Full Migration      • Optional: NLP   │
│  • Toast Notifications         • Error Handling         • Queries Optimized   • Search APIs     │
│  • Media Recorder API          • CORS Enabled           • Indexed PK/FK       • Security Auth   │
│  • Canvas API (Optional)       • Input Validation       • Transactional       • Rate Limiting   │
│                                • JWT Tokens (Ready)     • Backups Ready       • TLS/HTTPS       │
│                                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                  KEY FEATURES & CAPABILITIES                                   ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝

✨ CAPTION ANALYSIS & GENERATION
   • Master Caption Processor (5 sections of analysis)
   • SEO Scoring (Deterministic, 0-100)
   • Emotion Detection (9 categories with word citations)
   • Authenticity Analysis (Real % vs AI-Like %)
   • Caption Optimization (2 unique versions)
   • Hashtag Generation (12-20 dynamic tags)
   • Reach & Timing Insights (Dynamic predictions)

🎤 MULTIMODAL INPUT
   • Text Caption Entry
   • Voice-to-Text Conversion
   • Image-to-Caption Generation
   • Template-Based Suggestions

💬 SOCIAL MEDIA FEATURES
   • AI Comment Generation (5 categories)
   • Zero-Repetition Algorithm
   • Caption-Context Aware Comments
   • Language Auto-Detection (Bangla/English)
   • Tone Customization (Friendly, Professional, Emotional, Funny, etc.)

📱 FACEBOOK INTEGRATION
   • Direct Post Publishing
   • Scheduled Post Publishing
   • Multi-Account Support
   • Token Management & Storage
   • Real-time Feedback

📊 ANALYTICS & INSIGHTS
   • Post Performance Tracking
   • Trend Analysis
   • Audience Demographics (Optional)
   • Engagement Predictions
   • Best Posting Times

🔒 SECURITY & RELIABILITY
   • Input Validation & Sanitization
   • XSS Prevention
   • CORS Protection
   • Token Encryption
   • Error Recovery
   • Graceful Fallbacks

═══════════════════════════════════════════════════════════════════════════════════════════════════

```

## 📊 Architecture Layers Breakdown

### Layer 1: User Interface (Frontend)
- **Pro Dashboard**: Advanced features for premium users
- **Free Dashboard**: Basic caption analysis
- **Comment Helper**: AI-powered comment generation
- **Scheduler**: Post scheduling interface
- **Token Dashboard**: API token management

### Layer 2: API Layer (Backend Routes)
```
31 Total Routes organized into categories:
├─ Page Routes (5): Navigation & template rendering
├─ Caption Routes (8): Analysis, optimization, voice, hashtags
├─ Analysis Routes (6): SEO, emotion, authenticity, reach
├─ Media Routes (4): Image, video, audio processing
├─ Master Routes (2): Complete processing pipeline
├─ Schedule Routes (2): Post scheduling system
├─ Settings Routes (2): Configuration & token management
└─ Admin Routes (2): JSON templates & system admin
```

### Layer 3: AI Processing (Intelligent Modules)
```
Core AI Engines:
├─ Caption Analysis (Lightweight & Master)
├─ Emotion Detection (9 categories)
├─ Authenticity Verification
├─ Comment Generation (5 tones)
├─ Hashtag Ranking
├─ SEO Scoring
├─ Trend Detection
└─ Voice/Image Processing
```

### Layer 4: Data Layer (SQLite Database)
```
4 Primary Tables:
├─ captions: Caption history & analytics
├─ tokens: Facebook token management
├─ auto_share_rules: Automation rules
├─ trends: Trending topics & keywords
└─ scheduler: Scheduled posts
```

### Layer 5: External Services
```
Integrated Services:
├─ Facebook Graph API (Publishing & Insights)
├─ Google Speech Recognition (Voice-to-Text)
├─ Vision APIs (Optional Image Processing)
└─ Search & NLP APIs (Optional)
```

---

## 🔄 Request/Response Cycle

```
User Action
    ↓
Frontend (HTML/JS)
    ↓
HTTP Request (POST/GET)
    ↓
Flask Route Handler
    ↓
Input Validation & Sanitization
    ↓
AI Module Processing
    ↓
Database Query/Update
    ↓
External API Call (if needed)
    ↓
JSON Response Generation
    ↓
Frontend Display/Update
    ↓
User Sees Result
```

---

## 📈 Scalability & Performance

| Component | Optimization | Status |
|-----------|--------------|--------|
| Database Queries | Indexed PK/FK | ✅ Optimized |
| API Response Time | Caching Ready | ✅ Ready |
| Frontend Load | Lazy Loading | ✅ Implemented |
| Media Processing | Async Jobs (Ready) | ✅ Ready |
| AI Module Speed | Lightweight Fallbacks | ✅ Active |
| Error Handling | Graceful Degradation | ✅ Implemented |

---

**Generated**: November 29, 2025  
**InspiroAI Version**: 10.0  
**Status**: Production Ready ✅
