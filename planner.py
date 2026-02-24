<<<<<<< HEAD
import os
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai
from gpt_prompt import full_trip_prompt

# --- Load environment variables ---
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
GEMINI_TIMEOUT = int(os.getenv("GEMINI_TIMEOUT", "45"))

# --- Configure Gemini client ---
genai.configure(api_key=GEMINI_API_KEY)

# --- Verify available models and fallback if needed ---
try:
    available_models = [m.name for m in genai.list_models()]
    if GEMINI_MODEL not in available_models:
        print(f"⚠ Model '{GEMINI_MODEL}' not found. Falling back to 'gemini-2.5-flash-lite'")
        GEMINI_MODEL = "gemini-2.5-flash-lite"
except Exception as e:
    print(f"⚠ Failed to list models: {str(e)}")
    GEMINI_MODEL = "gemini-2.5-flash-lite"

model = genai.GenerativeModel(GEMINI_MODEL)

# --- Debug logging ---
print(f"🔧 Using Gemini model: {GEMINI_MODEL}")
api_key_prefix = (GEMINI_API_KEY[:8] + "...") if GEMINI_API_KEY else "(missing)"
print(f"🔐 API key prefix: {api_key_prefix}")

def generate_itinerary(trip: dict, weather_info=None) -> list:
    """
    Generate a structured travel itinerary using Gemini and your handcrafted prompt.
    Returns a list of day blocks with time slots, titles, descriptions, and optional map links.
    """

    # --- Use custom prompt if provided ---
    custom_prompt = trip.get("custom_prompt")
    if custom_prompt:
        try:
            response = model.generate_content(custom_prompt)
            print("🧪 Gemini raw output:\n", response.text.strip())
            blocks = parse_structured_itinerary(response.text.strip())
            return blocks if blocks else fallback_block(response.text.strip())
        except Exception as e:
            return error_block(str(e))

    # --- Extract trip details ---
    def to_date(val):
        if isinstance(val, datetime):
            return val.date()
        if isinstance(val, str):
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except:
                return datetime.today().date()
        return val

    source = trip.get("source", "")
    destination = trip.get("destination", "")
    num_people = trip.get("num_people", 1)
    start_date = to_date(trip.get("start_date", ""))
    end_date = to_date(trip.get("end_date", ""))
    travel_modes = trip.get("travel_modes", [])
    trip_style = trip.get("trip_style", [])
    budget_level = trip.get("budget_level", "")
    budget_amount = trip.get("budget_amount", 0.0)
    weather_text = str(weather_info or "")

    trip_length = max(1, (end_date - start_date).days + 1)
    try:
        budget_value = float(budget_amount)
    except (ValueError, TypeError):
        budget_value = 0.0
    budget_per_day = round(budget_value / trip_length, 2)

    if not isinstance(travel_modes, list):
        travel_modes = [str(travel_modes)]
    if isinstance(trip_style, str):
        trip_style = [trip_style]

    # --- Build prompt using gpt_prompt.py ---
    prompt = full_trip_prompt(
        {
            "source": source,
            "destination": destination,
            "num_people": num_people,
            "start_date": start_date,
            "end_date": end_date,
            "travel_modes": travel_modes,
            "trip_style": trip_style,
            "budget_level": budget_level,
        },
        weather_text,
        budget_per_day
    )

    print("🧠 Prompt sent to Gemini:\n", prompt)

    # --- Generate content ---
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        print("🧪 Gemini raw output:\n", raw_text)

        # Fallback if Gemini skips checklist or safety tips
        if "Packing Checklist" not in raw_text or "Safety Tips" not in raw_text:
            print("⚠️ Gemini skipped a section — generating fallback content...")
            fallback_prompt = f"""
You forgot one or more sections in the travel itinerary for {destination}.
Provide only the missing sections below, formatted in Markdown.
Each must have at least 5 bullet points.

### 🎒 Packing Checklist
### 🛡️ Safety Tips
"""
            extra_response = model.generate_content(fallback_prompt)
            raw_text += f"\n\n{extra_response.text.strip()}"

        blocks = parse_structured_itinerary(raw_text)
        return blocks if blocks else fallback_block(raw_text)

    except Exception as e:
        return error_block(str(e))

