from flask import Flask, render_template, request, send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

from utils import (
    geometry_decision,
    get_characteristic_influences,
    hm_and_sigma_vorh_calculation,
    z0_calculation,
    shape_factor_and_allowable_stresses_calculation,
    stresses_verification,
)

app = Flask(__name__)


@app.route("/")
def welcome():
    "Route to welcome page"
    return render_template("welcome.html")


@app.route("/input")
def index():
    "Route to handle input form"
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    """Route to handle form submission and perform calculations
    Fuction for calculation of the results"""
    # Request form data
    form = request.form
    
    choice = form["choice"]
    if choice == "p":
        hp = float(form["hp"])
        bp = float(form["bp"])
        dr = float(form["dr"])
        he, be = geometry_decision(choice, hp=hp, bp=bp, dr=dr)
    elif choice == "b":
        he = float(form["he"])
        be = float(form["be"])
        he, be = geometry_decision(choice, he=he, be=be)

    # Request characteristic influences
    influence_choice = form["influence_choice"]
    if influence_choice == "c":
        My = float(form["My"])
        N = float(form["N"])
        Fs = float(form["Fs"])
    elif influence_choice == "d":
        My_d = float(form["My_d"])
        Nd = float(form["Nd"])
        Fs = float(form["Fs"])
        My, N, Fs = get_characteristic_influences(
            influence_choice, My_d=My_d, Nd=Nd, Fs=Fs
        )

    # Request holes definition
    n = int(form["n"])
    e2 = float(form["e2"])
    d = float(form["d"])

    # Calculate z0, hm and sigma_vorh
    z0 = z0_calculation(n, Fs, N, My, he)
    F, hm, sigma_vorh = hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2)

    # Calculate shape factor "S" and allowable stresses "sigma_all"
    S, sigma_all = shape_factor_and_allowable_stresses_calculation(he, hm, be, n, d, te=10)

    # Initialize verification_status
    verification_status = None

    # Comparison of compression stresses with allowable stresses
    verification_status = stresses_verification(sigma_vorh, sigma_all, verification_status)

    # Zwróć wynik na stronę
    return render_template(
        "result.html", he=he, be=be, z0=z0, hm=hm, sigma_vorh=sigma_vorh, F=F, sigma_all=sigma_all, S=S, verification_status=verification_status
    )

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    """Route to generate PDF with calculation results"""
    # Request form data
    form = request.form
    
    choice = form["choice"]
    if choice == "p":
        hp = float(form["hp"])
        bp = float(form["bp"])
        dr = float(form["dr"])
        he, be = geometry_decision(choice, hp=hp, bp=bp, dr=dr)
    elif choice == "b":
        he = float(form["he"])
        be = float(form["be"])
        he, be = geometry_decision(choice, he=he, be=be)

    # Request characteristic influences
    influence_choice = form["influence_choice"]
    if influence_choice == "c":
        My = float(form["My"])
        N = float(form["N"])
        Fs = float(form["Fs"])
    elif influence_choice == "d":
        My_d = float(form["My_d"])
        Nd = float(form["Nd"])
        Fs = float(form["Fs"])
        My, N, Fs = get_characteristic_influences(
            influence_choice, My_d=My_d, Nd=Nd, Fs=Fs
        )

    # Request holes definition
    n = int(form["n"])
    e2 = float(form["e2"])
    d = float(form["d"])

    # Calculate z0, hm and sigma_vorh
    z0 = z0_calculation(n, Fs, N, My, he)
    F, hm, sigma_vorh = hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2)

    # Calculate shape factor "S" and allowable stresses "sigma_all"
    S, sigma_all = shape_factor_and_allowable_stresses_calculation(he, hm, be, n, d, te=10)

    # Initialize verification_status
    verification_status = None

    # Comparison of compression stresses with allowable stresses
    verification_status = stresses_verification(sigma_vorh, sigma_all, verification_status)

    # Generate PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Results of the calculation:")
    p.drawString(100, 735, f"1. Bearing height he: {he} [mm]")                                              
    p.drawString(100, 720, f"2. Bearing width be: {be} [mm]")                                               
    p.drawString(100, 705, f"3. Neutral line position z0: {z0} [mm]")                                       
    p.drawString(100, 690, f"4. Equivalent compression zone height hm: {hm} [mm]")                          
    p.drawString(100, 675, f"5. Equivalent compression in hm zone: {sigma_vorh} [MPa]")                     
    p.drawString(100, 660, f"6. Tensile force acting on row of screws in tensile zone F: {F} [kN]")         
    p.drawString(100, 645, f"7. Allowable compression stresses in hm zone, sigma_all: {sigma_all} [MPa]")   
    p.drawString(100, 630, f"8. Shape factor in equivalent hm compression zone S: {S} [-]")                 
    p.drawString(100, 615, f"9. Stresses verification status: {verification_status}")                       

    # Add date and hour of the calculation
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    p.drawString(100, 50, f"Calculation date and time: {date_time}")
    
    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='result.pdf', mimetype='application/pdf')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
