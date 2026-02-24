import streamlit as st
import json
import re
import os
import time
from streamlit_lottie import st_lottie
import db  # Optional

# --- Page Config ---
st.set_page_config(page_title="Roam-Genie – Welcome", layout="centered")

# --- Load Lottie Animation ---
def load_lottie(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"⚠️ Failed to load animation: {e}")
        return None


genie_animation = load_lottie(os.path.join("assets", "genie_lottie.json"))

# --- Custom CSS with adaptive glow ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Montserrat:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Light mode background glow */
@media (prefers-color-scheme: light) {
    html, body {
        background: radial-gradient(circle at center, #fdfbff 0%, #f3f0ff 100%);
    }
}

/* Dark mode background glow */
@media (prefers-color-scheme: dark) {
    html, body {
        background: radial-gradient(circle at center, #1E1E1E 0%, #2C2C2C 100%);
    }
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Montserrat', sans-serif !important;
    color: #6C5CE7;
}
h1 {
    text-align: center;
    font-size: 58px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 5px;
}
h4 {
    text-align: center;
    color: #636e72;
    margin-bottom: 20px;
}

/* Buttons */
.stButton>button {
    font-size: 18px;
    padding: 0.7em 2.5em;
    border-radius: 14px;
    background-color: #6C5CE7;
    color: white;
    border: none;
    box-shadow: 0 0 12px rgba(108, 92, 231, 0.25);
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #00B894;
    box-shadow: 0 0 16px rgba(0, 184, 148, 0.35);
    transform: scale(1.05);
}

/* Input styling */
input[type="text"] {
    border: 2px solid #6C5CE7 !important;
    border-radius: 10px;
    padding: 0.6em;
}
input[type="text"]:focus {
    border-color: #00B894 !important;
    box-shadow: 0 0 6px #00B894 !important;
}

/* Animations */
.fade-in {
    animation: fadeIn 1s ease-in-out;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}
.fade-out {
    animation: fadeOut 0.8s ease-in-out forwards;
}
@keyframes fadeOut {
    from {opacity: 1;}
    to {opacity: 0;}
}
</style>
""", unsafe_allow_html=True)

# --- Title & Tagline ---
st.markdown('<h1 class="fade-in">Welcome to Roam-Genie!!</h1>', unsafe_allow_html=True)
st.markdown('<h4 class="fade-in">Your AI-powered travel genie, ready to craft your perfect journey ✨</h4>', unsafe_allow_html=True)

# --- Genie Animation ---
if genie_animation:
    st_lottie(genie_animation, speed=1, height=400, key="genie")

# --- Email Validation ---
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


# --- Email Input ---
email = st.text_input("Enter your email to begin:", placeholder="you@example.com", key="email_input")

# --- Rotating micro-copy ---
messages = [
    "🧞‍♂️ Your magic carpet awaits…",
    "✨ The genie is polishing your itinerary lamp…",
    "🌍 Adventure is just one click away…"
]
if "msg_index" not in st.session_state:
    st.session_state.msg_index = 0
st.caption(messages[st.session_state.msg_index])
st.session_state.msg_index = (st.session_state.msg_index + 1) % len(messages)

# --- Start Button with fade-out transition ---
if st.button("Begin Your Journey.."):
    if not email:
        st.warning("Please enter your email before continuing.")
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")
    else:
        st.session_state["user_email"] = email
        # Optional: db.add_user(email)
        st.markdown('<div class="fade-out"></div>', unsafe_allow_html=True)
        time.sleep(0.8)  # Wait for fade-out animation
        st.switch_page("pages/1_TripDetails.py")  # Correct relative path
