# Best Time to Post Analysis Feature - Usage Guide

## Overview
The Best Time to Post Analysis feature helps users optimize their posting strategy by analyzing engagement patterns, reach predictions, and audience behavior across different days, hours, and content types.

## 4 New API Endpoints

### 1. GET /api/best_time
**Purpose:** Get optimal posting time for a specific day with detailed analysis

**Query Parameters:**
```
day      = Day of week (monday-sunday) or leave empty for today
type     = post type (paid/non-paid), default: non-paid
content  = content type (video/image/reel/carousel/text/link), optional
audience = target audience (students/working_professionals/homemakers/entrepreneurs), optional
```

**Example Requests:**
```bash
# Best time for Friday with video content (paid)
GET /api/best_time?day=friday&type=paid&content=video

# Best time for today with reel content
GET /api/best_time?content=reel

# Best time for professionals on Monday
GET /api/best_time?day=monday&audience=working_professionals

# Best time for students with non-paid
GET /api/best_time?day=friday&audience=students&type=non-paid
```

**Response Example:**
```json
{
  "success": true,
  "data": {
    "current_day": "friday",
    "best_time": "11:00 AM",
    "next_best_time": "4:00 PM",
    "avoid_times": "12:00 AM - 7:00 AM",
    "engagement_score": 91.0,
    "expected_reach": 5974,
    "post_type": "non-paid",
    "content_type": "video",
    "day_ranking": [
      {"day": "Saturday", "score": 90},
      {"day": "Friday", "score": 85},
      {"day": "Sunday", "score": 80}
    ],
    "tips": [
      "PEAK DAY! Post during 11 AM slot for maximum reach",
      "Videos get 75% more engagement! Add captions for accessibility",
      "Organic reach is good! Build community through consistent posting"
    ]
  }
}
```

---

### 2. GET /api/all_days_analysis
**Purpose:** Compare posting performance across all 7 days of the week

**Query Parameters:**
```
type    = post type (paid/non-paid), default: non-paid
content = content type (video/image/reel/carousel/text/link), optional
```

**Example Requests:**
```bash
# Compare all days for non-paid posts with video
GET /api/all_days_analysis?type=non-paid&content=video

# Compare all days for paid posts (general content)
GET /api/all_days_analysis?type=paid

# Compare all days for reel content
GET /api/all_days_analysis?content=reel
```

**Response Example:**
```json
{
  "success": true,
  "data": [
    {
      "day": "Saturday",
      "ranking": 1,
      "engagement_score": 96.0,
      "expected_reach": 6500,
      "best_time": "12:00 PM",
      "next_best": "7:00 PM",
      "avoid_times": "12:00 AM - 8:00 AM"
    },
    {
      "day": "Friday",
      "ranking": 2,
      "engagement_score": 91.0,
      "expected_reach": 5500,
      "best_time": "11:00 AM",
      "next_best": "4:00 PM",
      "avoid_times": "12:00 AM - 7:00 AM"
    },
    {
      "day": "Sunday",
      "ranking": 3,
      "engagement_score": 86.0,
      "expected_reach": 5000,
      "best_time": "1:00 PM",
      "next_best": "6:00 PM",
      "avoid_times": "12:00 AM - 8:00 AM"
    },
    {
      "day": "Thursday",
      "ranking": 4,
      "engagement_score": 81.0,
      "expected_reach": 4500,
      "best_time": "9:30 AM",
      "next_best": "1:00 PM",
      "avoid_times": "12:00 AM - 7:00 AM"
    },
    {
      "day": "Wednesday",
      "ranking": 5,
      "engagement_score": 76.0,
      "expected_reach": 4000,
      "best_time": "10:00 AM",
      "next_best": "2:30 PM",
      "avoid_times": "12:00 AM - 7:00 AM"
    },
    {
      "day": "Tuesday",
      "ranking": 6,
      "engagement_score": 71.0,
      "expected_reach": 3500,
      "best_time": "8:30 AM",
      "next_best": "3:00 PM",
      "avoid_times": "12:00 AM - 7:00 AM"
    },
    {
      "day": "Monday",
      "ranking": 7,
      "engagement_score": 66.0,
      "expected_reach": 3000,
      "best_time": "9:00 AM",
      "next_best": "2:00 PM",
      "avoid_times": "12:00 AM - 7:00 AM"
    }
  ],
  "post_type": "non-paid",
  "content_type": "video"
}
```

---

### 3. GET /api/hourly_breakdown
**Purpose:** Get detailed hour-by-hour engagement patterns for a specific day

**Query Parameters:**
```
day = Day of week (monday-sunday), default: friday
```

**Example Requests:**
```bash
# Hourly breakdown for Friday
GET /api/hourly_breakdown?day=friday

# Hourly breakdown for Saturday
GET /api/hourly_breakdown?day=saturday

# Hourly breakdown for Monday
GET /api/hourly_breakdown?day=monday
```

**Response Example:**
```json
{
  "success": true,
  "day": "Friday",
  "hourly_breakdown": {
    "morning": {
      "hours": "6 AM - 12 PM",
      "engagement": 90,
      "best_hour": "11 AM"
    },
    "afternoon": {
      "hours": "12 PM - 5 PM",
      "engagement": 85,
      "best_hour": "4 PM"
    },
    "evening": {
      "hours": "5 PM - 10 PM",
      "engagement": 88,
      "best_hour": "7 PM"
    },
    "night": {
      "hours": "10 PM - 12 AM",
      "engagement": 70,
      "best_hour": "11 PM"
    }
  }
}
```

