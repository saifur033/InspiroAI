"""
db_manager.py — InspiroAI Database Manager v10.0 (2025 Final Stable)

🔥 Supports:
- Caption AI (Rewrite / SEO / Emotion / FakeReal / Hashtags / Comments)
- Image Caption
- Trending History (optional future)
- Token Save System
- Facebook Scheduler
- Auto-Share Posting
- Auto Migration (No DB delete needed)
"""

import json
import os
import sqlite3
from threading import Lock
from typing import Dict, Any

# ---------------------------------------------------------
# 📌 DB PATH
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
_db_lock = Lock()

# ---------------------------------------------------------
# 🛡 SAFE JSON DUMP
# ---------------------------------------------------------
def safe_json(value):
    try:
        return json.dumps(value, ensure_ascii=False)
    except:
        return "{}"

# ---------------------------------------------------------
# 🧱 INIT + MIGRATE DB
# ---------------------------------------------------------
def init_db():
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # ----------------------------------------------------
        # TABLE 1 : CAPTIONS
        # ----------------------------------------------------
        c.execute("""
            CREATE TABLE IF NOT EXISTS captions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caption TEXT,
                optimized_caption TEXT,
                tone_used TEXT,
                rewrite_type TEXT,
                emotion_top TEXT,
                emotion_distribution TEXT,
                seo_score INTEGER,
                seo_difference INTEGER,
                seo_grade TEXT,
                seo_suggestion TEXT,
                fake_real TEXT,
                real_percent REAL,
                fake_percent REAL,
                real_new REAL,
                fake_new REAL,
                hashtags TEXT,
                comments TEXT,
                reach_prediction TEXT,
                image_caption TEXT,
                image_url TEXT,
                language_detected TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ----------------------------------------------------
        # AUTO-MIGRATION (Add missing columns safely)
        # ----------------------------------------------------
        required_cols = {
            "tone_used": "TEXT",
            "rewrite_type": "TEXT",
            "seo_difference": "INTEGER DEFAULT 0",
            "seo_suggestion": "TEXT",
            "fake_real": "TEXT",
            "real_new": "REAL DEFAULT 0",
            "fake_new": "REAL DEFAULT 0",
            "image_caption": "TEXT",
            "reach_prediction": "TEXT",
            "comments": "TEXT"
        }

        existing = {col[1] for col in c.execute("PRAGMA table_info(captions)")}

        for col, type_ in required_cols.items():
            if col not in existing:
                try:
                    c.execute(f"ALTER TABLE captions ADD COLUMN {col} {type_}")
                    print(f"🆕 Added column → {col}")
                except Exception as e:
                    print(f"⚠️ Could not add {col}: {e}")

        # ----------------------------------------------------
        # TABLE 2 : TOKEN SETTINGS
        # ----------------------------------------------------
        c.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_token TEXT,
                page_id TEXT,
                dev_mode TEXT
            )
        """)

        # ----------------------------------------------------
        # TABLE 3 : FB SCHEDULE POSTS
        # ----------------------------------------------------
        c.execute("""
            CREATE TABLE IF NOT EXISTS schedule_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_text TEXT,
                post_time TEXT,
                post_type TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)

        # ----------------------------------------------------
        # TABLE 4 : AUTO SHARE SETTINGS
        # ----------------------------------------------------
        c.execute("""
            CREATE TABLE IF NOT EXISTS auto_share (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reach_goal INTEGER,
                caption TEXT
            )
        """)

        # ----------------------------------------------------
        # TABLE 5 : TREND HISTORY (persistent)
        # Create this table while the connection is still open to avoid "closed database" issues
        # ----------------------------------------------------
        try:
            c.execute("""
                CREATE TABLE IF NOT EXISTS trend_history (
                    topic TEXT PRIMARY KEY,
                    last_score INTEGER,
                    computed_score REAL,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        except Exception as e:
            print("⚠️ Could not ensure trend_history table exists:", e)

        conn.commit()
        conn.close()
        print("[OK] DB Initialized + Fully Migrated (v10.0)")

# ---------------------------------------------------------
# 🧩 INSERT CAPTION RECORD
# ---------------------------------------------------------
def insert_caption(record: Dict[str, Any]):
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        try:
            c.execute("""
                INSERT INTO captions (
                    caption, optimized_caption, tone_used, rewrite_type,
                    emotion_top, emotion_distribution,
                    seo_score, seo_difference, seo_grade, seo_suggestion,
                    fake_real, real_percent, fake_percent, real_new, fake_new,
                    hashtags, comments, reach_prediction,
                    image_caption, image_url, language_detected
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.get("caption"),
                record.get("optimized_caption"),
                record.get("tone_used"),
                record.get("rewrite_type"),
                record.get("emotion_top"),
                safe_json(record.get("emotion_distribution")),
                record.get("seo_score"),
                record.get("seo_difference"),
                record.get("seo_grade"),
                record.get("seo_suggestion"),
                safe_json(record.get("fake_real")),
                record.get("real_percent"),
                record.get("fake_percent"),
                record.get("real_new"),
                record.get("fake_new"),
                safe_json(record.get("hashtags")),
                safe_json(record.get("comments")),
                safe_json(record.get("reach_prediction")),
                record.get("image_caption"),
                record.get("image_url"),
                record.get("language_detected")
            ))
            conn.commit()
        except Exception as e:
            print("❌ Insert Caption Error:", e)
        finally:
            conn.close()

# ---------------------------------------------------------
# TOKEN SYSTEM
# ---------------------------------------------------------
def save_token(api_token, page_id, dev_mode):
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM tokens")
        c.execute("INSERT INTO tokens(api_token, page_id, dev_mode) VALUES (?, ?, ?)",
                  (api_token, page_id, dev_mode))
        conn.commit()
        conn.close()

def save_token_data(api_token, page_id, dev_mode):
    return save_token(api_token, page_id, dev_mode)

def get_token():
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT api_token, page_id, dev_mode FROM tokens LIMIT 1")
        row = c.fetchone()
        conn.close()
        return row

# ---------------------------------------------------------
# SCHEDULE POST SYSTEM
# ---------------------------------------------------------
def save_schedule(text, time, type_):
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO schedule_posts(post_text, post_time, post_type) VALUES (?, ?, ?)",
            (text, time, type_)
        )
        conn.commit()
        conn.close()

def get_pending_schedule():
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, post_text, post_time, post_type FROM schedule_posts WHERE status='pending'")
        rows = c.fetchall()
        conn.close()
        return rows

def mark_schedule_sent(id_):
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE schedule_posts SET status='sent' WHERE id=?", (id_,))
        conn.commit()
        conn.close()

# ---------------------------------------------------------
# AUTO SHARE SETTINGS
# ---------------------------------------------------------
def save_auto_share(goal, caption):
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM auto_share")
        c.execute("INSERT INTO auto_share(reach_goal, caption) VALUES (?, ?)",
                  (goal, caption))
        conn.commit()
        conn.close()

def get_auto_share():
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT reach_goal, caption FROM auto_share LIMIT 1")
        row = c.fetchone()
        conn.close()
        return row


# ---------------------------------------------------------
# Trend history helpers
# ---------------------------------------------------------
def save_trend_point(topic, last_score, computed_score):
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("REPLACE INTO trend_history(topic, last_score, computed_score, last_seen) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                      (topic, int(last_score), float(computed_score)))
            conn.commit()
        except Exception as e:
            print('❌ save_trend_point error:', e)
        finally:
            conn.close()


def get_trend_point(topic):
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("SELECT last_score, computed_score, last_seen FROM trend_history WHERE topic=?", (topic,))
            row = c.fetchone()
            conn.close()
            if not row:
                return None
            return {"last_score": row[0], "computed_score": row[1], "last_seen": row[2]}
        except Exception as e:
            conn.close()
            print('❌ get_trend_point error:', e)
            return None


def get_all_trend_points():
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("SELECT topic, last_score, computed_score, last_seen FROM trend_history")
            rows = c.fetchall()
            conn.close()
            return [{"topic": r[0], "last_score": r[1], "computed_score": r[2], "last_seen": r[3]} for r in rows]
        except Exception as e:
            conn.close()
            print('❌ get_all_trend_points error:', e)
            return []


def get_all_tokens():
    """Get all saved Facebook tokens from database"""
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            # tokens table columns: api_token, page_id, dev_mode
            c.execute("SELECT page_id, api_token, dev_mode FROM tokens")
            rows = c.fetchall()
            conn.close()
            return [{"page_id": r[0], "token": r[1], "dev_mode": r[2]} for r in rows]
        except Exception as e:
            conn.close()
            print('❌ get_all_tokens error:', e)
            return []