def parse_structured_itinerary(text: str) -> list:
    import re

    days = []
    current_day = None

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Match Day headers like "### 🗓️ Day 1: ..."
        if re.match(r"(?i)^#+\s*🗓️?\s*day\s*\d+", line):
            if current_day:
                days.append(current_day)
            current_day = {"day": line, "slots": []}
            continue

        # Match Gemini-style blocks: **Morning (9:00 AM - 12:00 PM):** Activity
        gemini_match = re.match(r"^\*\*(.*?)\((.*?)\)\s*:\*\*\s*(.*)", line)
        if gemini_match and current_day:
            label = gemini_match.group(1).strip()
            time_range = gemini_match.group(2).strip()
            title = gemini_match.group(3).strip()
            current_day["slots"].append({
                "time": f"{label} ({time_range})",
                "title": title,
                "description": ""
            })
            continue

        # Match emoji-style blocks: **🕒 9:00 AM — Visit Mall Road**
        emoji_match = re.match(r"^\*\*🕒\s*(.*?)\s*—\s*(.*?)\*\*", line)
        if emoji_match and current_day:
            time = emoji_match.group(1).strip()
            title = emoji_match.group(2).strip()
            current_day["slots"].append({
                "time": time,
                "title": title,
                "description": ""
            })
            continue

        # Match description lines
        if current_day and current_day["slots"]:
            current_day["slots"][-1]["description"] += line + "\n"

    if current_day:
        days.append(current_day)

    for day in days:
        for slot in day["slots"]:
            slot["description"] = slot["description"].strip()

    return days

def fallback_block(raw_text: str) -> list:
    """
    Return a fallback block with raw Gemini output if parsing fails.
    """
    return [{
        "day": "Unparsed",
        "slots": [{
            "time": "",
            "title": "Raw Gemini Output",
            "description": raw_text
        }]
    }]

