import re
import streamlit as st
from datetime import date
from dotenv import load_dotenv

st.set_page_config(page_title="Trip Details", page_icon="🗺️", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
body {
    background-color: #fff9f4;
    color: #2d3436;
    font-family: 'Inter', sans-serif;
}
h4 {
    color: #6C5CE7;
    font-family: 'Montserrat', sans-serif;
}
.section-divider {
    border-top: 2px solid #ddd;
    margin: 20px 0;
}
.fade-in {
    animation: fadeIn 0.5s ease-in-out;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
.preview-card {
    background: #fff8ef;
    border: 2px solid #f0e0c9;
    border-radius: 16px;
    padding: 1em 1.5em;
    margin-top: 0 !important;
    box-shadow: 0 0 14px rgba(108, 92, 231, 0.08);
}
.login-btn > button {
    font-size: 16px;
    padding: 0.6em 1.8em;
    border-radius: 12px;
    background-color: #6C5CE7;
    color: white;
    border: none;
    box-shadow: 0 0 10px rgba(108, 92, 231, 0.25);
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    font-weight: 600;
}
.login-btn > button:hover {
    background-color: #00B894;
    box-shadow: 0 0 14px rgba(0, 184, 148, 0.35);
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# --- Auth check ---
if "user_email" not in st.session_state or not st.session_state["user_email"]:
    st.error("🔒 Please log in or authenticate before generating your itinerary.")
    if st.container():
        if st.button("Go to Login Page", key="login_btn", help="Return to the welcome screen"):
            st.switch_page("Roam-Genie.py")
    st.stop()

# --- Helpers ---
def is_valid_location(name: str) -> bool:
    name = name.strip()
    if len(name) < 3:
        return False
    try:
        import regex
        pattern = r"^[\p{L}\s,'-]+$"
        return bool(regex.fullmatch(pattern, name))
    except ImportError:
        return bool(re.fullmatch(r"^[A-Za-z\s,'-]+$", name))

def auto_capitalize(text: str) -> str:
    return " ".join(word.capitalize() for word in text.split())

def format_inr_input(value: str) -> str:
    try:
        num = int(value.replace(",", "").strip())
        return f"{num:,}"
    except:
        return value

def suggest_travel_modes(source: str, destination: str) -> list:
    suggestions = []
    if source and destination:
        src_country = source.split(",")[-1].strip().lower()
        dest_country = destination.split(",")[-1].strip().lower()
        if src_country == dest_country:
            suggestions.extend(["🚆 Train", "🚗 Car"])
        else:
            suggestions.append("✈️ Flight")
    return list(dict.fromkeys(suggestions))

def mascot_reaction(styles):
    reactions = {
        "Adventure": "🧞‍♂️ Your genie packed hiking boots!",
        "Luxury": "🧞‍♂️ Your genie polished the champagne glasses!",
        "Foodie": "🧞‍♂️ Your genie is sniffing out the best street food!",
        "Romantic": "🧞‍♂️ Your genie lit the candles and booked a sunset cruise!",
        "Spiritual": "🧞‍♂️ Your genie is meditating under a Bodhi tree!"
    }
    matched = [reactions[s] for s in styles if s in reactions]
    return "\n".join(matched) if matched else "🧞‍♂️ Your genie is crafting something magical..."

# --- Defaults ---
defaults = {
    "source": "", "destination": "", "num_people": 1,
    "start_date": date.today(), "end_date": date.today(),
    "trip_style": [], "budget_input": "", "currency": "INR",
    "travel_modes": [], "dietary_pref": "None",
    "show_section_2": False, "show_section_3": False, "show_section_4": False
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)

# --- Layout ---
col_form, col_preview = st.columns([2, 1])

with col_form:
    # Step 1
    with st.expander("📍 Step 1: Locations", expanded=True):
        
        source = st.text_input("🛫 Source (City, Country)", value=st.session_state.source)
        if source:
            st.session_state.source = auto_capitalize(source)
            if not is_valid_location(source):
                st.warning("⚠️ Source must be a valid city name (letters only, min 3 characters).")

        destination = st.text_input("🎯 Destination (City, Country)", value=st.session_state.destination)
        if destination:
            st.session_state.destination = auto_capitalize(destination)
            if not is_valid_location(destination):
                st.warning("⚠️ Destination must be a valid city name (letters only, min 3 characters).")

        if st.button("➡ Continue to Dates & People"):
            if is_valid_location(st.session_state.source) and is_valid_location(st.session_state.destination):
                st.session_state.show_section_2 = True
            else:
                st.warning("Please enter valid Source and Destination.")

    # Step 2
    if st.session_state.show_section_2:
        with st.expander("📅 Step 2: Dates & People", expanded=True):
            st.session_state.num_people = st.number_input("👥 Number of People", min_value=1, step=1, value=st.session_state.num_people)
            st.session_state.start_date = st.date_input("📆 Start Date", value=st.session_state.start_date)
            st.session_state.end_date = st.date_input("📆 End Date", value=st.session_state.end_date)

            if st.session_state.end_date < st.session_state.start_date:
                st.error("❌ End date cannot be before start date.")
            else:
                duration = (st.session_state.end_date - st.session_state.start_date).days + 1
                st.caption(f"Trip Duration: {duration} days")

            if st.button("➡ Continue to Style & Budget"):
                if st.session_state.num_people > 0 and st.session_state.end_date >= st.session_state.start_date:
                    st.session_state.show_section_3 = True
                else:
                    st.warning("Please enter valid dates and number of people.")

    # Step 3
    if st.session_state.show_section_3:
        with st.expander("🎨 Step 3: Style, Budget & Currency", expanded=True):
            trip_styles = [
                "Adventure", "Luxury", "Cultural", "Relaxation", "Romantic", "Nature",
                "Foodie", "Historical", "Spiritual", "Shopping", "Photography"
            ]
            st.session_state.trip_style = st.multiselect("🎭 Trip Style(s)", trip_styles, default=["Adventure"])

            st.session_state.currency = st.selectbox("💱 Preferred Currency", ["USD", "INR", "EUR", "JPY", "CNY", "GBP", "AUD"], index=1)

            budget_raw = st.text_input(f"💰 Daily Budget ({st.session_state.currency})", value=st.session_state.budget_input)
            if budget_raw:
                formatted = format_inr_input(budget_raw)
                if formatted != budget_raw:
                    st.session_state.budget_input = formatted
                try:
                    budget_amount = float(formatted.replace(",", "").strip())
                except ValueError:
                    budget_amount = 0.0
                    st.warning("⚠ Please enter a valid number for budget.")
            else:
                budget_amount = 0.0

            if st.button("➡ Continue to Travel Modes"):
                if budget_amount > 0:
                    st.session_state.show_section_4 = True
                else:
                    st.warning("Please enter a valid budget.")

    # Step 4
    if st.session_state.show_section_4:
        with st.expander("🚗 Step 4: Travel Modes & Preferences", expanded=True):
            suggested_modes = suggest_travel_modes(st.session_state.source, st.session_state.destination)
            st.session_state.travel_modes = st.multiselect(
                "🚀 Select Travel Modes",
                ["✈️ Flight", "🚆 Train", "🚗 Car", "🚌 Bus", "⛵ Boat"],
                default=suggested_modes if not st.session_state.travel_modes else st.session_state.travel_modes
            )

            st.session_state.dietary_pref = st.selectbox("🥗 Dietary Preference", ["None", "Vegetarian", "Vegan", "Halal"])

            show_weather = st.toggle("🌦 Include weather in itinerary??", value=False)

            if st.button("✨ Create your Magical Itinerary!!"):
                if st.session_state.travel_modes:
                    st.session_state["trip_details"] = {
                        "source": st.session_state.source.strip(),
                        "destination": st.session_state.destination.strip(),
                        "num_people": st.session_state.num_people,
                        "start_date": st.session_state.start_date,
                        "end_date": st.session_state.end_date,
                        "trip_style": st.session_state.trip_style,
                        "budget_amount": float(st.session_state.budget_input.replace(",", "")),
                        "currency": st.session_state.currency,
                        "budget_level": "Custom",
                        "travel_modes": st.session_state.travel_modes,
                        "dietary_pref": st.session_state.dietary_pref,
                        "include_weather": show_weather
                    }
                    st.switch_page("pages/2_TripPlan.py")

# --- Preview Section ---
with col_preview:
    st.markdown("""
    <div class="preview-card fade-in">
        <h4>🧭 Trip Preview</h4>
    """, unsafe_allow_html=True)

    if st.session_state.source and st.session_state.destination:
        st.markdown(f"**From:** {st.session_state.source}")
        st.markdown(f"**To:** {st.session_state.destination}")

    if st.session_state.start_date and st.session_state.end_date:
        duration = (st.session_state.end_date - st.session_state.start_date).days + 1
        st.markdown(f"**Dates:** {st.session_state.start_date} → {st.session_state.end_date}")
        st.markdown(f"**Duration:** {duration} days")

    st.markdown(f"**Travellers:** {st.session_state.num_people}")
    if st.session_state.trip_style:
        st.markdown(f"**Style:** {', '.join(st.session_state.trip_style)}")
        st.caption(mascot_reaction(st.session_state.trip_style))
    if st.session_state.budget_input:
        st.markdown(f"**Budget:** {st.session_state.budget_input} {st.session_state.currency}")
    if st.session_state.travel_modes:
        st.markdown(f"**Travel Mode(s):** {', '.join(st.session_state.travel_modes)}")
    if st.session_state.dietary_pref and st.session_state.dietary_pref != "None":
        st.markdown(f"**Dietary Preference:** {st.session_state.dietary_pref}")

    st.markdown("</div>", unsafe_allow_html=True)
