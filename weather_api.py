import os
import requests
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Geopy geolocator
geolocator = Nominatim(user_agent="roamgenie")

@lru_cache(maxsize=50)
def get_coordinates(city: str):
    """Return (lat, lon) tuple for a city name, or (None, None) if not found."""
    try:
        location = geolocator.geocode(city, timeout=10)
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception:
        return None, None

def get_weather(city: str, start_date=None, end_date=None):
    """
    Fetch current weather for a city using OpenWeather API.
    Returns a display-friendly string, or an error message.
    """
    if not OPENWEATHER_API_KEY:
        return "🌤️ Weather unavailable (missing OPENWEATHER_API_KEY)."
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return f"⚠️ Could not retrieve weather data for {city}."

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&units=metric&appid={OPENWEATHER_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        desc = data["weather"][0]["description"].capitalize()
        temp = round(data["main"]["temp"])
        city_name = data.get("name", city)

        return f"🌤️ {city_name}: {desc}, {temp}°C"
    except Exception as e:
        return f"⚠️ Error fetching weather for {city}: {e}"