def error_block(message: str) -> list:
    """
    Return a structured error block.
    """
    return [{
        "day": "Error",
        "slots": [{
            "time": "",
            "title": "Generation Failed",
            "description": message
        }]
=======
import os
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai
from gpt_prompt import full_trip_prompt

# --- Load environment variables ---
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
GEMINI_TIMEOUT = int(os.getenv("GEMINI_TIMEOUT", "45"))

# --- Configure Gemini client ---
genai.configure(api_key=GEMINI_API_KEY)

# --- Verify available models and fallback if needed ---
try:
    available_models = [m.name for m in genai.list_models()]
    if GEMINI_MODEL not in available_models:
        print(f"⚠ Model '{GEMINI_MODEL}' not found. Falling back to 'gemini-2.5-flash-lite'")
        GEMINI_MODEL = "gemini-2.5-flash-lite"
except Exception as e:
    print(f"⚠ Failed to list models: {str(e)}")
    GEMINI_MODEL = "gemini-2.5-flash-lite"

model = genai.GenerativeModel(GEMINI_MODEL)

# --- Debug logging ---
print(f"🔧 Using Gemini model: {GEMINI_MODEL}")
api_key_prefix = (GEMINI_API_KEY[:8] + "...") if GEMINI_API_KEY else "(missing)"
print(f"🔐 API key prefix: {api_key_prefix}")

def generate_itinerary(trip: dict, weather_info=None) -> list:
    """
    Generate a structured travel itinerary using Gemini and your handcrafted prompt.
    Returns a list of day blocks with time slots, titles, descriptions, and optional map links.
    """

    # --- Use custom prompt if provided ---
    custom_prompt = trip.get("custom_prompt")
    if custom_prompt:
        try:
            response = model.generate_content(custom_prompt)
            print("🧪 Gemini raw output:\n", response.text.strip())
            blocks = parse_structured_itinerary(response.text.strip())
            return blocks if blocks else fallback_block(response.text.strip())
        except Exception as e:
            return error_block(str(e))

    # --- Extract trip details ---
    def to_date(val):
        if isinstance(val, datetime):
            return val.date()
        if isinstance(val, str):
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except:
                return datetime.today().date()
        return val

    source = trip.get("source", "")
    destination = trip.get("destination", "")
    num_people = trip.get("num_people", 1)
    start_date = to_date(trip.get("start_date", ""))
    end_date = to_date(trip.get("end_date", ""))
    travel_modes = trip.get("travel_modes", [])
    trip_style = trip.get("trip_style", [])
    budget_level = trip.get("budget_level", "")
    budget_amount = trip.get("budget_amount", 0.0)
    weather_text = str(weather_info or "")

    trip_length = max(1, (end_date - start_date).days + 1)
    try:
        budget_value = float(budget_amount)
    except (ValueError, TypeError):
        budget_value = 0.0
    budget_per_day = round(budget_value / trip_length, 2)

    if not isinstance(travel_modes, list):
        travel_modes = [str(travel_modes)]
    if isinstance(trip_style, str):
        trip_style = [trip_style]

    # --- Build prompt using gpt_prompt.py ---
    prompt = full_trip_prompt(
        {
            "source": source,
            "destination": destination,
            "num_people": num_people,
            "start_date": start_date,
            "end_date": end_date,
            "travel_modes": travel_modes,
            "trip_style": trip_style,
            "budget_level": budget_level,
        },
        weather_text,
        budget_per_day
    )

    print("🧠 Prompt sent to Gemini:\n", prompt)

    # --- Generate content ---
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        print("🧪 Gemini raw output:\n", raw_text)

        # Fallback if Gemini skips checklist or safety tips
        if "Packing Checklist" not in raw_text or "Safety Tips" not in raw_text:
            print("⚠️ Gemini skipped a section — generating fallback content...")
            fallback_prompt = f"""
You forgot one or more sections in the travel itinerary for {destination}.
Provide only the missing sections below, formatted in Markdown.
Each must have at least 5 bullet points.

### 🎒 Packing Checklist
### 🛡️ Safety Tips
"""
            extra_response = model.generate_content(fallback_prompt)
            raw_text += f"\n\n{extra_response.text.strip()}"

        blocks = parse_structured_itinerary(raw_text)
        return blocks if blocks else fallback_block(raw_text)

    except Exception as e:
        return error_block(str(e))

def parse_structured_itinerary(text: str) -> list:
    import re

    days = []
    current_day = None

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Match Day headers like "### 🗓️ Day 1: ..."
        if re.match(r"(?i)^#+\s*🗓️?\s*day\s*\d+", line):
            if current_day:
                days.append(current_day)
            current_day = {"day": line, "slots": []}
            continue

        # Match Gemini-style blocks: **Morning (9:00 AM - 12:00 PM):** Activity
        gemini_match = re.match(r"^\*\*(.*?)\((.*?)\)\s*:\*\*\s*(.*)", line)
        if gemini_match and current_day:
            label = gemini_match.group(1).strip()
            time_range = gemini_match.group(2).strip()
            title = gemini_match.group(3).strip()
            current_day["slots"].append({
                "time": f"{label} ({time_range})",
                "title": title,
                "description": ""
            })
            continue

        # Match emoji-style blocks: **🕒 9:00 AM — Visit Mall Road**
        emoji_match = re.match(r"^\*\*🕒\s*(.*?)\s*—\s*(.*?)\*\*", line)
        if emoji_match and current_day:
            time = emoji_match.group(1).strip()
            title = emoji_match.group(2).strip()
            current_day["slots"].append({
                "time": time,
                "title": title,
                "description": ""
            })
            continue

        # Match description lines
        if current_day and current_day["slots"]:
            current_day["slots"][-1]["description"] += line + "\n"

    if current_day:
        days.append(current_day)

    for day in days:
        for slot in day["slots"]:
            slot["description"] = slot["description"].strip()

    return days

def fallback_block(raw_text: str) -> list:
    """
    Return a fallback block with raw Gemini output if parsing fails.
    """
    return [{
        "day": "Unparsed",
        "slots": [{
            "time": "",
            "title": "Raw Gemini Output",
            "description": raw_text
        }]
    }]

def error_block(message: str) -> list:
    """
    Return a structured error block.
    """
    return [{
        "day": "Error",
        "slots": [{
            "time": "",
            "title": "Generation Failed",
            "description": message
        }]
>>>>>>> d3ec141 (Initial commit: RoamGenie AI Travel Planner with Map and PDF support)
    }]