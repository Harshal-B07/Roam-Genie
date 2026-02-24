<<<<<<< HEAD
import streamlit as st
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

geolocator = Nominatim(user_agent="roamgenie")

def show_map(locations_text):
    locations = [city.strip() for city in locations_text.split(",") if city.strip()]
    coords = []

    for loc in locations:
        try:
            location = geolocator.geocode(loc, timeout=10)
            if location:
                coords.append((location.latitude, location.longitude))
            else:
                st.warning(f"⚠️ Could not locate '{loc}'.")
        except Exception as e:
            st.warning(f"⚠️ Error locating '{loc}': {e}")

    if not coords:
        st.error("❌ No valid locations found to map.")
        return None

    m = folium.Map()
    bounds = []

    for i, (lat, lon) in enumerate(coords):
        folium.Marker(
            location=[lat, lon],
            popup=f"📍 Stop {i+1}: {locations[i]}",
            tooltip=locations[i]
        ).add_to(m)
        bounds.append((lat, lon))

    # Fit map to all points
    if bounds:
        m.fit_bounds(bounds)

    st_folium(m, width=700, height=500)
=======
import streamlit as st
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

geolocator = Nominatim(user_agent="roamgenie")

def show_map(locations_text):
    locations = [city.strip() for city in locations_text.split(",") if city.strip()]
    coords = []

    for loc in locations:
        try:
            location = geolocator.geocode(loc, timeout=10)
            if location:
                coords.append((location.latitude, location.longitude))
            else:
                st.warning(f"⚠️ Could not locate '{loc}'.")
        except Exception as e:
            st.warning(f"⚠️ Error locating '{loc}': {e}")

    if not coords:
        st.error("❌ No valid locations found to map.")
        return None

    m = folium.Map()
    bounds = []

    for i, (lat, lon) in enumerate(coords):
        folium.Marker(
            location=[lat, lon],
            popup=f"📍 Stop {i+1}: {locations[i]}",
            tooltip=locations[i]
        ).add_to(m)
        bounds.append((lat, lon))

    # Fit map to all points
    if bounds:
        m.fit_bounds(bounds)

    st_folium(m, width=700, height=500)
>>>>>>> d3ec141 (Initial commit: RoamGenie AI Travel Planner with Map and PDF support)
