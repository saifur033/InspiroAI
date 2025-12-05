# 🧪 InspiroAI - Localhost Testing Guide

## সব Features Test করার Checklist

### ✅ Pre-Test Setup
- [ ] App localhost-এ চালানো হয়েছে (`http://localhost:8501`)
- [ ] Browser refresh করেছি (Ctrl+F5)
- [ ] সব pages accessible আছে

---

## 📊 Tab 1: Status Analyzer

### Test Case 1: FAKE Caption Detection
**Input:**
```
Check this amazing opportunity! Don't miss out! 
Click here for FREE money! Limited time offer!
Act now before it's gone! #opportunity #money #free
```

**Expected Output:**
- ❌ FAKE detection (50%+ score)
- Red/orange color indicator
- Reasons shown: "generic phrases", "copy-paste structure", "urgency tactics"
- "How to Make It More REAL" section visible
- Copyable REAL example in code block

**Test:**
- [ ] Caption enters correctly
- [ ] ANALYZE button works
- [ ] Emotion detected (should show: JOY, SURPRISE)
- [ ] Fake/Real score shows
- [ ] Proper expanders show/hide

---

### Test Case 2: REAL Caption Detection
**Input:**
```
honestly i still can't believe i graduated lol / spent 4 years and still don't know what i'm doing but here we are 🎓 / grateful for the people who kept me sane through this
```

**Expected Output:**
- ✅ REAL detection (<50% score)
- Green color indicator
- Reasons: "authentic language", "natural struggles", "genuine emotion"
- "Why This Is Detected As REAL" section
- Celebration message: "🎉 This caption looks authentic..."
- NO "How to improve" section

**Test:**
- [ ] Different content for REAL vs FAKE
- [ ] Success message shows
- [ ] Emotion detection accurate
- [ ] Score range 20-80%

---

### Test Case 3: CLEAR Button
**Steps:**
1. Enter caption
2. Click ANALYZE
3. Click CLEAR button
4. Caption field should empty
5. All results should reset

**Test:**
- [ ] Caption field empties
- [ ] Emotions clear
- [ ] Status resets
- [ ] Explanations disappear

---

## 💰 Tab 2: Post Reach Optimizer

### Test Case 1: Auto-Share Settings
**Steps:**
1. Enter caption in "Caption for Auto-Share" field
2. Click SET CAPTION
3. Change Target Reach (e.g., 300)
4. Click SAVE button

**Expected:**
- [ ] Caption saves (✓ message)
- [ ] Target reach updates
- [ ] Display shows current target

---

### Test Case 2: Best Time Suggestion
**Steps:**
1. Select Day: Friday
2. Select Type: Paid
3. Click "Suggest Best Time"

**Expected Output:**
- [ ] Shows Friday best time (5:00 PM - 7:00 PM)
- [ ] Shows +52% reach
- [ ] Shows next best day/time
- [ ] Predicted reach calculated
- [ ] Auto-share trigger logic works

---

### Test Case 3: Auto-Share Activation
**Steps:**
1. Set caption
2. Set target reach: 100
3. Suggest best time
4. If predicted reach >= target, click "Auto Reach Share"

**Expected:**
- [ ] Shows activation message
- [ ] Caption preview shows
- [ ] Status logged (if credentials present)

---

## 📅 Tab 3: Schedule Post

### Test Case 1: Schedule Validation
**Steps:**
1. Enter caption: "Test schedule post"
2. Select future date
3. Select time
4. Click SCHEDULE

**Expected:**
- [ ] Shows scheduled message
- [ ] Date/time format correct
- [ ] Caption preview shows

---

### Test Case 2: Past Date Validation
**Steps:**
1. Select past date (e.g., yesterday)
2. Click SCHEDULE

**Expected:**
- [ ] Error message: "Cannot schedule in past"
- [ ] Post not scheduled

---

## 🛠️ Tab 4: Tools

### Test Case 1: Caption Generator
**Steps:**
1. Enter topic: "graduation"
2. Click GENERATE CAPTIONS

**Expected:**
- [ ] 3 caption options show
- [ ] Each has proper hashtags
- [ ] "Save Caption" button works
- [ ] Saves to auto-share tab

---

### Test Case 2: Caption Optimizer
**Steps:**
1. Paste caption: "just finished project"
2. Click OPTIMIZE

**Expected:**
- [ ] Optimized version shows
- [ ] Better hashtags added
- [ ] CTAs included
- [ ] "Save to Auto-Share" works

---

