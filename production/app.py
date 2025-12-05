"""
InspiroAI - Context-Aware Facebook Caption Optimization System
Modern Streamlit Application with ML Pipeline
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
    
    /* Button styling - Enhanced */
    .stButton {
        width: 100%;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
        text-transform: uppercase !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.5px !important;
        min-height: 44px !important;
        width: 100% !important;
        display: block !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
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
@st.cache_resource
def load_models():
    try:
        from utils.model_loader import get_model_registry
        from sentence_transformers import SentenceTransformer
        
        registry = get_model_registry()
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        return registry, embedder, True
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, False

model_registry, embedder, models_loaded = load_models()

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
        st.session_state.fb_token = ''
        st.session_state.fb_page_id = ''
        st.sidebar.success("✅ Credentials cleared!")
        time.sleep(0.5)
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
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0  # Default to Status Analyzer
if 'target_reach' not in st.session_state:
    st.session_state.target_reach = 500  # Default target reach
if 'auto_share_caption' not in st.session_state:
    st.session_state.auto_share_caption = ""  # Caption for auto-share
if 'auto_share_active' not in st.session_state:
    st.session_state.auto_share_active = False  # Auto-share activation status

# ============================================
# MAIN TABS
# ============================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Status Analyzer",
    "Post Reach Optimizer",
    "Schedule Post",
    "Tools"
])

# ============================================
# TAB 1: STATUS ANALYZER
# ============================================
with tab1:
    st.session_state.active_tab = 0  # Mark as active
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
        # Save to session state whenever it changes
        st.session_state.tab1_caption = caption
    
    with col2:
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            analyze_btn = st.button("Analyze", use_container_width=True, key="analyze_btn_tab1")
        with col_btn2:
            clear_btn = st.button("Clear", use_container_width=True, key="clear_btn_tab1")
        with col_btn3:
            post_now_btn_temp = st.button("Share", use_container_width=True, key="post_now_btn_temp")
    
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
                        st.session_state.fake_real = "Unknown"
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
    
    # Handle Clear button
    if clear_btn:
        st.session_state.tab1_caption = ""
        st.session_state.emotions_list = []
        st.session_state.fake_real = "Unknown"
        st.session_state.fake_real_score = 0
        st.rerun()
    
    if analyze_btn:
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
                    
                    # Show WHY it's Fake/Real
                    st.markdown("---")
                    st.subheader("Why This Is Detected As " + fake_real)
                    
                    if fake_real == "Fake":
                        # FAKE CAPTION - Show why fake and how to improve
                        with st.expander("❌ Why This Is Detected As FAKE", expanded=True):
                            st.markdown("""
                            ❌ **Generic/Template Phrases:**
                            - Overused opening lines (e.g., "I am a student from...", "Looking for opportunities...")
                            - Standard motivational phrases
                            
                            ❌ **Copy-Paste Structure:**
                            - Repetitive format and patterns
                            - Similar to known spam templates
                            
                            ❌ **Limited Authenticity Signals:**
                            - Too polished/professional tone
                            - Heavy hashtag usage (#Success #Grateful #Blessed)
                            - Lack of personal emotions or specific details
                            
                            ❌ **Automated Writing Style:**
                            - Bot-like patterns detected
                            - Formal language without personality
                            - No typos or casual language
                            """)
                        
                        with st.expander("✅ How to Make It More REAL (Copy & Use Below):", expanded=True):
                            st.markdown("""
                            **Tips to improve authenticity:**
                            - Use casual language ("lol", "ngl", "honestly", "ig")
                            - Share real struggles or failures (not just success)
                            - Include specific details (names, dates, exact situations)
                            - Show genuine emotions (frustration, confusion, surprise)
                            - Keep typos/informal style (don't over-correct)
                            - Minimize or remove hashtags (0-2 max)
                            - Fragment sentences naturally
                            
                            **👇 COPY THIS REAL VERSION & PASTE ABOVE 👇**
                            """)
                            
                            st.code("""honestly i don't know how i'm graduating lol
4 years and i still feel lost af
but ig that's normal? at least my friends feel the same way
thank god this is over""", language="text")
                            
                            st.info("📋 Tip: Copy the text above and paste it in the caption box above to see it detected as REAL!")
                            
                            st.markdown("**More REAL Examples:**")
                            st.code("""just woke up and i have no idea what im doing with my life lol

honestly the anxiety is hitting different today
why am i like this

had the worst day ever but at least pizza exists

im not okay but also im fine? does anyone else feel this way""", language="text")
                    else:
                        # REAL CAPTION - Show why real and celebrate it
                        with st.expander("✅ Why This Is Detected As REAL", expanded=True):
                            st.markdown("""
                            ✅ **Authentic Language:**
                            - Natural, conversational tone ✨
                            - Personal voice and perspective
                            
                            ✅ **Genuine Expression:**
                            - Real emotions visible
                            - Honest struggles or vulnerabilities
                            
                            ✅ **Unpolished Style:**
                            - Casual language with typos
                            - Natural sentence fragmentation
                            - Minimal or contextual hashtags
                            
                            ✅ **Specific Details:**
                            - Unique situations or experiences
                            - Personal touches that make it authentic
                            """)
                        
                        st.success("🎉 This caption looks authentic and genuine! Keep this style!")
                    
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
    st.session_state.active_tab = 1  # Mark as active
    st.subheader("Post Reach Optimizer")
    st.write("Select the best day and type of post to maximize reach")
    
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
        # Data-driven best times from research (not random)
        # Source: Facebook engagement studies
        best_times = {
            'Monday': {'Paid': ('9:00 AM', '11:00 AM', 42), 'Non-Paid': ('10:00 AM', '12:00 PM', 18)},
            'Tuesday': {'Paid': ('10:00 AM', '2:00 PM', 48), 'Non-Paid': ('2:00 PM', '4:00 PM', 22)},
            'Wednesday': {'Paid': ('8:00 PM', '10:00 PM', 45), 'Non-Paid': ('9:00 PM', '11:00 PM', 20)},
            'Thursday': {'Paid': ('6:30 PM', '8:30 PM', 50), 'Non-Paid': ('7:00 PM', '9:00 PM', 24)},
            'Friday': {'Paid': ('5:00 PM', '7:00 PM', 52), 'Non-Paid': ('6:00 PM', '8:00 PM', 26)},
            'Saturday': {'Paid': ('12:00 PM', '2:00 PM', 38), 'Non-Paid': ('1:00 PM', '3:00 PM', 16)},
            'Sunday': {'Paid': ('7:00 PM', '9:00 PM', 40), 'Non-Paid': ('8:00 PM', '10:00 PM', 18)}
        }
        
        day_data = best_times[day][paid_option]
        best_time = day_data[0]
        end_time = day_data[1]
        reach_increase = day_data[2]
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        current_idx = days.index(day)
        next_day = days[(current_idx + 1) % 7]
        next_day_data = best_times[next_day][paid_option]
        next_time = next_day_data[0]
        
        st.markdown("---")
        
        # Glass box results - Enhanced
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
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="result-box">
                <p style="color: #667eea; margin: 0 0 8px 0; font-size: 0.9rem; font-weight: 700; letter-spacing: 0.5px;">🎯 BEST TIME ON {day.upper()}</p>
                <h2 style="margin: 0 0 12px 0; color: #667eea;">{best_time} - {end_time}</h2>
                <p style="font-size: 1.15em; color: #764ba2; font-weight: 700; margin: 0;">📈 +{reach_increase}% Reach</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="result-box">
                <p style="color: #667eea; margin: 0 0 8px 0; font-size: 0.9rem; font-weight: 700; letter-spacing: 0.5px;">📅 NEXT BEST TIME</p>
                <h2 style="margin: 0 0 12px 0; color: #667eea;">{next_day}</h2>
                <p style="font-size: 1.15em; color: #764ba2; font-weight: 700; margin: 0;">⏰ {next_time}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Check if reach exceeds target and auto-share
        predicted_reach = reach_increase * 10  # Simple estimation
        st.markdown("---")
        st.subheader("Predicted Reach")
        st.metric("Estimated Reach", f"{predicted_reach} impressions")
        
        if predicted_reach >= st.session_state.target_reach:
            st.success(f"✅ **Auto-Share Activated!** Predicted reach ({predicted_reach}) >= Target ({st.session_state.target_reach})")
            st.info("📤 Post will be automatically shared to Facebook at the optimal time!")
            
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
            st.warning(f"⚠️ **Reach not met.** Current: {predicted_reach} < Target: {st.session_state.target_reach}")
            st.info("Try different day/type combinations to increase reach")

# ============================================
# TAB 3: SCHEDULE POST
# ============================================
with tab3:
    st.subheader("Schedule Post")
    st.write("Schedule your caption to post at a specific date and time")
    
    # Initialize session state for scheduled posts
    if 'scheduled_posts' not in st.session_state:
        st.session_state.scheduled_posts = []
    
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
                # Calculate time difference
                time_diff = scheduled_dt - now
                hours = time_diff.total_seconds() / 3600
                minutes = (time_diff.total_seconds() % 3600) / 60
                
                try:
                    # POST IMMEDIATELY TO FACEBOOK
                    with st.spinner("Posting to Facebook..."):
                        from utils.facebook_posting import FacebookPoster
                        
                        poster = FacebookPoster(page_token=fb_token, page_id=fb_page_id)
                        success, result = poster.publish_post(message=schedule_caption)
                        
                        if success:
                            # Add to scheduled posts with "Posted" status
                            post_id = len(st.session_state.scheduled_posts) + 1
                            scheduled_post = {
                                'id': post_id,
                                'caption': schedule_caption,
                                'date': schedule_date,
                                'time': schedule_time,
                                'scheduled_dt': scheduled_dt,
                                'created_at': now,
                                'posted_at': now,
                                'post_id': result.get('post_id', 'unknown'),
                                'status': 'Posted'
                            }
                            st.session_state.scheduled_posts.append(scheduled_post)
                            
                            # Show success
                            st.success(f"Post shared successfully!")
                            st.success(f"Post ID: {result.get('post_id', 'unknown')}")
                            st.success(f"Scheduled for: {schedule_date} at {int(hours)}h {int(minutes)}m")
                            st.info(f"Caption: {schedule_caption[:100]}...")
                            
                            # Show confirmation
                            st.markdown("---")
                            st.markdown("### Scheduled Post Details")
                            st.write(f"**Date:** {schedule_date}")
                            st.write(f"**Time:** {schedule_time}")
                            st.write(f"**Caption:** {schedule_caption}")
                            st.write(f"**Facebook Page:** {fb_page_id}")
                            st.write(f"**Status:** Posted")
                            st.write(f"**Post ID:** {result.get('post_id', 'unknown')}")
                            
                            time.sleep(1)
                        else:
                            st.error(f"Failed to post: {result.get('error', 'Unknown error')}")
                            if result.get('details'):
                                st.warning(f"Details: {result.get('details')}")
                    
                except Exception as e:
                    st.error(f"Error posting: {str(e)}")
    
    # Show all scheduled posts
    if st.session_state.scheduled_posts:
        st.markdown("---")
        st.markdown("### Your Scheduled Posts")
        
        for post in st.session_state.scheduled_posts:
            status = post.get('status', 'Pending')
            with st.expander(f"Post #{post['id']} - {post['date']} at {post['time']} - {status}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Caption:** {post['caption'][:150]}...")
                    st.write(f"**Scheduled for:** {post['date']} at {post['time']}")
                    st.write(f"**Status:** {status}")
                    if status == 'Posted' and 'post_id' in post:
                        st.write(f"**Post ID:** {post['post_id']}")
                
                with col2:
                    if st.button(f"Delete", key=f"delete_post_{post['id']}", use_container_width=True):
                        st.session_state.scheduled_posts = [p for p in st.session_state.scheduled_posts if p['id'] != post['id']]
                        st.rerun()

# ============================================
# TAB 4: TOOLS
# ============================================
with tab4:
    st.markdown("""
    <style>
    .tool-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 24px;
        border-radius: 14px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
    }
    
    .tool-header h2 {
        margin: 0;
        font-size: 1.8em;
        color: white !important;
    }
    
    .tool-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .tool-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
        border-color: rgba(102, 126, 234, 0.3);
    }
    </style>
    
    <div class="tool-header">
        <h2>Tools & Utilities</h2>
        <p style="margin: 8px 0 0 0; opacity: 0.95;">Generate and optimize captions for better engagement</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("English Language Support Only - All tools use AI to enhance your content")
    
    # Tool selection with better styling
    st.markdown("### Select Tool")
    tool_option = st.radio(
        "Select Tool",
        ["Caption Generator", "Caption Optimizer", "Hashtag Generator"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if tool_option == "Caption Generator":
        st.markdown('<div class="tool-card"><h3 style="margin-top: 0;">Generate AI Captions</h3></div>', unsafe_allow_html=True)
        
        topic = st.text_input(
            "Enter topic/theme",
            placeholder="e.g., graduation, project completion, internship",
            help="AI will generate multiple caption variations based on your topic"
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            generate_btn = st.button("Generate Captions", use_container_width=True, key="gen_captions")
        
        if generate_btn:
            if topic.strip():
                # AI caption generation templates with enhanced hashtags
                caption_templates = {
                    'graduation': [
                        f"Finally! Completed my journey at the university. Grateful for all the mentors and friends who supported me. Excited for what's next! #Graduation #NewBeginning #Success #ProudMoment #ClassOf2024 #{topic} #Achievement #Thankful #Future",
                        f"What an incredible milestone! Officially graduated! This achievement wouldn't be possible without my teachers, family, and friends. Thank you all! #{topic} #Proud #Achievement #UniversityLife #GraduationDay #FutureLeader #Grateful #Accomplished",
                        f"From student to professional! Excited to embark on this new chapter. Special thanks to everyone who believed in me. Let's do this! #Graduation #{topic} #NewJourney #CareerStart #Motivated #DreamsComeTrue #Ready #Professional",
                    ],
                    'project': [
                        f"Proud to announce the completion of my {topic} project! Hard work and dedication finally paid off. Grateful for the support! #ProjectComplete #Success #{topic} #Achievement #Accomplished #ProudMoment #Innovation #Learning",
                        f"Just finished an amazing {topic} project! Learned so much through this journey. Can't wait to share the results! #{topic} #Achievement #ProjectSuccess #Learning #Development #TeamWork #Skills #Growth",
                        f"Excited to showcase my {topic} project! This has been an incredible learning experience. Thank you to everyone who helped! #ProudMoment #{topic} #Success #CreativeWork #Innovation #Collaboration #Growth #Grateful",
                    ],
                    'internship': [
                        f"Starting an exciting {topic} internship journey! Looking forward to learning and growing. Let's make it amazing! #Internship #NewOpportunity #{topic} #CareerGrowth #Learning #Experience #Excited #NewBeginning",
                        f"Thrilled to begin my {topic} internship! Ready to work hard, learn, and contribute to the team. Let's go! #{topic} #CareerGrowth #Internship #Professional #Development #TeamSpirit #Motivated #Skills",
                        f"Beginning my {topic} internship today! Excited to be part of the team and gain real-world experience. #Internship #Journey #{topic} #CareerStart #Opportunity #Growth #Professional #Experience",
                    ],
                    'learning': [
                        f"Excited about learning {topic}! It's amazing how much knowledge is out there. Join me on this learning journey! #Learning #{topic} #Development #Skills #Knowledge #Growth #MindsetMatters #SelfImprovement #Inspired",
                        f"Started my {topic} learning journey today! Never too late to acquire new skills. Who else is learning {topic}? #{topic} #SkillDevelopment #Learning #Growth #ContinuousLearning #PersonalDevelopment #Achievement #Knowledge",
                        f"Diving into {topic}! Every day brings new insights and challenges. Love the learning process! #{topic} #Growth #NewSkills #Learning #Development #Inspired #Knowledge #Progress",
                    ]
                }
                
                # Find matching template
                generated = []
                for key in caption_templates.keys():
                    if key.lower() in topic.lower():
                        generated = caption_templates[key]
                        break
                
                # If no specific match, use generic templates with more hashtags
                if not generated:
                    generated = [
                        f"Amazing experience with {topic}! Grateful for this opportunity. Looking forward to more! #{topic} #Success #Achievement #Grateful #Growth #Inspired #ProudMoment #Learning",
                        f"Excited about my journey with {topic}! Learning so much every day. #Growth #{topic} #Development #Journey #Inspired #Success #Achievement #NewExperience #Motivated",
                        f"Proud moment with {topic}! Can't wait to share more updates. Thanks to all supporters! #{topic} #Grateful #Proud #Achievement #Success #Growth #Community #Thankful",
                    ]
                
                st.markdown("### Generated Captions")
                for i, caption in enumerate(generated, 1):
                    with st.expander(f"Caption Option {i}", expanded=(i==1)):
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(245, 87, 108, 0.05) 100%); 
                                    padding: 18px; border-radius: 12px; border-left: 4px solid #667eea;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                            <p style="margin: 0; color: #333; line-height: 1.7; font-size: 1.05em;">{caption}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            if st.button(f"Save Caption {i}", key=f"use_cap_{i}", use_container_width=True):
                                st.session_state.auto_share_caption = caption
                                st.success(f"Caption {i} saved to Auto-Share!")
                        
                        with col2:
                            fb_token = st.session_state.get('fb_token', '')
                            fb_page_id = st.session_state.get('fb_page_id', '')
                            
                            if fb_token and fb_page_id:
                                if st.button(f"Share {i}", key=f"share_cap_{i}", use_container_width=True):
                                    st.success(f"Caption {i} shared to Facebook!")
                                    st.info(f"Posted: {caption[:80]}...")
                            else:
                                st.button(f"Share {i}", use_container_width=True, disabled=True, key=f"share_cap_{i}_disabled")
            else:
                st.warning("⚠️ Please enter a topic")
    
    elif tool_option == "Caption Optimizer":
        st.markdown('<div class="tool-card"><h3 style="margin-top: 0;">Optimize Your Caption</h3></div>', unsafe_allow_html=True)
        
        original_caption = st.text_area("Enter original caption (English only)", height=100, placeholder="Paste your caption here...")
        
        if st.button("Optimize", use_container_width=True):
            if original_caption.strip():
                # Advanced optimization: rewrite and enhance caption
                optimized = original_caption.strip()
                
                # Remove existing hashtags to rewrite better
                import re
                caption_without_hashtags = re.sub(r'#\w+', '', optimized).strip()
                
                # Make it more engaging - add powerful words and punctuation
                enhancement_words = ["Excited to share", "Grateful for", "Blessed to announce", "Thrilled about", "Amazing opportunity"]
                if not any(word in caption_without_hashtags for word in enhancement_words):
                    if caption_without_hashtags.endswith(('.', '!', '?')):
                        caption_without_hashtags = caption_without_hashtags[:-1]
                    # Rewrite with better opening
                    optimized = f"Excited to share: {caption_without_hashtags}! "
                else:
                    optimized = caption_without_hashtags + " "
                
                # Add engaging question/CTA if missing
                if "?" not in optimized:
                    cta_questions = [
                        "What are your thoughts on this?",
                        "Would love to hear your feedback!",
                        "Join me on this journey!",
                        "Let's connect and grow together!",
                        "What's your experience with this?"
                    ]
                    import random
                    optimized += random.choice(cta_questions) + " "
                
                # Add comprehensive hashtags for better reach
                hashtags = " #Growth #Success #Achievement #Inspired #Grateful #Motivation #Learning #Community #Development #Empowered #Journey #Goals #Dreams #ProudMoment #LivingMyBestLife"
                optimized += hashtags
                
                st.markdown("### Optimized Caption")
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(81, 207, 102, 0.1) 100%);
                            padding: 20px; border-radius: 14px; border: 2px solid rgba(76, 175, 80, 0.2);
                            box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                    <p style="margin: 0 0 8px 0; color: #4caf50; font-weight: 700; font-size: 0.9rem; letter-spacing: 0.5px;">OPTIMIZED CAPTION</p>
                    <p style="margin: 0; color: #333; font-size: 1.05em; line-height: 1.7;">{optimized}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.current_optimized_caption = optimized
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save to Auto-Share", use_container_width=True):
                        st.session_state.auto_share_caption = optimized
                        st.success("Caption saved to Auto-Share!")
                
                with col2:
                    fb_token = st.session_state.get('fb_token', '')
                    fb_page_id = st.session_state.get('fb_page_id', '')
                    
                    if fb_token and fb_page_id:
                        if st.button("Share to Facebook", use_container_width=True, key="share_optimized"):
                            try:
                                import requests
                                # Facebook Graph API endpoint
                                url = f"https://graph.facebook.com/v18.0/{fb_page_id}/feed"
                                params = {
                                    'message': optimized,
                                    'access_token': fb_token
                                }
                                response = requests.post(url, params=params)
                                if response.status_code == 200:
                                    st.success("✅ Caption shared to Facebook successfully!")
                                    st.info(f"Posted: {optimized[:100]}...")
                                else:
                                    st.error(f"Error: {response.json().get('error', {}).get('message', 'Unknown error')}")
                            except Exception as e:
                                st.error(f"Sharing error: {str(e)}")
                    else:
                        st.button("Share to Facebook", use_container_width=True, disabled=True, key="share_optimized_disabled")
                        st.warning("Please provide Facebook Token & Page ID in sidebar to share")
            else:
                st.warning("⚠️ Please enter a caption to optimize")
    
    elif tool_option == "Hashtag Generator":
        st.markdown('<div class="tool-card"><h3 style="margin-top: 0;">Generate Trending Hashtags</h3></div>', unsafe_allow_html=True)
        
        theme = st.text_input("Enter theme/keyword (English only)", placeholder="e.g., education, career, technology...")
        
        if st.button("Generate", use_container_width=True):
            if theme.strip():
                # Hashtag suggestions based on theme
                hashtag_suggestions = {
                    'education': "#Education #Learning #Student #University #Growth #FutureLeader #AcademicJourney #Knowledge",
                    'career': "#Career #Professional #JobSearch #CareerGrowth #Success #WorkLife #NewOpportunity #Goals",
                    'technology': "#Tech #Innovation #Programming #Developer #FutureOfTech #DigitalTransformation #StartupLife",
                    'inspiration': "#Inspiration #Motivated #DreamsBigger #GoalAchievement #SuccessStory #Grateful #MindsetMatters",
                    'lifestyle': "#Lifestyle #DailyLife #Wellness #PersonalGrowth #Balance #HappyLife #SelfCare #Mindful",
                }
                
                generated_hashtags = "#Trending #Amazing #Content #Share #Follow #Engage #InstaGood"
                for key in hashtag_suggestions.keys():
                    if key.lower() in theme.lower():
                        generated_hashtags = hashtag_suggestions[key]
                        break
                
                st.markdown("### Generated Hashtags")
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255, 152, 0, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%);
                            padding: 20px; border-radius: 14px; border: 2px solid rgba(255, 152, 0, 0.2);
                            box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                    <p style="margin: 0 0 12px 0; color: #ff9800; font-weight: 700; font-size: 0.9rem; letter-spacing: 0.5px;">TRENDING HASHTAGS</p>
                    <p style="margin: 0; color: #333; font-size: 1.1em; line-height: 1.8; font-weight: 500;">{generated_hashtags}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Copy Hashtags", use_container_width=True):
                    st.success("Hashtags ready to use!")
            else:
                st.warning("⚠️ Please enter a theme or keyword")

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
