from utils import (
    geometry_decision,
    get_characteristic_influences,
    hm_and_sigma_vorh_calculation,
    shape_factor_and_allowable_stresses_calculation,
    stresses_verification,
    z0_calculation,
)


def calculate(form_data):
    """Route to handle form submission and perform calculations
    Fuction for calculation of the results"""
    # Request form data

    print(form_data)

    choice = form_data["choice"]
    if choice == "p":
        hp = float(form_data["hp"])
        bp = float(form_data["bp"])
        dr = float(form_data["dr"])
        he, be = geometry_decision(choice, hp=hp, bp=bp, dr=dr)
    elif choice == "b":
        he = float(form_data["he"])
        be = float(form_data["be"])
        he, be = geometry_decision(choice, he=he, be=be)

    # Request characteristic influences
    influence_choice = form_data["influence_choice"]
    if influence_choice == "c":
        My = float(form_data["My"])
        N = float(form_data["N"])
        Fs = float(form_data["Fs"])
    elif influence_choice == "d":
        My_d = float(form_data["My_d"])
        Nd = float(form_data["Nd"])
        Fs = float(form_data["Fs"])
        My, N, Fs = get_characteristic_influences(
            influence_choice, My_d=My_d, Nd=Nd, Fs=Fs
        )

    # Request holes definition and thickness of the bearing
    n = int(form_data["n"])
    e2 = float(form_data["e2"])
    d = float(form_data["d"])
    te = int(form_data["te"])

    # Calculate z0, hm and sigma_vorh
    z0 = z0_calculation(n, Fs, N, My, he)
    F, hm, sigma_vorh = hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2)

    # Calculate shape factor "S" and allowable stresses "sigma_all"
    S, sigma_all = shape_factor_and_allowable_stresses_calculation(he, hm, be, n, d, te)

    # Initialize verification_status
    verification_status = None

    # Comparison of compression stresses with allowable stresses
    verification_status = stresses_verification(
        sigma_vorh, sigma_all, verification_status
    )

    # Return result to the page
    return {
        "he": he,
        "be": be,
        "te": te,
        "z0": z0,
        "hm": hm,
        "sigma_vorh": sigma_vorh,
        "F": F,
        "sigma_all": sigma_all,
        "S": S,
        "verification_status": verification_status,
    }
