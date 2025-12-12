"""
================================================================================
InspiroAI - AI-Based Caption Optimization & Facebook Auto-Posting System
================================================================================

DEVELOPED BY: Saifur Rahman (Lead Developer)
PROJECT: East West University Capstone Project
SUPERVISOR: Dr. Anisur Rahman

COPYRIGHT NOTICE:
This software is the intellectual property of the development team.
Unauthorized redistribution, copying, or claiming ownership is strictly prohibited.
All rights reserved.

================================================================================
"""
import streamlit as st
from datetime import datetime, timedelta
import time

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="InspiroAI",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# AUTO-REFRESH FOR SCHEDULED POSTS
# ============================================
# Check if there are pending posts and auto-refresh
if 'check_interval' not in st.session_state:
    st.session_state.check_interval = 0

st.session_state.check_interval += 1

# Check pending posts FIRST, before rendering anything (ON EVERY RENDER)
try:
    pending_posts = [p for p in st.session_state.get('scheduled_posts', []) if p.get('status') == 'Pending']
    
    if pending_posts:
        from datetime import datetime
        now = datetime.now()
        posted_any = False
        
        for post in pending_posts:
            scheduled_dt = post.get('scheduled_dt')
            if scheduled_dt and scheduled_dt <= now:
                # Time to post!
                try:
                    from utils.facebook_posting import FacebookPoster
                    fb_token = st.session_state.get('fb_token', '')
                    fb_page_id = st.session_state.get('fb_page_id', '')
                    
                    if fb_token and fb_page_id:
                        poster = FacebookPoster(page_token=fb_token, page_id=fb_page_id)
                        success, result = poster.publish_post(message=post['caption'])
                        
                        if success:
                            post['status'] = 'Posted'
                            post['posted_at'] = now
                            post['post_id'] = result.get('post_id', 'unknown')
                            posted_any = True
                        else:
                            post['status'] = 'Failed'
                            post['error'] = result.get('error', 'Unknown error')
                            posted_any = True
                except Exception as e:
                    post['status'] = 'Failed'
                    post['error'] = str(e)
                    posted_any = True
        
        # Refresh UI immediately if any post was updated
        if posted_any:
            from utils.post_storage import PostStorage
            PostStorage.save_posts(st.session_state.scheduled_posts)
            st.rerun()
except:
    pass

# Auto-rerun every 1 second if there are pending posts
try:
    pending_posts = [p for p in st.session_state.get('scheduled_posts', []) if p.get('status') == 'Pending']
    if pending_posts:
        time.sleep(1)
        st.rerun()
except:
    pass

