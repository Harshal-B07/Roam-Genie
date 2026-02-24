<<<<<<< HEAD
# Roam-Genie

Roam-Genie is a Streamlit-based travel itinerary generator that helps users plan personalized trips with ease. It features a multi-step form for trip details, generates day-wise itineraries, provides packing checklists and safety tips, and allows users to download their plans as stylish PDFs.

## Features

- **Multi-step Trip Form:** Enter source, destination, dates, number of people, travel style, budget, currency, travel modes, and dietary preferences.
- **Personalized Itinerary Generation:** Get a detailed, day-wise itinerary tailored to your preferences.
- **Packing Checklist & Safety Tips:** Automatically generated based on your trip details.
- **Weather Integration:** Optionally include weather information in your itinerary.
- **PDF Export:** Download your itinerary as a professionally formatted PDF.
- **User Authentication:** Secure access to your trip plans.
- **Modern UI:** Clean, responsive interface with custom CSS and helpful feedback.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Final
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file with any required API keys or settings.

4. **Run the app:**
   ```bash
   streamlit run pages/1_TripDetails.py
   ```

## Project Structure

- `pages/1_TripDetails.py` — Multi-step form for entering trip details.
- `pages/2_TripPlan.py` — Generates and displays the itinerary, checklist, and PDF download.
- `pdf_utils.py` — PDF generation utilities.
- `planner.py` — Itinerary generation logic.
- `weather_api.py` — Weather data integration.
- `db.py` — Database utilities for saving and retrieving trips.

## Screenshots

_Add screenshots of the UI and sample PDF output here._

## License

MIT License

---

**Roam-Genie** — Your AI-powered travel planning companion!
=======
# Roam-Genie

Roam-Genie is a Streamlit-based travel itinerary generator that helps users plan personalized trips with ease. It features a multi-step form for trip details, generates day-wise itineraries, provides packing checklists and safety tips, and allows users to download their plans as stylish PDFs.

## Features

- **Multi-step Trip Form:** Enter source, destination, dates, number of people, travel style, budget, currency, travel modes, and dietary preferences.
- **Personalized Itinerary Generation:** Get a detailed, day-wise itinerary tailored to your preferences.
- **Packing Checklist & Safety Tips:** Automatically generated based on your trip details.
- **Weather Integration:** Optionally include weather information in your itinerary.
- **PDF Export:** Download your itinerary as a professionally formatted PDF.
- **User Authentication:** Secure access to your trip plans.
- **Modern UI:** Clean, responsive interface with custom CSS and helpful feedback.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Final
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file with any required API keys or settings.

4. **Run the app:**
   ```bash
   streamlit run pages/1_TripDetails.py
   ```

## Project Structure

- `pages/1_TripDetails.py` — Multi-step form for entering trip details.
- `pages/2_TripPlan.py` — Generates and displays the itinerary, checklist, and PDF download.
- `pdf_utils.py` — PDF generation utilities.
- `planner.py` — Itinerary generation logic.
- `weather_api.py` — Weather data integration.
- `db.py` — Database utilities for saving and retrieving trips.

## Screenshots

_Add screenshots of the UI and sample PDF output here._

## License

MIT License

---

**Roam-Genie** — Your AI-powered travel planning companion!
>>>>>>> d3ec141 (Initial commit: RoamGenie AI Travel Planner with Map and PDF support)
