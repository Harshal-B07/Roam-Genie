import streamlit as st
from streamlit_lottie import st_lottie
import json
import os

# --- Page Config ---
st.set_page_config(page_title="About Roam-Genie", page_icon="🧞‍♂️", layout="wide")

# --- Load Lottie Animation ---
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Unable to load animation: {e}")
        return None

lottie_path = os.path.join("assets", "genie_lottie.json")
lottie_genie = load_lottiefile(lottie_path)

# --- Styling ---
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #fff9f4 0%, #f8f4ff 100%);
    color: #2d3436;
    font-family: 'Inter', sans-serif;
}
h1 {
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    color: #5E60CE;
    margin-top: 0.5em;
    margin-bottom: 0.2em;
    text-shadow: 0 0 8px rgba(108, 92, 231, 0.15);
}
.subheading {
    font-size: 20px;
    color: #6c757d;
    margin-bottom: 2.5em;
}
.main-text {
    font-size: 18px;
    line-height: 1.9;
    max-width: 950px;
    text-align: left;
}
ul {
    font-size: 17px;
    line-height: 1.8;
    margin-left: 1.2em;
    margin-bottom: 2em;
}
h3 {
    color: #6C5CE7;
    margin-top: 2em;
    margin-bottom: 0.8em;
    font-family: 'Montserrat', sans-serif;
}
.footer {
    text-align: center;
    font-size: 15px;
    color: #7f8c8d;
    margin-top: 60px;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>🧞‍♂️ About Roam-Genie</h1>", unsafe_allow_html=True)
st.markdown('<p class="subheading">Your wish for the perfect journey, granted with a touch of AI magic ✨</p>', unsafe_allow_html=True)

# --- Wide Layout ---
left, right = st.columns([3, 1.2], gap="large")

with left:
    st.markdown("""
    <div class="main-text">
    Imagine a world where planning a trip feels like making a wish✨  

    That’s the magic of **Roam-Genie** — your digital travel companion who listens, learns,  
    and designs journeys shaped perfectly for your spirit of adventure.  

    Born from the blend of **wanderlust and technology**, Roam-Genie helps travelers uncover  
    not just places, but stories. From mountain trails to midnight bazaars, your genie maps  
    every detail with intuition and care — so you can simply live the moment.  

    <h3>💫 Why Travelers Love Roam-Genie</h3>
    <ul>
        <li>Day-by-day itineraries powered by AI and real-time insights</li>
        <li>Smart budgeting and travel mode recommendations</li>
        <li>Hidden gems, local secrets, and cultural highlights</li>
        <li>Instant PDF downloads for your pocket-ready itinerary</li>
        <li>A friendly genie mascot that evolves with your vibe</li>
    </ul>

    Whether you’re a **solo wanderer**, **couple of dreamers**, or a **tribe of explorers**,  
    Roam-Genie turns your plans into effortless adventures — so your only job  
    is to dream where to go next. 🌍
    </div>
    """, unsafe_allow_html=True)

with right:
    if lottie_genie:
        # 🧞‍♂️ Increased height for a more visible floating genie
        st_lottie(lottie_genie, key="genie", height=600, speed=1)
    else:
        st.info("🪔 The Genie is resting...")

# --- Footer ---
st.markdown("""
<hr style='margin-top: 50px; border: none; height: 1px; background: linear-gradient(to right, transparent, #b3a9ff, transparent);'>
<div style='text-align: center; font-size: 15px; color: #7f8c8d;'>
    Made with 💜, and sprinkle of desert stardust✨.<br>
    <b>Website by Harshal Bhosale</b>
</div>
""", unsafe_allow_html=True)