---

### 4. GET /api/weekly_strategy
**Purpose:** Get recommended posting strategy for the entire week based on goal

**Query Parameters:**
```
goal = Strategy goal: maximize_reach, maximize_engagement, or balanced
       (default: balanced)
```

**Available Goals:**
- `maximize_reach` - Focus on high-reach days (3 posts/week: Fri, Sat, Thu)
- `maximize_engagement` - Focus on high-engagement days (4 posts/week: Thu, Fri, Wed)
- `balanced` - Consistent posting throughout week (4 posts/week: spread across)

**Example Requests:**
```bash
# Get strategy to maximize reach
GET /api/weekly_strategy?goal=maximize_reach

# Get strategy to maximize engagement
GET /api/weekly_strategy?goal=maximize_engagement

# Get balanced strategy
GET /api/weekly_strategy?goal=balanced
```

**Response Example:**
```json
{
  "success": true,
  "goal": "maximize_reach",
  "strategy": {
    "post_days": ["friday", "saturday", "thursday"],
    "avoid_days": ["monday", "tuesday"],
    "posts_per_week": 3,
    "focus": "High-reach days with maximum visibility",
    "tips": [
      "Post on Friday, Saturday, or Thursday",
      "Use paid promotion on these days for 3x reach boost",
      "Use video or reel format for extra engagement",
      "Post at 11 AM on Friday for maximum reach"
    ]
  }
}
```

---

## Integration with Frontend

### Pro Dashboard Integration
Add a "Best Time Analysis" card in the Pro Dashboard:

```html
<div class="card">
  <h3>Best Time to Post</h3>
  <div id="best-time-result">
    <p>Best Time: <span id="best-time">Loading...</span></p>
    <p>Engagement: <span id="engagement-score">0</span>/100</p>
    <p>Expected Reach: <span id="expected-reach">0</span></p>
    <button onclick="analyzeBestTime()">Analyze Now</button>
  </div>
</div>
```

### JavaScript Example

```javascript
async function analyzeBestTime() {
  const day = document.getElementById('daySelect').value;
  const type = document.getElementById('typeSelect').value;
  const content = document.getElementById('contentSelect').value;
  
  const response = await fetch(
    `/api/best_time?day=${day}&type=${type}&content=${content}`
  );
  
  const data = await response.json();
  
  if (data.success) {
    document.getElementById('best-time').textContent = data.data.best_time;
    document.getElementById('engagement-score').textContent = data.data.engagement_score;
    document.getElementById('expected-reach').textContent = data.data.expected_reach;
  }
}
```

---

## Performance Characteristics

| Aspect | Details |
|--------|---------|
| **Response Time** | <500ms per request |
| **Accuracy** | Based on historical patterns and algorithms |
| **Data Freshness** | Real-time calculations (no caching) |
| **Scalability** | Can handle concurrent requests |
| **Database Impact** | Zero (no database queries needed) |

---

## Usage Examples

### Example 1: Finding Best Time for Video
```bash
curl "http://localhost:5000/api/best_time?day=friday&type=paid&content=video"
```
**Result:** 11:00 AM with 98% engagement, 8500+ reach

### Example 2: Comparing All Days
```bash
curl "http://localhost:5000/api/all_days_analysis?type=non-paid&content=reel"
```
**Result:** Saturday ranks #1 (96/100), then Friday (91/100), Sunday (86/100)

### Example 3: Hourly Patterns
```bash
curl "http://localhost:5000/api/hourly_breakdown?day=friday"
```
**Result:** Morning best (90 engagement), 11 AM optimal, Night lowest (70 engagement)

### Example 4: Weekly Strategy
```bash
curl "http://localhost:5000/api/weekly_strategy?goal=maximize_reach"
```
**Result:** Post 3x/week on Thu, Fri, Sat for maximum reach

---

## Tips for Users

1. **For Maximum Reach:**
   - Use `/api/weekly_strategy?goal=maximize_reach`
   - Post on Friday at 11:00 AM (peak time)
   - Use paid promotion (3x reach increase)
   - Use video or reel format

2. **For Maximum Engagement:**
   - Use `/api/weekly_strategy?goal=maximize_engagement`
   - Post on Thursday/Friday mid-morning
   - Use interactive content (polls, questions)
   - Respond to comments in first hour

3. **For Consistent Presence:**
   - Use `/api/weekly_strategy?goal=balanced`
   - Post 4x per week across different days
   - Vary content types
   - Use best times for each day

4. **Audience-Specific:**
   - Students: Post at 8 PM (evening hours)
   - Professionals: Post at 9 AM (morning)
   - General: Friday 11 AM works best

---

## Testing

Run the comprehensive test suite:

```bash
python test_best_time.py
```

This tests all 4 endpoints with various scenarios including:
- Single day analysis
- All days comparison
- Hourly breakdown
- Weekly strategies
- Paid vs non-paid comparison
- Content type performance
- Audience-specific recommendations

---

## Files Modified/Created

**New Files:**
- `src/best_time_analyzer.py` (350+ lines) - Core analyzer module
- `test_best_time.py` (200+ lines) - Test suite

**Modified Files:**
- `main.py` - Added 4 new route handlers

**Updated Documentation:**
- `README.md` - Added endpoint documentation and examples

---

## Version

**Feature Release:** v1.0.4 (November 2025)
**Module:** best_time_analyzer.py v1.0
**Total Endpoints:** 35 (31 previous + 4 new)

---

*For more details, visit: https://github.com/saifur033/InspiroAI*
