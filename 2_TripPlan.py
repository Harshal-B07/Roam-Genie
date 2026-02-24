import streamlit as st
from planner import generate_itinerary
from pdf_utils import generate_pdf
from weather_api import get_weather
from dotenv import load_dotenv
import time
import threading
import db
from datetime import datetime, date

st.set_page_config(page_title="Your Trip Plan", page_icon="🗺️", layout="wide")
load_dotenv()

st.markdown("""
<style>
.fade-in { animation: fadeIn 0.5s ease-in-out; }
@keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }
hr {border: none; border-top: 1px solid #ccc; margin: 2rem 0;}
</style>
""", unsafe_allow_html=True)

# --- Auth check ---
if "user_email" not in st.session_state or not st.session_state["user_email"]:
    st.error("🔒 Please log in or authenticate before generating your itinerary.")
    if st.button("Go to Login Page", key="login_btn"):
        st.switch_page("Roam-Genie.py")
    st.stop()

# --- Trip data check ---
trip = st.session_state.get("selected_trip") or st.session_state.get("trip_details")
if not trip:
    st.error("🧞‍♂️ No trip details found. Please go back and enter your trip info.")
    if st.button("🔙 Return to Dashboard"):
        st.switch_page("pages/3_History.py")
    st.stop()

# --- Extract trip fields ---
trip_data = trip.get("trip_data", trip)
destination = trip_data.get("destination", "Unknown")
start_date = trip_data.get("start_date", "")
end_date = trip_data.get("end_date", "")
style = trip_data.get("trip_style", [])
budget_level = trip_data.get("budget_level", "medium")
currency = trip_data.get("currency", "USD")
show_weather = trip_data.get("include_weather", True)

def to_date(value):
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None

start_date = to_date(start_date)
end_date = to_date(end_date)
style_str = ", ".join(style) if isinstance(style, list) else str(style)

# --- Weather + Itinerary ---
weather_info = get_weather(destination, start_date, end_date) if show_weather else None

loading_messages = [
    f"🌍 Mapping out hidden gems in {destination}...",
    f"🍛 Finding the best local flavors in {destination}...",
    f"🚆 Planning scenic routes by train and car...",
    f"📸 Curating unforgettable moments for your {style_str} trip...",
    f"🧭 Stitching together your perfect {destination} itinerary..."
]

loading_done = False

def loop_loading_messages():
    i = 0
    while not loading_done:
        placeholder.info(loading_messages[i % len(loading_messages)])
        time.sleep(0.8)
        i += 1

placeholder = st.empty()
thread = threading.Thread(target=loop_loading_messages)
thread.start()

# --- Generate itinerary ---
itinerary_blocks = generate_itinerary(trip_data, weather_info)
loading_done = True
thread.join()
placeholder.empty()


if not itinerary_blocks:
    st.warning("⚠️ No itinerary content was generated. Please try again or adjust your trip details.")
    st.stop()

# --- Checklist + Tips ---
def extract_checklist_and_tips(blocks):
    checklist, tips = {}, []
    for block in blocks:
        for slot in block.get("slots", []):
            title = slot.get("title", "").lower()
            desc = slot.get("description", "")
            if "packing checklist" in title:
                for line in desc.splitlines():
                    if ":" in line:
                        category, item = line.split(":", 1)
                        checklist.setdefault(category.strip(), []).append(item.strip())
                    elif line.startswith("-"):
                        checklist.setdefault("General", []).append(line.lstrip("- ").strip())
            elif "safety tips" in title:
                for line in desc.splitlines():
                    if line.startswith("-") or line.startswith("•"):
                        tips.append(line.lstrip("-• ").strip())
    return checklist, tips

checklist, safety_tips = extract_checklist_and_tips(itinerary_blocks)

# --- Save to DB ---
db.init_db()
db.add_itinerary(st.session_state["user_email"], trip_data, itinerary_blocks, checklist, safety_tips)
st.session_state.pop("selected_trip", None)

# --- Page Header ---
st.markdown(f"## 🗓️ Your **{destination}** Itinerary")
st.markdown(f"Here's your personalized travel plan for {destination}, crafted with adventure, comfort, and discovery in mind.")
st.markdown(f"**Destination:** {destination}  \n**Dates:** {start_date} to {end_date}  \n**Travel Style:** {style_str}")

