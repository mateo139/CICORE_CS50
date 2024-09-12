from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Funkcje do obliczeń (możesz przenieść swój kod tutaj)
def geometry_decision(choice, hp=None, bp=None, dr=None, he=None, be=None):
    if choice == "p":
        he = hp - 2 * dr
        be = bp - 2 * dr
    elif choice == "b":
        he = he
        be = be
    return he, be

def get_characteristic_influences(choice, My=None, N=None, My_d=None, Nd=None, Fs=None):
    if choice == "c":
        return My, N, Fs
    elif choice == "d":
        My = My_d / 1.4
        N = Nd / 1.4
        return My, N, Fs

def holes_definition(n, e2, d):
    return n, e2, d

def z0_calculation(n, Fs, N, My, he):
    z0 = int(((n * Fs - N) / (12 * My) * he ** 2) / 1000)
    return z0

def hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2):
    if z0 > he / 2:
        hm = int((he + 2 * My * 1000 / (N - n * Fs)))
        sigma_vorh = (N - n * Fs)**2 * 1000 / (be * (he * (N - n * Fs) + 2 * My * 1000))
    else:
        F = int((N - n * Fs) / he * (he / 2 - z0) + 6 * My * 1000 / he**3 * (he**2 / 4 - z0 * 2))
        hm = int(he + (2 * My * 1000 - F * e2) / (N - n * Fs - F))
        sigma_vorh = (N - n * Fs - F)**2 * 1000 / (be * (he * (N - n * Fs - F) + 2 * My * 1000 - F * e2))
    return hm, round(sigma_vorh, 2)

# Route to handle input form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and perform calculations
@app.route('/calculate', methods=['POST'])
def calculate():
    # Pobranie danych z formularza
    choice = request.form['choice']
    if choice == 'p':
        hp = float(request.form['hp'])
        bp = float(request.form['bp'])
        dr = float(request.form['dr'])
        he, be = geometry_decision(choice, hp=hp, bp=bp, dr=dr)
    elif choice == 'b':
        he = float(request.form['he'])
        be = float(request.form['be'])
        he, be = geometry_decision(choice, he=he, be=be)
    
    # Pobranie danych do charakterystyk
    influence_choice = request.form['influence_choice']
    if influence_choice == 'c':
        My = float(request.form['My'])
        N = float(request.form['N'])
        Fs = float(request.form['Fs'])
    elif influence_choice == 'd':
        My_d = float(request.form['My_d'])
        Nd = float(request.form['Nd'])
        Fs = float(request.form['Fs'])
        My, N, Fs = get_characteristic_influences(influence_choice, My_d=My_d, Nd=Nd, Fs=Fs)
    
    # Definicja otworów
    n = int(request.form['n'])
    e2 = float(request.form['e2'])
    d = float(request.form['d'])
    
    z0 = z0_calculation(n, Fs, N, My, he)
    hm, sigma_vorh = hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2)

    # Zwróć wynik na stronę
    return render_template('result.html', he=he, be=be, z0=z0, hm=hm, sigma_vorh=sigma_vorh)

if __name__ == '__main__':
    app.run(debug=True)