# 🚀 InspiroAI - Streamlit Cloud Deployment Guide

## Pre-Deployment Checklist

- [ ] All localhost tests passed (see LOCALHOST_TESTING.md)
- [ ] No console errors
- [ ] All features working
- [ ] Facebook API integration tested
- [ ] requirements.txt updated
- [ ] Code pushed to GitHub

---

## Step 1: Prepare GitHub Repository

### Verify Files
```
InspiroAI/
├── streamlit_app.py          ✅ Entry point (already set up)
├── production/
│   ├── app.py               ✅ Main Streamlit app
│   ├── utils/
│   │   ├── inference.py
│   │   ├── model_loader.py
│   │   └── ...
│   ├── models/
│   │   ├── emotion_model/
│   │   ├── status_model.pkl
│   │   └── ...
├── requirements.txt         ✅ Dependencies
├── .gitignore              ✅ Excludes venv, __pycache__
└── README.md               ✅ Documentation
```

### Push Latest Code
```bash
cd "d:\Important File\I\InspiroAI"
git add -A
git commit -m "Final pre-deployment: all tests passed, ready for Streamlit Cloud"
git push origin main
```

---

## Step 2: Create Streamlit Cloud Account

1. Go to: https://share.streamlit.io/
2. Sign up with GitHub
3. Authorize Streamlit to access your repos

---

## Step 3: Deploy on Streamlit Cloud

### Method 1: Web Interface (Easiest)
1. Go to: https://share.streamlit.io/
2. Click "New app"
3. Select:
   - Repository: `saifur033/InspiroAI`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
4. Click "Deploy"

### Method 2: CLI (If installed)
```bash
streamlit deploy --help
```

---

## Step 4: Configure Secrets (IMPORTANT!)

### Streamlit Secrets for Facebook API

After deployment, go to your app settings:

1. Click **⚙️ Settings** (top right of your Streamlit app)
2. Go to **Secrets** tab
3. Add your secrets:

```toml
# .streamlit/secrets.toml (LOCAL ONLY - DO NOT COMMIT)

[facebook]
api_token = "your_facebook_api_token_here"
page_id = "your_facebook_page_id_here"
```

### Access Secrets in App
In your Streamlit app:
```python
import streamlit as st

fb_token = st.secrets.get("facebook", {}).get("api_token", "")
fb_page_id = st.secrets.get("facebook", {}).get("page_id", "")
```

---

## Step 5: Update App for Cloud Secrets

### Current Sidebar Code (localhost):
```python
fb_token = st.sidebar.text_input(
    "Facebook API Token",
    value=st.session_state.fb_token,
    placeholder="Paste your token here"
)
```

### Cloud-Ready Code (Optional):
```python
# Try to get from secrets first
default_token = st.secrets.get("facebook", {}).get("api_token", "")
default_page = st.secrets.get("facebook", {}).get("page_id", "")

# But allow override
fb_token = st.sidebar.text_input(
    "Facebook API Token",
    value=default_token or st.session_state.get('fb_token', ''),
    placeholder="Paste or use secrets"
)

fb_page_id = st.sidebar.text_input(
    "Facebook Page ID",
    value=default_page or st.session_state.get('fb_page_id', ''),
    placeholder="Enter page ID or use secrets"
)
```

---

## Step 6: Deployment Verification

### Check Deployment Status
1. Go to: https://share.streamlit.io/
2. Find your app
3. Check deployment log (should show "App is running")

### Test Cloud App
1. Open your app URL (e.g., `https://share.streamlit.io/saifur033/InspiroAI/main/streamlit_app.py`)
2. Test all features:
   - [ ] Status Analyzer works
   - [ ] Emotions detected
   - [ ] Reach optimizer works
   - [ ] Tools functional
   - [ ] Facebook posting (if token provided)

---

## Common Deployment Issues

### Issue 1: ModuleNotFoundError
**Error:** `No module named 'streamlit'`

**Solution:**
- Make sure `requirements.txt` includes all dependencies
- Streamlit rebuilds environment automatically

### Issue 2: Port Already in Use
**Error:** `Port 8501 already in use`

**Solution:**
- This is managed by Streamlit Cloud (ignore locally)

### Issue 3: Model Files Not Found
**Error:** `FileNotFoundError: models/...`

**Solution:**
- Ensure all model files are in Git (not in .gitignore)
- Use relative paths: `production/models/...`

### Issue 4: Secrets Not Working
**Error:** `KeyError: 'facebook'`

**Solution:**
- Add secrets in Streamlit Cloud settings
- Restart app after adding secrets
- Use `.get()` with defaults to prevent errors

### Issue 5: Memory Limit Exceeded
**Error:** `Streamlit Cloud ran out of memory`

**Solution:**
- Optimize model loading (load once, reuse)
- Use `@st.cache_resource` for heavy models
- Reduce unnecessary data caching

---

## Performance Optimization for Cloud

### Add Caching to App
```python
import streamlit as st
from functools import lru_cache

# Cache model loading
@st.cache_resource
def load_emotion_model():
    from utils.inference import EmotionPredictor
    return EmotionPredictor()

@st.cache_resource
def load_status_model():
    from utils.inference import StatusPredictor
    return StatusPredictor()

# Use cached models
emotion_predictor = load_emotion_model()
status_predictor = load_status_model()
```

---

## Monitoring & Maintenance

### View Logs
1. Go to your app on Streamlit Cloud
2. Click "🔧 Manage app"
3. View logs and errors

### Update App
```bash
# Make changes locally
cd InspiroAI
git add -A
git commit -m "Update feature X"
git push origin main

# Streamlit Cloud auto-redeploys within 1-2 minutes
```

### Disable/Archive App
1. Go to app settings
2. Click "Archive app" to pause
3. Or click "Unlist app" to hide from directory

---

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] All tabs functional
- [ ] Status analysis works
- [ ] Emotions detected
- [ ] Reach predictions show
- [ ] Best times suggestions work
- [ ] Schedule functionality works
- [ ] Caption tools work
- [ ] Facebook integration ready (secrets configured)
- [ ] POST NOW button works (with credentials)
- [ ] Copyable examples work
- [ ] UI looks professional
- [ ] No missing models
- [ ] Response time acceptable (<5s)

---

## Useful Links

- **Streamlit Cloud**: https://share.streamlit.io/
- **Streamlit Docs**: https://docs.streamlit.io/
- **GitHub Integration**: https://docs.streamlit.io/streamlit-cloud/deploy-a-github-repo
- **Secrets Management**: https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
- **Configuration**: https://docs.streamlit.io/library/advanced-features/configuration

---

## Quick Deploy Command (After Push)

```bash
# 1. Push code
cd "d:\Important File\I\InspiroAI"
git push origin main

# 2. Wait 1-2 minutes for auto-deploy
# App URL: https://share.streamlit.io/saifur033/InspiroAI/main/streamlit_app.py

# 3. Add secrets in Streamlit Cloud dashboard
# Settings → Secrets → Add facebook token & page_id

# 4. Test in browser!
```

---

## Success! 🎉

Your InspiroAI application is now live on Streamlit Cloud!

Share your app URL: 
```
https://share.streamlit.io/saifur033/InspiroAI/main/streamlit_app.py
```

**Features Live:**
✅ Status/Authenticity Analysis
✅ Emotion Detection (6 classes)
✅ Reach Prediction
✅ Best Time Suggestions
✅ Schedule Posts
✅ Caption Tools
✅ Facebook Integration

---

Last Updated: December 5, 2025
Status: Ready for Production