# --- Sidebar Summary ---
with st.sidebar:
    # Format dates
    start_str = start_date.strftime("%d %B %Y") if isinstance(start_date, date) else str(start_date)
    end_str = end_date.strftime("%d %B %Y") if isinstance(end_date, date) else str(end_date)

    # Add emojis to trip styles
    style_emojis = {
        "Adventure": "🧗", "Luxury": "💎", "Cultural": "🏯", "Relaxation": "🛀",
        "Romantic": "💖", "Nature": "🌿", "Foodie": "🍜", "Historical": "🏰",
        "Spiritual": "🕉️", "Shopping": "🛍️", "Photography": "📸"
    }
    style_tags = ", ".join(
        f"{style_emojis.get(s.strip(), '')} {s.strip()}"
        for s in style_str.split(",")
    )

    st.markdown(f"### 🧳 Trip {destination} Summary")
    st.markdown(f"- **Destination:** `{destination}`")
    st.markdown(f"- **Dates:** `{start_str}` to `{end_str}`")
    st.markdown(f"- **Style:** {style_tags}")
    st.markdown(f"- **Budget:** `{budget_level}`")

# --- Actions ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✏️ Edit Trip"):
        st.switch_page("pages/1_TripDetails.py")

with col2:
    pdf_bytes = generate_pdf(trip_data, itinerary_blocks, checklist, safety_tips)
    safe_name = "".join(ch for ch in destination if ch.isalnum() or ch in (" ", "_", "-")).strip().replace(" ", "_")
    filename = f"{safe_name}_{start_date}_to_{end_date}_Itinerary.pdf"
    st.download_button("📄 Download Itinerary PDF", pdf_bytes, file_name=filename, mime="application/pdf")

with col3:
    if st.button("🔄 Regenerate Itinerary"):
        with st.spinner("Regenerating your adventure..."):
            itinerary_blocks = generate_itinerary(trip_data, weather_info)
            checklist, safety_tips = extract_checklist_and_tips(itinerary_blocks)
            db.add_itinerary(st.session_state["user_email"], trip_data, itinerary_blocks, checklist, safety_tips)
            st.rerun()

## --- Itinerary Display ---
for day in itinerary_blocks:
    day_label = str(day.get("day", "")).lower().strip()

    if day_label == "unparsed":
        for slot in day.get("slots", []):
            title = slot.get("title", "").lower()
        if "raw gemini output" in title:
            st.markdown(f"<div class='fade-in'>{slot.get('description', '')}</div>", unsafe_allow_html=True)
        continue

    st.markdown(f"### 📅 {day.get('day', 'Day')}")
    st.markdown("<hr>", unsafe_allow_html=True)

    for slot in day.get("slots", []):
        time = slot.get("time", "")
        title = slot.get("title", "")
        desc = slot.get("description", "")
        map_url = slot.get("map_url", "")

        title_lower = title.lower()
        if "food recommendation" in title_lower:
            st.markdown("🍽️ **Food Recommendation**")
        elif "hidden gem" in title_lower:
            st.markdown("💎 **Hidden Gem**")
        elif "travel tip" in title_lower or "advisory" in title_lower:
            st.markdown("🧭 **Travel Tip**")

        if time or title:
            st.markdown(f"**🕒 {time} — {title}**", unsafe_allow_html=True)
        if desc:
            st.markdown(f"<div class='fade-in'>{desc}</div>", unsafe_allow_html=True)
        if map_url:
            st.markdown(f"[📍 View on Map]({map_url})")
        st.markdown("---")


# --- Packing Checklist ---
if checklist:
    st.markdown("## 🎒 Packing Checklist")
    icon_map = {
        "Essentials": "🧾", "Clothing": "👕", "Electronics": "🔌", "Toiletries": "🧼", "General": "📦"
    }
    for category in sorted(checklist.keys()):
        items = checklist[category]
        icon = icon_map.get(category, "📦")
        st.markdown(f"**{icon} {category}**")
        for item in items:
            st.markdown(f"- {item}")
        st.markdown("")

# --- Safety Tips ---
if safety_tips:
    st.markdown("## 🛡️ Safety Tips")
    for tip in safety_tips:
        st.markdown(f"🛡️ {tip}")