from fpdf import FPDF
from typing import Dict, Any
from datetime import date
import unicodedata

def sanitize_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    return ''.join(
        ch for ch in text
        if ord(ch) <= 0xFFFF and (unicodedata.category(ch)[0] != 'C' or ch in '\n\t')
    )

def render_trip_overview(pdf, trip, content_width):
    destination = trip.get("destination", "")
    start_date = trip.get("start_date", "")
    end_date = trip.get("end_date", "")
    trip_style = trip.get("trip_style", "")
    budget_amount = trip.get("budget_amount", "")
    budget_level = trip.get("budget_level", "")
    num_people = trip.get("num_people", "")
    travel_modes = trip.get("travel_modes", [])

    if isinstance(start_date, date):
        start_date_str = start_date.strftime("%d %B %Y")
    else:
        start_date_str = str(start_date)
    if isinstance(end_date, date):
        end_date_str = end_date.strftime("%d %B %Y")
    else:
        end_date_str = str(end_date)
    travel_modes_str = ", ".join(map(str, travel_modes))

    pdf.set_x(pdf.l_margin)
    pdf.set_font("DejaVu", 'B', 16)
    pdf.cell(0, 10, "Trip Itinerary", ln=True, align='L')
    pdf.ln(10)

    pdf.set_font("DejaVu", size=12)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(content_width, 8, sanitize_text(f"Destination: {destination}"))

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(content_width, 8, sanitize_text(f"Dates: {start_date_str} to {end_date_str}"))

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(content_width, 8, sanitize_text(f"Style: {trip_style}"))

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(content_width, 8, sanitize_text(f"Budget: ₹{budget_amount} ({budget_level})"))

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(content_width, 8, sanitize_text(f"Travel modes: {travel_modes_str}"))

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(content_width, 8, sanitize_text(f"Travellers: {num_people}"))

    pdf.ln(5)


def render_itinerary(pdf, itinerary_text, content_width):
    blocks = []

    if isinstance(itinerary_text, list):
        for block in itinerary_text:
            if isinstance(block, dict) and "day" in block and "slots" in block:
                title = block["day"]
                lines = [
                    f"{slot.get('time', '')} — {slot.get('title', '')}\n{slot.get('description', '')}"
                    for slot in block["slots"]
                ]
                blocks.append([title] + lines)
            elif isinstance(block, str):
                blocks.append([block])
    else:
        lines = [ln for ln in str(itinerary_text).splitlines() if ln.strip()]
        current = []
        for ln in lines:
            if ln.lower().startswith("day ") and any(char.isdigit() for char in ln):
                if current:
                    blocks.append(current)
                current = [ln]
            else:
                current.append(ln)
        if current:
            blocks.append(current)

    for block in blocks:
        title = block[0]
        title_clean = title
        if isinstance(title, str) and title.strip().lower() in ["unparsed", "raw gemini output"]:
            title_clean = "Handcrafted Summary"  # 👈 Rebrand the title only

        pdf.set_x(pdf.l_margin)
        pdf.set_font("DejaVu", 'B', 14)
        pdf.cell(0, 10, sanitize_text(title_clean), ln=True, align='L')
        pdf.set_font("DejaVu", size=12)
        for body_line in block[1:]:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(content_width, 6, sanitize_text(body_line))
        pdf.ln(2)

def render_checklist(pdf, checklist, content_width):
    if not checklist:
        return
    pdf.add_page()  # 🔹 Page break before checklist
    pdf.set_font("DejaVu", 'B', 13)
    pdf.cell(0, 10, "Packing Checklist", ln=True)
    pdf.set_font("DejaVu", size=12)
    if isinstance(checklist, dict):
        for category, items in checklist.items():
            pdf.set_font("DejaVu", 'B', 12)
            pdf.cell(0, 8, sanitize_text(f"{category}:"), ln=True)
            pdf.set_font("DejaVu", size=12)
            for item in items:
                pdf.multi_cell(content_width, 6, sanitize_text(f"• {item}"))
    else:
        for item in checklist:
            pdf.multi_cell(content_width, 6, sanitize_text(f"• {item}"))

def render_safety_tips(pdf, safety_tips, content_width):
    if not safety_tips:
        return
    pdf.add_page()  # 🔹 Page break before safety tips
    pdf.set_font("DejaVu", 'B', 13)
    pdf.cell(0, 10, "Safety Tips", ln=True)
    pdf.set_font("DejaVu", size=12)
    for tip in safety_tips:
        pdf.multi_cell(content_width, 6, sanitize_text(f"• {tip}"))

def generate_pdf(trip: Dict[str, Any], itinerary_text: Any, checklist=None, safety_tips=None) -> bytes:
    checklist = checklist or {}
    safety_tips = safety_tips or []

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf", uni=True)
    pdf.set_font("DejaVu", 'B', 16)
    pdf.cell(0, 10, "Trip Itinerary", ln=True, align='C')
    pdf.ln(5)

    content_width = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_x(pdf.l_margin)

    render_trip_overview(pdf, trip, content_width)
    render_itinerary(pdf, itinerary_text, content_width)
    render_checklist(pdf, checklist, content_width)
    render_safety_tips(pdf, safety_tips, content_width)

    out = pdf.output(dest='S')
    if isinstance(out, bytearray):
        return bytes(out)
    if isinstance(out, bytes):
        return out
    if isinstance(out, str):
        return out.encode('latin1', errors='ignore')
    try:
        return bytes(out)
    except Exception:
        return str(out).encode('latin1', errors='ignore')