from datetime import datetime
from io import BytesIO

from flask import Flask, render_template, request, send_file

import calculation

import render_pdf
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

    results = calculation.calculate(request.form)

    # Return result to the page
    return render_template(
        "result.html",
        result=results,
    )


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    """Function to generate PDF with calculation results"""

    pdf_file = render_pdf.render_pdf(request.form)

    # Request form data

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name="result.pdf",
        mimetype="application/pdf",
    )


# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8000)
