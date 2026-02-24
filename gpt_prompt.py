<<<<<<< HEAD
from datetime import datetime, date
from typing import Any, Dict

def _to_date_safe(value):
    """Return a date object if possible, else return the original value."""
    if value is None:
        return ""
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, fmt).date()
            except Exception:
                pass
        try:
            return datetime.fromisoformat(value).date()
        except Exception:
            return value
    return value

def full_trip_prompt(trip: Dict[str, Any], weather_parsed: str, budget_per_day: float) -> str:
    start = _to_date_safe(trip.get("start_date", ""))
    end = _to_date_safe(trip.get("end_date", ""))

    try:
        nights = (end - start).days if hasattr(start, "day") and hasattr(end, "day") else ""
    except Exception:
        nights = ""

    currency = trip.get("currency", "USD")
    destination = str(trip.get("destination", "Unknown")).split(",")[0].strip()
    travel_modes = [str(mode).lower() for mode in trip.get("travel_modes", []) or []]

    travel_mode_note = ""
    if travel_modes:
        allowed_modes = ", ".join(travel_modes)
        travel_mode_note = f"\nUse only the following travel modes: {allowed_modes}. Do not include any other form of transport."

    travel_modes_joined = ", ".join(trip.get("travel_modes", [])) if trip.get("travel_modes") else "N/A"
    trip_style_joined = ", ".join(trip.get("trip_style", [])) if trip.get("trip_style") else "N/A"

    return f"""
You are an expert travel planner and well-travelled blogger who creates realistic, inspiring itineraries that feel handcrafted.

Create a customized trip titled:  
**Your {destination} Adventure**  
_A handcrafted journey through culture, charm, and hidden gems._

Plan a trip from {trip.get('source', 'Unknown source')} to {trip.get('destination', 'Unknown destination')} for {trip.get('num_people', 1)} people.  
Trip dates: {start} to {end} ({nights} nights)  
Weather snapshot: {weather_parsed}  
Preferred travel modes: {travel_modes_joined}  
Trip style: {trip_style_joined}  
Budget level: {trip.get('budget_level', 'N/A')} (approx. {budget_per_day} {currency} per day){travel_mode_note}

Preferences:  
- Tone: friendly, engaging, and written like a local sharing insider knowledge  
- Dietary: {trip.get('dietary_pref', 'none')}  
- Must-include: {trip.get('must_include_list', 'none')}  
- Avoid: {trip.get('avoid_list', 'none')}

Local logistics:  
- Typical opening hours: {trip.get('opening_hours_hint', 'N/A')}  
- Known closures: {trip.get('closures_hint', 'N/A')}  
- Sunrise/Sunset: {trip.get('sunrise', 'N/A')} / {trip.get('sunset', 'N/A')}  
- Suggested neighborhood clustering: {trip.get('neighborhood_clusters', 'N/A')}

---

### 🧭 Structure your response using **exactly these headings in this order**:
Do not rename, omit, or merge them.

1. **### 🗓️Your **{destination}** Itinerary**  
   - Include a clear per-day breakdown (Day 1, Day 2, etc.)
   - Each day must include Morning, Afternoon, and Evening sections with time ranges.
   - Each block: 1 popular anchor + 1 hidden gem (when possible)
   - Include local food recommendations respecting dietary preferences.
   - Logical flow (minimize travel time).
   - End each day with a “Daily Travel Tip”.

2. **### 🎒 Packing Checklist**  
   - Must have at least 3 categories (e.g., Essentials, Weather Gear, Electronics, etc.)
   - Each category must have 3–6 bullet points.
   - Tailor suggestions to the trip’s weather, duration, and activities.

3. **### 🛡️ Safety Tips**  
   - Include 5–10 concise, destination-specific tips.
   - Cover local etiquette, health/safety, and transit or scam warnings.

✅ Always include both the “🎒 Packing Checklist” and “🛡️ Safety Tips” sections — never omit them.
"""



def day_edit_prompt(
    trip,
    weather_parsed,
    prev_day_content,
    next_day_content,
    day_num,
    day_date,
    trip_summary
):
    currency = trip.get("currency", "USD")
    travel_modes = [mode.lower() for mode in trip.get("travel_modes", []) or []]

    travel_mode_note = ""
    if travel_modes:
        allowed_modes = ", ".join(travel_modes)
        travel_mode_note = f"\nUse only the following travel modes: {allowed_modes}. Do not include any other form of transport."

    return f"""
You are an expert travel planner and well-travelled blogger. You will regenerate ONLY one day of an existing trip itinerary.

Trip context:  
From {trip['source']} to {trip['destination']} for {trip['num_people']} people  
Trip dates: {trip['start_date']} to {trip['end_date']}  
Weather snapshot: {weather_parsed}  
Preferred travel modes: {', '.join(trip['travel_modes'])}  
Trip style: {', '.join(trip['trip_style'])}  
Budget level: {trip['budget_level']} (approx. {trip.get('budget_per_day', 'N/A')} {currency} per day){travel_mode_note}

Existing itinerary summary:  
{trip_summary}

Previous day’s plan:  
{prev_day_content}

Next day’s plan:  
{next_day_content}

Regenerate Day {day_num} ({day_date}) with:  
- Morning / Afternoon / Evening blocks with time ranges  
- Each block: 1 popular anchor + 1 hidden gem (when possible)  
- Include local food recs (respect dietary prefs)  
- Logical flow from previous day to next day  
- No repeating venues from any other day in the trip  
- End with a one-line “Daily Travel Tip”  
- Keep tone/style consistent with the rest of the trip

Formatting:  
Markdown for the day’s plan (same style as full itinerary)  
=======
from datetime import datetime, date
from typing import Any, Dict

def _to_date_safe(value):
    """Return a date object if possible, else return the original value."""
    if value is None:
        return ""
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, fmt).date()
            except Exception:
                pass
        try:
            return datetime.fromisoformat(value).date()
        except Exception:
            return value
    return value

def full_trip_prompt(trip: Dict[str, Any], weather_parsed: str, budget_per_day: float) -> str:
    start = _to_date_safe(trip.get("start_date", ""))
    end = _to_date_safe(trip.get("end_date", ""))

    try:
        nights = (end - start).days if hasattr(start, "day") and hasattr(end, "day") else ""
    except Exception:
        nights = ""

    currency = trip.get("currency", "USD")
    destination = str(trip.get("destination", "Unknown")).split(",")[0].strip()
    travel_modes = [str(mode).lower() for mode in trip.get("travel_modes", []) or []]

    travel_mode_note = ""
    if travel_modes:
        allowed_modes = ", ".join(travel_modes)
        travel_mode_note = f"\nUse only the following travel modes: {allowed_modes}. Do not include any other form of transport."

    travel_modes_joined = ", ".join(trip.get("travel_modes", [])) if trip.get("travel_modes") else "N/A"
    trip_style_joined = ", ".join(trip.get("trip_style", [])) if trip.get("trip_style") else "N/A"

    return f"""
