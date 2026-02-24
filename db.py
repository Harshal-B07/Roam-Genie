import sqlite3
import json
from typing import List, Dict, Any

DB_PATH = "roamgenie.db"

# --- Initialize database with auto-migration ---
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        # Create table if it doesn't exist
        c.execute("""
            CREATE TABLE IF NOT EXISTS itineraries (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
        """)
        conn.commit()

        # Get existing columns
        c.execute("PRAGMA table_info(itineraries)")
        existing_cols = [row[1] for row in c.fetchall()]

        # Define required columns
        required_cols = {
            "user_email": "TEXT",
            "trip_data": "TEXT",
            "itinerary_text": "TEXT",
            "checklist": "TEXT",
            "safety_tips": "TEXT"
        }

        # Add missing columns
        for col, col_type in required_cols.items():
            if col not in existing_cols:
                c.execute(f"ALTER TABLE itineraries ADD COLUMN {col} {col_type}")
                print(f"[DB] Added missing column: {col}")

        conn.commit()

# --- Add itinerary ---
def add_itinerary(user_email: str, trip_data: Dict[str, Any], itinerary_text: List[Dict[str, Any]], checklist: Dict[str, List[str]], safety_tips: List[str]):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO itineraries (user_email, trip_data, itinerary_text, checklist, safety_tips)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_email,
            json.dumps(trip_data, default=str),
            json.dumps(itinerary_text),
            json.dumps(checklist),
            json.dumps(safety_tips)
        ))
        conn.commit()

# --- Get itineraries for a user ---
def get_itineraries(user_email: str) -> List[Dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT id, trip_data, itinerary_text, checklist, safety_tips
            FROM itineraries
            WHERE user_email = ?
            ORDER BY id DESC
        """, (user_email,))
        rows = c.fetchall()

    results = []
    for itinerary_id, trip_data_json, itinerary_text_json, checklist_json, tips_json in rows:
        try:
            trip_data = json.loads(trip_data_json)
        except Exception:
            trip_data = {}

        try:
            itinerary_text = json.loads(itinerary_text_json)
        except Exception:
            itinerary_text = []

        try:
            checklist = json.loads(checklist_json)
        except Exception:
            checklist = {}

        try:
            safety_tips = json.loads(tips_json)
        except Exception:
            safety_tips = []

        results.append({
            "id": itinerary_id,
            "trip_data": trip_data,
            "itinerary_text": itinerary_text,
            "checklist": checklist,
            "safety_tips": safety_tips
        })

    return results

# --- Delete an itinerary by ID ---
def delete_itinerary(itinerary_id: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM itineraries WHERE id = ?", (itinerary_id,))
        conn.commit()
        return c.rowcount > 0