from flask import Flask, render_template, request

from utils import (
    geometry_decision,
    get_characteristic_influences,
    hm_and_sigma_vorh_calculation,
    z0_calculation,
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

    # Zwróć wynik na stronę
    return render_template(
        "result.html", he=he, be=be, z0=z0, hm=hm, sigma_vorh=sigma_vorh, F=F
    )


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