You are an expert travel planner and well-travelled blogger who creates realistic, inspiring itineraries that feel handcrafted.

Create a customized trip titled:  
**Your {destination} Adventure**  
_A handcrafted journey through culture, charm, and hidden gems._

Plan a trip from {trip.get('source', 'Unknown source')} to {trip.get('destination', 'Unknown destination')} for {trip.get('num_people', 1)} people.  
Trip dates: {start} to {end} ({nights} nights)  
Weather snapshot: {weather_parsed}  
Preferred travel modes: {travel_modes_joined}  
Trip style: {trip_style_joined}  
Budget level: {trip.get('budget_level', 'N/A')} (approx. {budget_per_day} {currency} per day){travel_mode_note}

Preferences:  
- Tone: friendly, engaging, and written like a local sharing insider knowledge  
- Dietary: {trip.get('dietary_pref', 'none')}  
- Must-include: {trip.get('must_include_list', 'none')}  
- Avoid: {trip.get('avoid_list', 'none')}

Local logistics:  
- Typical opening hours: {trip.get('opening_hours_hint', 'N/A')}  
- Known closures: {trip.get('closures_hint', 'N/A')}  
- Sunrise/Sunset: {trip.get('sunrise', 'N/A')} / {trip.get('sunset', 'N/A')}  
- Suggested neighborhood clustering: {trip.get('neighborhood_clusters', 'N/A')}

---

### 🧭 Structure your response using **exactly these headings in this order**:
Do not rename, omit, or merge them.

1. **### 🗓️Your **{destination}** Itinerary**  
   - Include a clear per-day breakdown (Day 1, Day 2, etc.)
   - Each day must include Morning, Afternoon, and Evening sections with time ranges.
   - Each block: 1 popular anchor + 1 hidden gem (when possible)
   - Include local food recommendations respecting dietary preferences.
   - Logical flow (minimize travel time).
   - End each day with a “Daily Travel Tip”.

2. **### 🎒 Packing Checklist**  
   - Must have at least 3 categories (e.g., Essentials, Weather Gear, Electronics, etc.)
   - Each category must have 3–6 bullet points.
   - Tailor suggestions to the trip’s weather, duration, and activities.

3. **### 🛡️ Safety Tips**  
   - Include 5–10 concise, destination-specific tips.
   - Cover local etiquette, health/safety, and transit or scam warnings.

✅ Always include both the “🎒 Packing Checklist” and “🛡️ Safety Tips” sections — never omit them.
"""



def day_edit_prompt(
    trip,
    weather_parsed,
    prev_day_content,
    next_day_content,
    day_num,
    day_date,
    trip_summary
):
    currency = trip.get("currency", "USD")
    travel_modes = [mode.lower() for mode in trip.get("travel_modes", []) or []]

    travel_mode_note = ""
    if travel_modes:
        allowed_modes = ", ".join(travel_modes)
        travel_mode_note = f"\nUse only the following travel modes: {allowed_modes}. Do not include any other form of transport."

    return f"""
You are an expert travel planner and well-travelled blogger. You will regenerate ONLY one day of an existing trip itinerary.

Trip context:  
From {trip['source']} to {trip['destination']} for {trip['num_people']} people  
Trip dates: {trip['start_date']} to {trip['end_date']}  
Weather snapshot: {weather_parsed}  
Preferred travel modes: {', '.join(trip['travel_modes'])}  
Trip style: {', '.join(trip['trip_style'])}  
Budget level: {trip['budget_level']} (approx. {trip.get('budget_per_day', 'N/A')} {currency} per day){travel_mode_note}

Existing itinerary summary:  
{trip_summary}

Previous day’s plan:  
{prev_day_content}

Next day’s plan:  
{next_day_content}

Regenerate Day {day_num} ({day_date}) with:  
- Morning / Afternoon / Evening blocks with time ranges  
- Each block: 1 popular anchor + 1 hidden gem (when possible)  
- Include local food recs (respect dietary prefs)  
- Logical flow from previous day to next day  
- No repeating venues from any other day in the trip  
- End with a one-line “Daily Travel Tip”  
- Keep tone/style consistent with the rest of the trip

Formatting:  
Markdown for the day’s plan (same style as full itinerary)  
>>>>>>> d3ec141 (Initial commit: RoamGenie AI Travel Planner with Map and PDF support)
"""