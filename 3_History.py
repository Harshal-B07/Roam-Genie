import streamlit as st
import db
from datetime import date
from pdf_utils import generate_pdf
from dotenv import load_dotenv
from collections import Counter

st.set_page_config(page_title="Your Trip History", page_icon="📜", layout="wide")
load_dotenv()
db.init_db()

# --- Auth check ---
user_email = st.session_state.get("user_email")
if not user_email:
    st.error("🔒 Please log in to view your trip history.")
    st.stop()

# --- Load trips ---
itineraries = db.get_itineraries(user_email)

# --- Pinning logic ---
if "pinned_trips" not in st.session_state:
    st.session_state.pinned_trips = set()
pinned_ids = st.session_state.pinned_trips

# --- Styling ---
st.markdown("""
<style>
.stat-box {
    background-color: var(--secondary-background-color);
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.trip-card {
    background: linear-gradient(135deg, #fdfbff, #f3f0ff);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}
.trip-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: bold;
    background-color: #6C5CE7;
    color: white;
    margin-right: 6px;
}
.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("📜 Your RoamGenie Dashboard")
st.markdown("Welcome back, adventurer! Here's a look at your magical journeys so far:")

# --- Stats ---
if itineraries:
    all_styles = []
    all_destinations = []
    total_budget = 0

    for t in itineraries:
        trip_data = t.get("trip_data", {})
        style = trip_data.get("trip_style", [])
        destination = trip_data.get("destination", "")
        budget = trip_data.get("budget_amount", 0)

        if isinstance(style, list):
            all_styles.extend(style)
        elif isinstance(style, str):
            all_styles.append(style)

        all_destinations.append(destination)
        try:
            total_budget += float(budget)
        except (ValueError, TypeError):
            pass

    style_counts = Counter(all_styles)
    destination_counts = Counter(all_destinations)

    most_common_style = style_counts.most_common(1)[0][0] if style_counts else "N/A"
    most_visited = destination_counts.most_common(1)[0][0] if destination_counts else "N/A"
    avg_budget = round(total_budget / len(itineraries), 2)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='stat-box'><b>Total Trips</b><br>{len(itineraries)}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-box'><b>Most Visited</b><br>{most_visited}</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stat-box'><b>Avg Budget</b><br>₹{avg_budget}</div>", unsafe_allow_html=True)

    st.divider()

    # --- Search & Filter ---
    search_query = st.text_input("🔍 Search by destination or style", placeholder="e.g. Goa, Adventure")
    filtered = [
        trip for trip in itineraries
        if search_query.lower() in trip["trip_data"].get("destination", "").lower()
        or search_query.lower() in str(trip["trip_data"].get("trip_style", "")).lower()
    ] if search_query else itineraries

    # --- Sort: pinned first, then by ID descending ---
    sorted_trips = sorted(filtered, key=lambda t: (t["id"] not in pinned_ids, -t["id"]))

    # --- Trip Cards ---
    for trip in sorted_trips:
        trip_data = trip["trip_data"]
        trip_id = trip["id"]
        destination = trip_data.get("destination", "Unknown")
        start_date = trip_data.get("start_date", "")
        end_date = trip_data.get("end_date", "")
        style = trip_data.get("trip_style", "N/A")
        budget = trip_data.get("budget_amount", "N/A")
        budget_level = trip_data.get("budget_level", "N/A")

        st.markdown(f"""
        <div class="trip-card fade-in">
            <h4 style="margin-bottom: 0;">{destination}</h4>
            <p style="margin: 0; font-size: 0.9em; color: gray;">{start_date} → {end_date}</p>
            <p style="margin: 6px 0;">
                <span class="badge">{style}</span>
                <span class="badge">₹{budget} ({budget_level})</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # --- Action Buttons (inside loop, unique keys) ---
        b1, b2, b3, b4, b5 = st.columns(5)

        with b1:
            if st.button("👁 View", key=f"view_{trip_id}"):
                st.session_state["selected_trip"] = trip
                st.switch_page("pages/2_TripPlan.py")

        with b2:
            if st.button("♻ Replan", key=f"replan_{trip_id}"):
                st.session_state["trip_details"] = trip_data
                st.switch_page("pages/1_TripDetails.py")

        with b3:
            if st.button("🗑 Delete", key=f"delete_{trip_id}"):
                if db.delete_itinerary(trip_id):
                    st.toast("✅ Trip deleted!")
                    st.rerun()
                else:
                    st.toast("❌ Error deleting trip.")

        with b4:
            pdf_bytes = generate_pdf(trip_data, trip["itinerary_text"], trip["checklist"], trip["safety_tips"])
            st.download_button("📄 PDF", pdf_bytes, file_name=f"{destination}_itinerary.pdf", mime="application/pdf", key=f"pdf_{trip_id}")

        with b5:
            pin_label = "⭐ Unpin" if trip_id in pinned_ids else "☆ Pin"
            if st.button(pin_label, key=f"pin_{trip_id}"):
                if trip_id in pinned_ids:
                    pinned_ids.remove(trip_id)
                else:
                    pinned_ids.add(trip_id)
                st.rerun()

else:
    st.markdown("""
    <div style="text-align:center; margin-top:60px;">
        <h2>🧞‍♂️ No trips yet!</h2>
        <p>Rub the lamp and begin your journey by planning your first adventure.</p>
    </div>
    """, unsafe_allow_html=True)