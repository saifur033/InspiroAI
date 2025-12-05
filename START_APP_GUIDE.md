# 🚀 InspiroAI - Quick Start Guide

## Windows-এ App চালানোর সবচেয়ে সহজ উপায়

### Option 1: Double-Click (সবচেয়ে সহজ) ✨
1. **`run_app.bat`** ফাইলে double-click করো
2. Automatic venv activate হবে
3. Dependencies install হবে
4. App চালু হবে 🎉

### Option 2: PowerShell-এ চালাও
```powershell
cd "d:\Important File\I\InspiroAI"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\run_app.ps1
```

### Option 3: Manual চালানো
```powershell
# Navigate to project
cd "d:\Important File\I\InspiroAI"

# Activate venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Navigate to production folder
cd production

# Run app
python -m streamlit run app.py
```

---

## App কখন চালু হয়েছে জানবো কি?

✅ এই message দেখলে app চালু হয়েছে:
```
Local URL: http://localhost:8501
Network URL: http://192.168.0.169:8501
```

---

## Browser-এ কিভাবে access করবো?

1. **Local (Same Computer)**: http://localhost:8501
2. **Network (Other Device)**: http://192.168.0.169:8501

---

## সাধারণ সমস্যা ও সমাধান

### Problem: "python command not found"
**Solution**: Python properly install আছে কি check করো
```powershell
python --version
```

### Problem: "venv activate not working"
**Solution**: .venv folder আছে কি check করো
```powershell
Test-Path ".\.venv"
```

### Problem: "app.py not found"
**Solution**: production folder-এ আছে কি check করো
```powershell
Test-Path ".\production\app.py"
```

### Problem: Streamlit port already in use
**Solution**: অন্য streamlit process বন্ধ করো
```powershell
Get-Process streamlit | Stop-Process -Force
```

---

## Features ✨

✅ Status Analyzer - Caption authenticity detection
✅ Reach Optimizer - Best time to post suggestions
✅ Schedule Post - Schedule posts for future
✅ Tools - Caption generator, optimizer, hashtag generator
✅ Facebook Integration - Direct posting to Facebook

---

## Technical Stack

- **Framework**: Streamlit 1.35.0
- **ML Models**: HuggingFace, scikit-learn, XGBoost, CatBoost
- **Language**: Python 3.10+
- **API**: Facebook Graph API v18.0

---

## Help & Support

📧 GitHub: https://github.com/saifur033/InspiroAI
📝 Issues: Report problems on GitHub issues

---

**Last Updated**: December 5, 2025
**Version**: 1.0 Production Ready