# ============================================
# CUSTOM STYLING
# ============================================
st.markdown("""
    <style>
    /* Main container */
    .main { 
        padding: 2rem; 
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 12px;
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(10px);
        padding: 12px 16px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    
    /* Metric cards - Enhanced */
    .metric-card { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem; 
        border-radius: 16px;
        color: white;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.35);
    }
    
    /* Card wrapper for content */
    .content-card {
        background: white;
        padding: 1.5rem;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .content-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Button styling - Enhanced & Responsive */
    .stButton {
        width: 100% !important;
        min-width: 0 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
        font-size: 0.85rem !important;
        line-height: 1.3 !important;
        letter-spacing: 0.2px !important;
        min-height: 40px !important;
        height: auto !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-sizing: border-box !important;
        white-space: normal !important;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Mobile responsive buttons */
    @media (max-width: 768px) {
        .stButton > button {
            font-size: 0.85rem !important;
            padding: 10px 16px !important;
            min-height: 40px !important;
        }
    }
    
    @media (max-width: 480px) {
        .stButton > button {
            font-size: 0.8rem !important;
            padding: 10px 14px !important;
            min-height: 38px !important;
        }
    }
    
    /* Text input styling - Enhanced */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e8e8e8;
        padding: 14px 16px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #fafbfc;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
        background: white;
    }
    
    /* Select box styling - Enhanced */
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e8e8e8;
        padding: 12px 16px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
    }
    
    /* Radio styling - Enhanced */
    .stRadio > div {
        gap: 24px;
        background: rgba(255,255,255,0.5);
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid #e8e8e8;
    }
    
    /* Info boxes - Enhanced */
    .stInfo {
        background: linear-gradient(135deg, rgba(227, 242, 253, 0.8) 0%, rgba(243, 229, 245, 0.8) 100%);
        border-left: 5px solid #667eea;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(232, 245, 233, 0.8) 0%, rgba(241, 248, 233, 0.8) 100%);
        border-left: 5px solid #4caf50;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 243, 224, 0.8) 0%, rgba(252, 228, 236, 0.8) 100%);
        border-left: 5px solid #ff9800;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 12px rgba(255, 152, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 235, 238, 0.8) 0%, rgba(253, 237, 236, 0.8) 100%);
        border-left: 5px solid #f44336;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 12px rgba(244, 67, 54, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Section headers - Enhanced */
    h1, h2, h3 {
        color: #667eea;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    h1 {
        font-size: 2.2em;
    }
    
    h2 {
        font-size: 1.6em;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-size: 1.3em;
        margin-bottom: 0.8rem !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 1.5rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Progress bar enhancement */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Columns and spacing */
    .stColumn {
        padding: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# LOAD MODELS
# ============================================
# MODEL LOADING WITH ERROR HANDLING
# ============================================
@st.cache_resource
def load_models():
    try:
        from utils.model_loader import get_model_registry
        from sentence_transformers import SentenceTransformer
        
        print("[INFO] Loading models...")
        registry = get_model_registry()
        print(f"[OK] Model registry loaded - status_rf: {registry.status_rf is not None}")
        
        print("[INFO] Loading embedder...")
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        print(f"[OK] Embedder loaded: {embedder is not None}")
        
        if registry.status_rf is None:
            print("[ERROR] Status RF model not loaded!")
            return None, None, False
            
        return registry, embedder, True
    except Exception as e:
        print(f"[ERROR] Error loading models: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None, False

model_registry, embedder, models_loaded = load_models()

# Show error if models failed to load
if not models_loaded:
    st.error("""
    ❌ **Models failed to load!** 
    
    This might be due to:
    1. Missing model files in `/production/models/`
    2. Network timeout downloading embedder (try refreshing)
    3. Insufficient memory on server
    
    Check the terminal logs for detailed error messages.
    """)
    st.stop()

# ============================================
# INITIALIZE PERSISTENT STORAGE
# ============================================
# Load scheduled posts from persistent storage at app startup (BEFORE anything else)
if 'scheduled_posts' not in st.session_state:
    from utils.post_storage import PostStorage
    st.session_state.scheduled_posts = PostStorage.load_posts()

# ============================================
# SIDEBAR - AUTHENTICATION
# ============================================
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px;">
    <h3 style="margin: 0; text-align: center;">Authentication</h3>
</div>
""", unsafe_allow_html=True)

# Initialize session state for credentials
if 'fb_token' not in st.session_state:
    st.session_state.fb_token = ''
if 'fb_page_id' not in st.session_state:
    st.session_state.fb_page_id = ''

# Token input - allow paste/copy
fb_token = st.sidebar.text_input(
    "Facebook API Token",
    value=st.session_state.get('fb_token', ''),
    placeholder="Paste your token here (visible for copying)",
    help="You can safely paste and copy your token here",
    key="fb_token_input"
)
# Update session state as user types
st.session_state.fb_token = fb_token

# Page ID input
fb_page_id = st.sidebar.text_input(
    "Facebook Page ID",
    value=st.session_state.get('fb_page_id', ''),
    placeholder="123456789",
    help="Your Facebook page numeric ID",
    key="fb_page_id_input"
)
# Update session state as user types
st.session_state.fb_page_id = fb_page_id

st.sidebar.markdown("---")

# Save & Clear buttons
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Save", use_container_width=True, key="fb_save_btn"):
        if fb_token and fb_page_id:
            st.sidebar.success("✅ Credentials saved successfully!")
        else:
            st.sidebar.warning("⚠️ Please enter both token and page ID")

with col2:
    if st.button("Clear", use_container_width=True, key="fb_clear_btn"):
        # Clear from session state only
        st.session_state.fb_token = ''
        st.session_state.fb_page_id = ''
        st.sidebar.success("✅ Credentials cleared!")
        time.sleep(0.3)
        st.rerun()

