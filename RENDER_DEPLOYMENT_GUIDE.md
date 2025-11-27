# 🚀 InspiroAI Deployment Guide

## Deploy to Render

### Step 1: Create Render Account
- Go to https://render.com
- Sign up with GitHub account
- Authorize Render to access your GitHub repos

### Step 2: Create New Web Service
1. Click **"New"** → **"Web Service"**
2. Select repository: **`saifur033/InspiroAI`**
3. Choose branch: **`main`**

### Step 3: Configure Deployment Settings

**Name:** `inspiroai` (or your preferred name)

**Runtime:** Python 3.11

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
```

**Environment Variables:**
Add these in **Environment** tab:
```
FLASK_ENV=production
DEBUG=False
```

### Step 4: Deploy
- Click **"Create Web Service"**
- Render will automatically build and deploy
- Wait for logs showing "Connected to <your-app>.onrender.com"

### Step 5: Access Your App
- Your app will be live at: `https://<your-app>.onrender.com`
- Example: `https://inspiroai.onrender.com`

---

## Key Files for Render Deployment

✅ **Procfile** - Deployment instructions
✅ **wsgi.py** - WSGI entry point for Gunicorn
✅ **runtime.txt** - Python version (3.11.9)
✅ **requirements.txt** - All Python dependencies

All files are already committed to GitHub!

---

## Common Issues & Fixes

### Issue: "ModuleNotFoundError"
**Solution:** Make sure all imports in `main.py` are available in `requirements.txt`

### Issue: Port binding error
**Solution:** Already fixed with WSGI entry point (`wsgi.py`)

### Issue: Build timeout
**Solution:** Render has generous timeouts, but if it fails:
- Check `requirements.txt` for problematic packages
- Ensure all files are committed (not in `.gitignore`)

### Issue: App starts but 502 Bad Gateway
**Solution:** Check Render logs tab for specific errors

---

## Monitoring Your App

Once deployed on Render:
1. Go to your dashboard at https://dashboard.render.com
2. Click your service to see:
   - **Logs** - Real-time application logs
   - **Metrics** - CPU, Memory usage
   - **Events** - Deployment history

---

## Redeploy After Updates

After pushing changes to GitHub, Render will automatically redeploy:
1. Make changes locally
2. `git add .`
3. `git commit -m "Your message"`
4. `git push origin main`
5. Render detects push and rebuilds automatically

Or manually trigger:
- Dashboard → Your Service → Click **"Redeploy"** button

---

## Features Once Deployed

✅ **21 API Endpoints** - All working
✅ **Caption-Specific Detection** - Emotion & Authenticity analysis
✅ **Multi-language** - English & Bengali support
✅ **SQLite Database** - Auto-initialized
✅ **Free & Pro Modes** - All features included
✅ **Comment Helper** - AI-powered comment generation
✅ **Responsive UI** - 7 HTML templates

---

**Your app is production-ready! Deploy now! 🎉**
