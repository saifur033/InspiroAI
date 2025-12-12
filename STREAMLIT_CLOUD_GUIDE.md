# Streamlit Cloud Deployment Guide

## Problem: App shows UI but no predictions

**Common causes:**
1. Models not loading
2. Embedder timeout
3. Missing model files
4. Path issues on Streamlit Cloud

## Solution

### Step 1: Verify Models Are Uploaded

Ensure these files exist in your GitHub repo:
```
production/
  models/
    ├── status_rf.joblib        (Required)
    ├── status_xgb.joblib       (Required)
    ├── status_lgb.joblib       (Required)
    ├── status_meta.json        (Required)
    ├── status_style_features.joblib
    ├── reach_voting.joblib
    ├── reach_ohe.joblib
    ├── reach_scaler.joblib
    ├── reach_thresh.joblib
    └── reach_meta.json
```

### Step 2: Set Up Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select your GitHub repo (saifur033/InspiroAI)
4. Set main file path to: `production/app.py`
5. Click "Deploy"

### Step 3: Add Secrets (Optional)

For Facebook integration, add secrets:
1. Go to App Settings (gear icon)
2. Click "Secrets"
3. Add your secrets:
```toml
[facebook]
api_token = "your_token_here"
page_id = "your_page_id_here"
```

### Step 4: Check Logs

If still not working:
1. Click "Manage app" (gear icon)
2. Click "View logs"
3. Look for error messages starting with `[ERROR]`

## Testing

### Local Testing (Works)
```bash
cd production
streamlit run app.py
```
Access at: http://localhost:8501

### Streamlit Cloud Testing
1. Check terminal logs for model loading errors
2. Try refreshing the page (might help with embedder timeout)
3. Verify model files are in GitHub repo

## Debugging Script

Run this to test locally:
```bash
cd production
python test_models.py
```

This will show:
- ✓ Model paths are correct
- ✓ Files exist
- ✓ Models load successfully
- ✓ Predictions work

## If Still Not Working

### Option A: Check Memory
Streamlit Cloud free tier has limited memory. Your models might be too large.

### Option B: Reduce Model Size
Simplify models or use smaller versions:
- DistilRoBERTa instead of RoBERTa
- Smaller ensemble
- Quantized models

### Option C: Use Alternative
Deploy to:
- Heroku
- AWS EC2
- DigitalOcean
- Render.com

## Expected Output

When working correctly:
1. App loads in ~15 seconds
2. Models load successfully (check terminal)
3. User enters caption
4. Click "Analyze"
5. Predictions appear instantly
6. All 3 tabs work (Status, Reach, Schedule)

## Contact Support

If models still don't load:
1. Check GitHub issue: https://github.com/saifur033/InspiroAI/issues
2. Provide terminal logs
3. Describe what you see vs what's expected

---

**Last Updated:** December 12, 2025