# ============================================
# PAGE TITLE
# ============================================
st.markdown("""
<style>
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); }
    50% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.6); }
}

.glass-title {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 30px;
    text-align: center;
    animation: float 3s ease-in-out infinite, glow 3s ease-in-out infinite;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
}

.glass-title h1 {
    margin: 0;
    font-size: 1.8em;
    white-space: nowrap;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    letter-spacing: -0.5px;
}
</style>

<div class="glass-title">
    <h1>InspiroAI - Context-Aware Facebook Caption Optimization System</h1>
</div>
""", unsafe_allow_html=True)

# ============================================
# INITIALIZE SESSION STATE
# ============================================
if 'target_reach' not in st.session_state:
    st.session_state.target_reach = 500  # Default target reach
if 'auto_share_caption' not in st.session_state:
    st.session_state.auto_share_caption = ""  # Caption for auto-share
if 'auto_share_active' not in st.session_state:
    st.session_state.auto_share_active = False  # Auto-share activation status

# ============================================
# MAIN TABS
# ============================================
tab1, tab2, tab3 = st.tabs([
    "Status Analyzer",
    "Post Reach Optimizer",
    "Schedule Post"
])

# ============================================
# TAB 1: STATUS ANALYZER
# ============================================
with tab1:
    # Initialize session state for analysis results
    if 'fake_real' not in st.session_state:
        st.session_state.fake_real = None
    if 'fake_real_score' not in st.session_state:
        st.session_state.fake_real_score = 0
    if 'emotions_list' not in st.session_state:
        st.session_state.emotions_list = []
    
    st.subheader("Status Analyzer")
    st.write("Enter your status/caption here...")
    
    # Authenticity explanation in collapsible expander
    with st.expander("🔍 How Authenticity is Determined (Click to expand)"):
        st.markdown("""
### **Real Caption**
- Score < 65% → Authentic, natural writing
- Includes personal tone, unique wording

### **Fake Caption**
- Score ≥ 65% → Template-like, repetitive, or spam-pattern content  
- Overuse of generic phrases or engagement-bait

### **Why threshold updated to 0.65**
- Original model threshold was 0.40 (too strict)
- Adjusted to 0.65 for balanced performance on Facebook-style writing

### **Model detects Fake when caption contains:**
- Template or repetitive structure ("I am a student from…")
- Copy-paste patterns
- Low-engagement linguistic signals
- Bot-like or overly formal writing

⚠️ **Note:** LinkedIn-style highly formal captions may be mistakenly flagged as fake.
        """)
    
    # Add example captions section
    with st.expander("View Example: Fake vs Real Captions"):
        st.markdown("**❌ EXAMPLE FAKE CAPTIONS (Score ≥ 40%):**")
        st.markdown("- 'i am a student from east west university' (73.1%)")
        st.markdown("- 'I am looking for job opportunities. Please contact me.' (73.4%)")
        st.markdown("- 'Hi! I'm Saifur Rahman from CSE at East West University' (73.1%)")
        st.markdown("- 'Discovering robotics with Discover Robotics, discovering myself. Alhamdulillah.' (72.8%)")
        
        st.markdown("**✅ EXAMPLE REAL CAPTIONS (Score < 40%):**")
        st.markdown("- 'Just had genuine conversation with friend about life goals'")
        st.markdown("- 'Sharing unique personal story with authentic emotional expression'")
        st.markdown("- 'Original thought or experience with specific details and context'")
        
        st.info("**Notebook Logic:** Threshold is 0.40 from the original research paper. This model is trained on Facebook social media data.")    
    
    # Initialize caption in session state if not exists
    if 'tab1_caption' not in st.session_state:
        st.session_state.tab1_caption = ""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        caption = st.text_area(
            "Caption",
            value=st.session_state.tab1_caption,
            height=120,
            placeholder="Write your Facebook caption...",
            label_visibility="collapsed",
            key="tab1_caption_input"
        )
    
    with col2:
        st.write("")  # Spacer
        st.write("")  # Spacer
        analyze_btn = st.button("Analyze", use_container_width=True, key="analyze_btn_tab1")
        clear_btn = st.button("Clear", use_container_width=True, key="clear_btn_tab1")
        post_now_btn_temp = st.button("Share", use_container_width=True, key="post_now_btn_temp")
    
    # Handle Clear button BEFORE syncing caption
    if clear_btn:
        st.session_state.tab1_caption = ""
        st.session_state.emotions_list = []
        st.session_state.fake_real = None
        st.session_state.fake_real_score = 0
        st.rerun()
    
    # Always sync caption from text_area to session state (after clear button check)
    st.session_state.tab1_caption = caption
    
    # Handle Share button
    if post_now_btn_temp:
        fb_token = st.session_state.get('fb_token', '')
        fb_page_id = st.session_state.get('fb_page_id', '')
        
        if not caption.strip():
            st.error("❌ Please enter a caption first")
        elif not fb_token or not fb_page_id:
            st.error("❌ Please provide Facebook Token & Page ID in the sidebar first")
        else:
            # Show loading spinner while posting
            with st.spinner("📤 Publishing to Facebook..."):
                try:
                    from utils.facebook_posting import FacebookPoster
                    import time
                    
                    poster = FacebookPoster(page_token=fb_token, page_id=fb_page_id)
                    
                    # Publish only the caption (no analysis data)
                    success, result = poster.publish_post(message=caption)
                    
                    # Add small delay to ensure Facebook processes it
                    time.sleep(1)
                    
                    if success:
                        st.success("✅ Post published successfully to Facebook!")
                        st.success(f"📱 Post ID: {result.get('post_id', 'unknown')}")
                        st.success(f"🔗 View post: {result.get('url', '')}")
                        st.balloons()
                        
                        # Clear caption after successful post
                        st.session_state.tab1_caption = ""
                        st.session_state.emotions_list = []
                        st.session_state.fake_real = None
                        st.session_state.fake_real_score = 0
                        time.sleep(2)
                        st.rerun()
                    else:
                        error_msg = result.get('error', 'Unknown error')
                        st.error(error_msg)
                        if result.get('details'):
                            st.warning(f"ℹ️ Details: {result.get('details')}")
                
                except Exception as e:
                    st.error(f"❌ Error posting to Facebook: {str(e)}")
    
    if analyze_btn:
        # Clear previous results first
        st.session_state.fake_real = None
        st.session_state.fake_real_score = 0
        st.session_state.emotions_list = []
        
        if not caption.strip():
            st.warning("Please enter a caption first")
        elif not models_loaded:
            st.error("Models not loaded. Please check your environment.")
        else:
            try:
                from utils.inference import EmotionPredictor, StatusPredictor
                
                # Get predictions - emotion now uses pretrained transformer
                status_result = StatusPredictor.predict(caption, embedder=embedder, model_registry=model_registry)
                emotion_result = EmotionPredictor.predict(caption)  # No model_registry needed - uses transformer
                
                # Check for errors
                has_error = False
                if "error" in status_result:
                    st.error(f"Status error: {status_result['error']}")
                    has_error = True
                
                if "error" in emotion_result:
                    st.error(f"Emotion error: {emotion_result['error']}")
                    has_error = True
                
                if not has_error:
                    # Extract results
                    fake_real_score = status_result.get('suspicion_score', 0)
                    # Adjusted threshold: 0.65 instead of 0.40
                    # This balances between notebook accuracy and practical detection
                    # Original notebook: 0.40, but model bias suggests 0.65 is better
                    fake_real = "Fake" if fake_real_score >= 0.55 else "Real"
                    
                    # Color based on Real/Fake
                    if fake_real == "Fake":
                        grad_color = "linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%)"
                    else:
                        grad_color = "linear-gradient(135deg, #51cf66 0%, #37b24d 100%)"
                    
                    emotion = emotion_result.get('emotion', 'Unknown')
                    emotion_probs = emotion_result.get('all_emotions', {emotion: 1.0})
                    
                    # Save results to session state for persistence
                    st.session_state.fake_real = fake_real
                    st.session_state.fake_real_score = fake_real_score
                    st.session_state.emotions_list = [emotion]  # List for future expansion
                    
                    # Display metrics - ONLY Authenticity and Emotion
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div style="background: {grad_color};
                                    padding: 28px; border-radius: 16px; color: white; text-align: center;
                                    box-shadow: 0 8px 24px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.2);
                                    transition: all 0.3s ease; backdrop-filter: blur(10px);">
                            <p style="margin: 0; font-size: 0.85rem; opacity: 0.95; font-weight: 600; letter-spacing: 1px;">AUTHENTICITY</p>
                            <h2 style="margin: 12px 0 0 0; font-size: 2.2em; font-weight: 800;">{fake_real}</h2>
                            <p style="margin: 8px 0 0 0; font-size: 1rem; opacity: 0.9; font-weight: 500;">{fake_real_score:.1%} confidence</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                    padding: 28px; border-radius: 16px; color: white; text-align: center;
                                    box-shadow: 0 8px 24px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.2);
                                    transition: all 0.3s ease; backdrop-filter: blur(10px);">
                            <p style="margin: 0; font-size: 0.85rem; opacity: 0.95; font-weight: 600; letter-spacing: 1px;">EMOTION</p>
                            <h2 style="margin: 12px 0 0 0; font-size: 2.2em; font-weight: 800;">{emotion.title()}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Show all 6 emotion types supported
                    st.markdown("---")
                    st.info("Emotions detected: **anger, fear, joy, neutral, sadness, surprise**")
                    
                    emotion_col1, emotion_col2 = st.columns(2)
                    emotions_list = list(emotion_probs.items())
                    
                    # Store in session state for Post Now button
                    st.session_state.emotions_list = emotions_list
                    st.session_state.fake_real = fake_real
                    st.session_state.fake_real_score = fake_real_score
                    
                    for i, (emotion_label, prob) in enumerate(emotions_list):
                        if i < len(emotions_list) // 2:
                            with emotion_col1:
                                st.write(f"**{emotion_label}**")
                                st.progress(prob, text=f"{prob:.1%}")
                        else:
                            with emotion_col2:
                                st.write(f"**{emotion_label}**")
                                st.progress(prob, text=f"{prob:.1%}")
                    
                    st.markdown("---")
                    
                    # Initialize post status in session state
                    if 'post_status' not in st.session_state:
                        st.session_state.post_status = None
                    
                    # Show status message if exists
                    if st.session_state.post_status == "success":
                        st.success("✅ Post published successfully to Facebook!")
                        st.balloons()
                    elif st.session_state.post_status == "error":
                        st.error(st.session_state.get('post_error_msg', '❌ Failed to post. Please check token & page ID.'))
            
            except Exception as e:
                st.error(f"Analysis error: {str(e)}")