### Test Case 3: Hashtag Generator
**Steps:**
1. Enter theme: "technology"
2. Click GENERATE

**Expected:**
- [ ] Relevant hashtags show
- [ ] At least 8+ hashtags
- [ ] Professional & trendy

---

## 🔐 Sidebar: Facebook Integration

### Test Case 1: Token Entry
**Steps:**
1. Paste Facebook API Token
2. Paste Facebook Page ID
3. Click SAVE

**Expected:**
- [ ] Token field accepts paste (not hidden as password)
- [ ] Page ID field accepts paste
- [ ] Save button confirms
- [ ] Data persists on refresh

---

### Test Case 2: Token Persistence
**Steps:**
1. Save credentials
2. Refresh page (F5)
3. Check sidebar

**Expected:**
- [ ] Credentials still visible
- [ ] Session state preserved
- [ ] Can clear and reset

---

## 📤 Facebook Posting Tests

### Test Case 1: POST NOW (Tab 1)
**Prerequisites:**
- [ ] Valid Facebook token in sidebar
- [ ] Valid Page ID in sidebar
- [ ] Caption analyzed

**Steps:**
1. Click POST NOW button
2. Wait for response

**Expected:**
- [ ] Success message: "✅ Post published..."
- [ ] Balloons animation
- [ ] Posted caption preview
- [ ] Button remains visible
- [ ] Can post again

---

### Test Case 2: Share from Caption Generator
**Steps:**
1. Generate caption
2. Click "Share" button (if credentials exist)

**Expected:**
- [ ] Confirms to Facebook
- [ ] Success/error message

---

## 🎨 UI/UX Tests

### Visual Tests
- [ ] Gradient backgrounds render correctly
- [ ] Colors are consistent (purple/blue theme)
- [ ] Text is readable (contrast OK)
- [ ] Buttons highlight on hover
- [ ] Expandable sections work

---

### Responsive Tests
- [ ] Layout works at different browser widths
- [ ] Mobile view doesn't break (if testing)
- [ ] Buttons clickable on different sizes
- [ ] Text wraps properly

---

### Performance Tests
- [ ] Page loads in <3 seconds
- [ ] ANALYZE completes in <5 seconds
- [ ] No lag when switching tabs
- [ ] Smooth button animations

---

## ❌ Error Handling Tests

### Test Case 1: Missing Facebook Credentials
**Steps:**
1. Clear Facebook token & Page ID
2. Try POST NOW

**Expected:**
- [ ] Error: "Please provide Facebook token & Page ID"
- [ ] Post doesn't happen
- [ ] User can try again

---

### Test Case 2: Empty Caption
**Steps:**
1. Click ANALYZE without caption

**Expected:**
- [ ] Warning/error message
- [ ] No analysis attempted

---

### Test Case 3: Network Error Simulation
**Steps:**
1. Disconnect internet (if testing)
2. Try POST NOW

**Expected:**
- [ ] Proper error message
- [ ] App doesn't crash
- [ ] Can retry

---

## 📋 Final Checklist Before Deploy

- [ ] All 4 tabs work
- [ ] ANALYZE detects FAKE/REAL correctly
- [ ] Different UI for FAKE vs REAL
- [ ] POST NOW creates posts
- [ ] Copyable examples work
- [ ] Emotions show 6 classes
- [ ] Best times are data-driven
- [ ] No console errors
- [ ] No missing dependencies
- [ ] Facebook integration ready
- [ ] Token/ID persist correctly
- [ ] All buttons functional
- [ ] No broken links
- [ ] UI looks professional

---

## 🚀 Ready to Deploy?

When ALL tests pass ✅ :

1. Update `requirements.txt` (should be already OK)
2. Create `streamlit_app.py` at root (symlink to production/app.py)
3. Push to GitHub
4. Deploy to Streamlit Cloud
5. Add Streamlit secrets for FB token/ID

---

## Test Results Template

```
=================================
LOCALHOST TEST RESULTS
=================================

Date: __________
Time: __________

Tab 1 - Status Analyzer: [ PASS / FAIL ]
Tab 2 - Reach Optimizer: [ PASS / FAIL ]
Tab 3 - Schedule Post: [ PASS / FAIL ]
Tab 4 - Tools: [ PASS / FAIL ]

Features Tested: _____
Features Failed: _____

Ready for Deploy: [ YES / NO ]

Notes:
_____________________________________
_____________________________________
```

---

**Good luck with testing!** 🍀

Last Updated: December 5, 2025
