# 🚀 InspiroAI - সহজ শুরু করার গাইড

## প্রথমবার সেটআপ (একবার করলেই হবে)

### Step 1: Command Prompt খুলুন
- Windows কী + R চাপুন
- `cmd` টাইপ করুন এবং Enter চাপুন

### Step 2: সঠিক ফোল্ডারে যান
```
cd "d:\Important File\I\InspiroAI"
```

### Step 3: Python environment setup করুন
```
python -m venv .venv
```

### Step 4: Environment activate করুন
```
.venv\Scripts\activate.bat
```

### Step 5: সব dependencies install করুন (একবার)
```
pip install -r requirements.txt
```

এটি দেখতে দেবে:
```
✓ Successfully installed streamlit pandas numpy ...
```

---

## প্রতিদিন App চালানো (Step 1-2 এর পরে)

### নিয়ম:
1. Command Prompt খুলুন
2. `cd "d:\Important File\I\InspiroAI"` করুন
3. এটি রান করুন:

```
.venv\Scripts\activate.bat && cd production && python -m streamlit run app.py
```

অথবা সহজ উপায়ে **`run_app.bat`** double-click করুন!

---

## App চালু হয়েছে কি জানবো?

এই message দেখলে app চালু:
```
Local URL: http://localhost:8501
```

তারপর Browser-এ যান: **http://localhost:8501**

---

## সমস্যা হলে?

### Command not found?
Windows-এ Python install আছে কি check করুন:
```
python --version
```

### Dependencies missing?
পুনরায় install করুন:
```
pip install -r requirements.txt --force-reinstall
```

### Port already in use?
অন্য terminal এ run করুন বা port change করুন:
```
python -m streamlit run app.py --server.port 8502
```

---

## QuickStart Commands

```powershell
# এক লাইনে সবকিছু
cd "d:\Important File\I\InspiroAI" && .venv\Scripts\activate.bat && cd production && python -m streamlit run app.py
```

---

**Ready to go!** 🎉

Last Updated: December 5, 2025