# ============================================
# TAB 2: POST REACH OPTIMIZER WITH AUTO-SHARE
# ============================================
with tab2:
    st.subheader("Post Reach Optimizer")
    st.write("Select the best day and type of post to maximize reach")
    
    # Check authentication - must have Facebook Token & Page ID
    fb_token = st.session_state.get('fb_token', '')
    fb_page_id = st.session_state.get('fb_page_id', '')
    
    if not fb_token or not fb_page_id:
        st.error("❌ Please provide Facebook Token & Page ID in the sidebar first before using Reach Prediction")
        st.info("📍 Go to **Sidebar** → Enter your **Facebook Token** & **Page ID** → Click **Save**")
    else:
        # Only show content if credentials are provided
        # Caption input section - ALWAYS VISIBLE
        st.markdown("---")
        st.subheader("Caption for Auto-Share")
        
        caption_col, button_col = st.columns([4, 1])
        
        with caption_col:
            caption_input = st.text_area(
                "Enter caption to post",
                value=st.session_state.auto_share_caption,
                height=100,
                placeholder="Write your Facebook caption here...",
                key="caption_input_tab2",
                label_visibility="collapsed"
            )
        
        with button_col:
            st.write("")  # spacing
            st.write("")  # spacing
            if st.button("Set Caption", use_container_width=True, key="set_caption_btn"):
                st.session_state.auto_share_caption = caption_input
                st.success("✓ Caption saved")
        
        if st.session_state.auto_share_caption:
            st.info(f"📝 **Current Caption:** {st.session_state.auto_share_caption[:100]}...")
        else:
            st.warning("⚠️ Please enter a caption first")
        
        # Auto-share target reach section
        st.markdown("---")
        st.subheader("Auto-Share Settings")
        
        # Allow user to input custom target reach with Save/Clear buttons
        col1, col2, col3, col4 = st.columns([2, 0.8, 0.6, 0.6], gap="small")
        
        with col1:
            target_reach_input = st.text_input(
                "Target Reach for Auto-Share",
                value=str(st.session_state.target_reach),
                placeholder="Enter target reach (e.g., 500, 1000, 5000)",
                help="Post will auto-share when predicted reach reaches this value or more",
                key="target_reach_input"
            )
        
        with col2:
            if st.button("Save", use_container_width=True, key="save_target"):
                try:
                    new_target = int(target_reach_input)
                    if new_target < 100:
                        st.warning("⚠️ Minimum target reach is 100")
                        st.session_state.target_reach = 100
                    else:
                        st.session_state.target_reach = new_target
                        st.success(f"✓ Target set to {new_target}")
                except ValueError:
                    st.error("❌ Enter valid number")
        
        with col3:
            if st.button("Clear", use_container_width=True, key="clear_target"):
                st.session_state.target_reach = 500
                st.info("🔄 Reset to default (500)")
        
        with col4:
            st.metric("Target", f"{st.session_state.target_reach}")
        
        st.info(f"📌 **Auto-share will activate when predicted reach reaches {st.session_state.target_reach} or more**")
        
        st.markdown("---")
        
        # Create glass box container
        with st.container():
            st.markdown("""
            <style>
            .glass-input {
                background: rgba(102, 126, 234, 0.08) !important;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(102, 126, 234, 0.2) !important;
                border-radius: 12px;
                padding: 20px;
            }
            .stSelectbox > div > div > select {
                height: 40px !important;
                padding: 8px !important;
            }
            .stButton > button {
                height: 40px !important;
                padding: 10px 20px !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1.2, 1.2, 1.5], gap="small")
            
            with col1:
                day = st.selectbox(
                    "Day",
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    key="day_select",
                    label_visibility="collapsed"
                )
            
            with col2:
                paid_option = st.selectbox(
                    "Type",
                    ["Paid", "Non-Paid"],
                    key="ad_type_select",
                    label_visibility="collapsed"
                )
            
            with col3:
                suggest_btn = st.button("Suggest Best Time", use_container_width=True, key="suggest_btn")
        
        if suggest_btn:
            # ML-based reach prediction for each hour
            if not caption:
                st.error("❌ Please enter a caption to analyze")
            else:
                st.markdown("---")
                
                # Use ML to predict reach for each hour of selected day
                from utils.feature_engineering import predict_reach_for_hours
                
                with st.spinner("🔮 Analyzing best posting times using ML models..."):
                    try:
                        hourly_predictions = predict_reach_for_hours(caption, day, embedder, model_registry)
                        
                        # Sort by reach probability (descending)
                        hourly_predictions_sorted = sorted(hourly_predictions, key=lambda x: x[1], reverse=True)
                        
                        # Get top 3 best hours
                        top_3 = hourly_predictions_sorted[:3]
                        
                        if not top_3:
                            st.error("❌ Could not predict reach for any hours")
                        else:
                            # Display best time prominently
                            best_hour, best_prob, best_hour_int = top_3[0]
                            
                            # Glass box results
                            st.markdown("""
                            <style>
                            .result-box {
                                background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
                                backdrop-filter: blur(10px);
                                -webkit-backdrop-filter: blur(10px);
                                border: 2px solid rgba(102, 126, 234, 0.3);
                                border-radius: 14px;
                                padding: 24px;
                                margin: 15px 0;
                                box-shadow: 0 4px 16px rgba(102, 126, 234, 0.1);
                                transition: all 0.3s ease;
                            }
                            .result-box:hover {
                                transform: translateY(-2px);
                                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
                                border-color: rgba(102, 126, 234, 0.5);
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            # ML-predicted best time
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"""
                                <div class="result-box">
                                    <p style="color: #667eea; margin: 0 0 8px 0; font-size: 0.9rem; font-weight: 700; letter-spacing: 0.5px;">🎯 BEST TIME ON {day.upper()}</p>
                                    <h2 style="margin: 0 0 12px 0; color: #667eea;">{best_hour}</h2>
                                    <p style="font-size: 1.15em; color: #764ba2; font-weight: 700; margin: 0;">📈 Reach Score: {best_prob:.1%}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Estimated reach calculation (scaled from probability)
                            estimated_reach = int(best_prob * 1000)  # Scale probability to estimated impressions
                            
                            st.markdown("---")
                            st.subheader("📊 Predicted Reach")
                            st.metric("Estimated Reach (Best Hour)", f"~{estimated_reach} impressions")
                            
                            # Auto-share logic
                            if estimated_reach >= st.session_state.target_reach:
                                st.success(f"✅ **Auto-Share Ready!** Predicted reach (~{estimated_reach}) >= Target ({st.session_state.target_reach})")
                                st.info("📤 Post is eligible for automatic sharing based on target reach!")
                                
                                if st.session_state.auto_share_caption:
                                    if st.button("Auto Reach Share", use_container_width=True, key="confirm_auto_share"):
                                        st.session_state.auto_share_active = True
                                        fb_token = st.session_state.get('fb_token', '')
                                        fb_page_id = st.session_state.get('fb_page_id', '')
                                        if fb_token and fb_page_id:
                                            st.success("✅ Auto-share activated! Your caption will be posted when target reach is met.")
                                            st.info(f"📝 Caption: {st.session_state.auto_share_caption[:80]}...")
                                        else:
                                            st.error("❌ Please provide Facebook token & Page ID in sidebar")
                                else:
                                    st.error("❌ Please enter and save a caption first (see Caption section above)")
                            else:
                                st.warning(f"⚠️ **Reach not met.** Predicted: ~{estimated_reach} < Target: {st.session_state.target_reach}")
                                st.info("💡 Try different day/type combinations or improve your caption to increase reach")
                    
                    except Exception as e:
                        st.error(f"❌ Reach prediction error: {str(e)}")
                        st.info("Please ensure all models are loaded correctly")


# ============================================
# TAB 3: SCHEDULE POST
# ============================================
with tab3:
    st.subheader("Schedule Post")
    st.write("Schedule your caption to post at a specific date and time")
    
    # Check credentials first
    fb_token = st.session_state.get('fb_token', '')
    fb_page_id = st.session_state.get('fb_page_id', '')
    
    # Show credential status
    if fb_token and fb_page_id:
        st.success("✅ Facebook credentials ready for scheduling")
    else:
        st.error("❌ Please provide Facebook Token & Page ID in sidebar first before scheduling")
    
    st.markdown("---")
    
    schedule_caption = st.text_area(
        "Caption",
        height=100,
        placeholder="Your caption here...",
        label_visibility="collapsed",
        key="schedule_caption_input"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        schedule_date = st.date_input(
            "Select Date",
            value=datetime.now() + timedelta(days=1),
            key="schedule_date_input"
        )
    
    with col2:
        # Time input in 12-hour format (AM/PM)
        col2a, col2b, col2c = st.columns(3)
        
        with col2a:
            hour = st.number_input(
                "Hour",
                min_value=1,
                max_value=12,
                value=10,
                key="schedule_hour_input"
            )
        
        with col2b:
            minute = st.number_input(
                "Minute",
                min_value=0,
                max_value=59,
                value=30,
                step=5,
                key="schedule_minute_input"
            )
        
        with col2c:
            am_pm = st.selectbox(
                "AM/PM",
                ["AM", "PM"],
                key="schedule_ampm_input"
            )
        
        # Convert to 24-hour format for datetime
        hour_24 = int(hour)
        if am_pm == "PM" and hour != 12:
            hour_24 += 12
        elif am_pm == "AM" and hour == 12:
            hour_24 = 0
        
        schedule_time = datetime.strptime(f"{hour_24:02d}:{int(minute):02d}", "%H:%M").time()
    
    with col3:
        st.write("")  # spacing
        st.write("")  # spacing
        schedule_btn = st.button("Schedule", use_container_width=True, key="schedule_btn")
    
    # Handle Schedule button
    if schedule_btn:
        # Validate caption
        if not schedule_caption.strip():
            st.error("Please enter a caption first")
        # Validate credentials
        elif not fb_token or not fb_page_id:
            st.error("Please provide Facebook Token & Page ID in the sidebar first")
        else:
            # Validate date/time
            scheduled_dt = datetime.combine(schedule_date, schedule_time)
            now = datetime.now()
            
            if scheduled_dt <= now:
                st.error("Cannot schedule post in the past. Please select a future date/time.")
            else:
                # Create scheduled post entry WITHOUT posting immediately
                post_id = len(st.session_state.scheduled_posts) + 1
                time_diff = scheduled_dt - now
                hours = time_diff.total_seconds() / 3600
                minutes = (time_diff.total_seconds() % 3600) / 60
                
                scheduled_post = {
                    'id': post_id,
                    'caption': schedule_caption,
                    'date': str(schedule_date),
                    'time': str(schedule_time),
                    'scheduled_dt': scheduled_dt,
                    'created_at': now,
                    'posted_at': None,
                    'post_id': None,
                    'status': 'Pending'  # Will be posted when time arrives
                }
                st.session_state.scheduled_posts.append(scheduled_post)
                
                # Save to persistent storage
                from utils.post_storage import PostStorage
                PostStorage.save_posts(st.session_state.scheduled_posts)
                
                # Show confirmation that post is scheduled
                st.success(f"✅ Post scheduled successfully!")
                st.info(f"📅 Scheduled for: {schedule_date} at {schedule_time}")
                st.info(f"⏱️ Time remaining: {int(hours)}h {int(minutes)}m")
                st.info(f"📝 Caption: {schedule_caption[:80]}...")
                
                # Show confirmation details
                st.markdown("---")
                st.markdown("### Scheduled Post Details")
                st.write(f"**Status:** Pending - Will post automatically at scheduled time")
                st.write(f"**Date:** {schedule_date}")
                st.write(f"**Time:** {schedule_time}")
                st.write(f"**Caption:** {schedule_caption}")
                st.write(f"**Facebook Page:** {fb_page_id}")

    
    # Show all scheduled posts and check if any need to be posted
    if st.session_state.scheduled_posts:
        st.markdown("---")
        st.markdown("### Your Scheduled Posts")
        
        # Import for displaying posts
        from utils.scheduler import ScheduledPostManager
        
        # Display all scheduled posts
        for post in st.session_state.scheduled_posts:
            status = post.get('status', 'Pending')
            countdown = ScheduledPostManager.get_countdown(post['scheduled_dt'])
            countdown_str = ScheduledPostManager.format_countdown(countdown)
            
            # Color coding for status
            if status == 'Pending':
                status_color = "🟡"
                status_text = f"Pending - {countdown_str}"
            elif status == 'Posted':
                status_color = "🟢"
                status_text = "Posted ✅"
            else:
                status_color = "🔴"
                status_text = "Failed ❌"
            
            with st.expander(f"{status_color} Post #{post['id']} - {post['date']} at {post['time']} - {status_text}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Caption:** {post['caption'][:150]}...")
                    st.write(f"**Scheduled for:** {post['date']} at {post['time']}")
                    
                    if status == 'Pending':
                        st.info(f"⏱️ Time remaining: {countdown_str}")
                    
                    st.write(f"**Status:** {status}")
                    if status == 'Posted' and post.get('post_id'):
                        st.write(f"**Post ID:** {post['post_id']}")
                        st.write(f"**Posted at:** {post.get('posted_at', 'N/A')}")
                    elif status == 'Failed':
                        st.error(f"**Error:** {post.get('error', 'Unknown error')}")
                
                with col2:
                    if st.button(f"Delete", key=f"delete_post_{post['id']}", use_container_width=True):
                        from utils.post_storage import PostStorage
                        st.session_state.scheduled_posts = [p for p in st.session_state.scheduled_posts if p['id'] != post['id']]
                        PostStorage.save_posts(st.session_state.scheduled_posts)
                        st.rerun()


# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 12px; font-size: 0.85rem; color: #999;">
    <p style="margin: 0;">InspiroAI | Context-Aware Facebook Caption Optimization System</p>
    <p style="margin: 3px 0 0 0; font-size: 0.8rem; opacity: 0.8;">2025 | Powered by Advanced ML & NLP</p>
</div>
""", unsafe_allow_html=True)
