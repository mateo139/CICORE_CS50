from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from calculation import calculate
from utils import (
    geometry_decision,
    get_characteristic_influences,
    hm_and_sigma_vorh_calculation,
    shape_factor_and_allowable_stresses_calculation,
    stresses_verification,
    z0_calculation,
)


def render_pdf(form_data):

    # Request form data
    result = calculate(form_data)

    # Generate PDF
    pdf_file = BytesIO()
    p = canvas.Canvas(pdf_file, pagesize=letter)
    p.drawString(100, 750, f"Results of the calculation:")
    p.drawString(100, 735, f"1. Bearing height he: {result['he']} [mm]")
    p.drawString(100, 720, f"2. Bearing width be: {result['be']} [mm]")
    p.drawString(100, 705, f"3. Neutral line position z0: {result['z0']} [mm]")
    p.drawString(
        100, 690, f"4. Equivalent compression zone height hm: {result['hm']} [mm]"
    )
    p.drawString(
        100, 675, f"5. Equivalent compression in hm zone: {result['sigma_vorh']} [MPa]"
    )
    p.drawString(
        100,
        660,
        f"6. Tensile force acting on row of screws in tensile zone F: {result['F']} [kN]",
    )
    p.drawString(
        100,
        645,
        f"7. Allowable compression stresses in hm zone, sigma_all: {result['sigma_all']} [MPa]",
    )
    p.drawString(
        100,
        630,
        f"8. Shape factor in equivalent hm compression zone S: {result['S']} [-]",
    )
    p.drawString(
        100, 615, f"9. Stresses verification status: {result['verification_status']}"
    )

    # Add date and hour of the calculation
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    p.drawString(100, 50, f"Calculation date and time: {date_time}")

    p.showPage()
    p.save()

    pdf_file.seek(0)

    return pdf_file
