import math # Import modułu math

def geometry_decision(): # Deklaracja funkcji geometry_decision zwracającej wartości he i be
    # Zadaj pytanie użytkownikowi
    choice = input("Czy chcesz zdefiniować płytę czołową (wpisz 'p') czy podkładkę elastomerową (wpisz 'b')?: ").strip().lower()



    if choice == "p": # Pobieranie danych dla płyty czołowej
        # Pobieranie danych dla płyty czołowej
        hp = float(input("Podaj wysokość płyty hp: "))
        bp = float(input("Podaj szerokość płyty bp: "))
        dr = float(input("Podaj odległość krawędziową dr: "))
        
        # Obliczenia he i be
        he = hp - 2 * dr
        be = bp - 2 * dr
        
        print(f"Wartość he = {he}, Wartość be = {be}")
        return he, be,

    elif choice == "b": # Pobieranie danych dla podkładki elastomerowej
        # Pobieranie danych dla podkładki elastomerowej
        he = float(input("Podaj wartość he: "))
        be = float(input("Podaj wartość be: "))
        
        print(f"Wartość he = {he}, Wartość be = {be}")
        return he, be

    else:
        print("Niepoprawny wybór. Proszę wybrać 'plate' lub 'bearing'.")
        return geometry_decision()  # Rekurencyjnie pytamy ponownie, jeśli wybór był niepoprawny

def get_characteristic_influences():  # Funkcja pobierająca wartości charakterystyczne Momentu zginającego, Siły osiowej i Siły sprężającej śruby -> Zwraca wartości My, N i Fs
    # Zapytać użytkownika, czy podaje wartości charakterystyczne czy obliczeniowe
    choice = input("Czy podawane wartości Momentu zginającego (M) i Siły osiowej (N) są charakterystyczne (wpisz 'c') czy obliczeniowe (wpisz 'd')?: ").strip().lower()
    
    if choice == "c":
        # Pobieranie wartości charakterystycznych
        My = float(input("Podaj wartość Momentu zginającego My (charakterystyczne): "))
        N = float(input("Podaj wartość Siły osiowej N (charakterystyczne): "))
        
    elif choice == "d":
        # Pobieranie wartości obliczeniowych
        My_d = float(input("Podaj wartość Momentu zginającego My,d (obliczeniowe): "))
        Nd = float(input("Podaj wartość Siły osiowej Nd (obliczeniowe): "))
        
        # Przeliczenie na wartości charakterystyczne
        My = My_d / 1.4
        N = Nd / 1.4
        
    else:
        print("Niepoprawny wybór. Proszę wybrać 'charakterystyczne' lub 'obliczeniowe'.")
        return get_characteristic_influences()  # Rekurencyjnie pytamy ponownie, jeśli wybór był niepoprawny
    
    # Pobranie wartości Siły sprężającej śruby Fs
    Fs = float(input("Podaj wartość Siły sprężającej śruby Fs: "))
    
    # Zwracanie wartości My, N i Fs
    return My, N, Fs

def holes_definition(): 
    # Pobieranie wartości n - ilość otworów na śruby
    while True:
            n = int(input("Podaj całkowitą ilość otworów na śruby w podkładce (n) w dwóch rzędach, (liczba parzysta): "))
            if n % 2 == 0:
                break
            else:
                print("Ilość otworów (n) musi być liczbą parzystą. Spróbuj ponownie.")
    
    
    # Pobieranie wartości e2 - pionowy dystans między osiami centralnymi rzędów śrub
    e2 = float(input("Podaj pionowy dystans między osiami centralnymi rzędów śrub (e2): "))
    
    # Pobieranie wartości d - średnica otworu na śruby w podkładce
    d = float(input("Podaj średnicę otworu na śruby w podkładce (d): "))
    
    # Zwracanie wartości na zewnątrz funkcji
    return n, e2, d

def z0_calculation(n, Fs, N, My, he):
     z0 = int(((n * Fs - N) / (12 * My) * he ** 2)/1000)
     print ("z0= ", z0)
     return z0

def hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2):
    #Obliczenie wartości hm i sigma_vorh
    if z0 > he / 2:
        print("Neutral axis is outside of crossection -> Only pressures appear in crossection.")
        hm = int((he + 2 * My * 1000/ (N - n * Fs)))
        print ("hm= ", hm, "mm")
        sigma_vorh = (N - n * Fs)**2 * 1000 / (be * (he * (N - n * Fs) + 2 * My * 1000))           ### zaokrąglić najpierw w górę
        sigma_vorh = round(sigma_vorh, 2)
        print ("sigma_vorh =  ", sigma_vorh, "MPa")
        return hm, sigma_vorh
    else:
        print("Neutral axis is within the cross-section -> Tension and pressure areas exist.")
        F = int((N - n * Fs)/he * (he/2 - z0) + 6* My * 1000/he**3 * (he**2/4 - z0*2))                       ### przeliczyć jednostki
        print ("F= " , F, "kN")                   
        hm = int(he + (2 * My * 1000 - F * e2) / (N - n * Fs - F))                                         ### przeliczyć jednostki
        print ("hm= " , hm, "mm")
        sigma_vorh = (N - n * Fs - F)**2 * 1000 / (be * (he * (N - n * Fs - F) + 2 * My * 1000 - F * e2))          ### przeliczyć jednostki  ### zaokrąglić najpierw w górę
        sigma_vorh = round(sigma_vorh, 2)
        print ("sigma_vorh = " , sigma_vorh, "MPa")

        # Jeśli z0 > he / 2, zwracamy tylko hm i sigma_vorh
        return hm, sigma_vorh

def edge_distance_check(dr, te): # Funkcja sprawdzająca, czy odległość krawędziowa dr jest większa od te
    if dr > te:
        print("Dla te=", te, "mm, zalecana odległość krawędziowa dr powinna wynościć co najmniej tyle co te.")

def screws_in_pressured_area_check(he, hm, be, d, n, sigma_zul): # Funkcja sprawdzająca, czy śruby znajdują się w obszarze ściskanym
    te = 5 ########################## do zmiany
    
    if hm <= 2 / 3 * he:
        print("Only one row of screws is in pressured area.")

        S = (hm * be - math.pi * d**2 / 2) / (te * (2 * hm + 2 * be + 2 * math.pi * d))
        sigma_zul = (S **2 + S + 1 ) / 0.7

        if sigma_zul > 30:
            sigma_zul = 30

        return sigma_zul

    else:
        S = (hm * be - n * math.pi * d ** 2 / 4) / (te * (2 * hm + 2 * be + n * math.pi * d))
        sigma_zul = (S **2 + S + 1 ) / 0.7

        if sigma_zul > 30:
            sigma_zul = 30
        
        return sigma_zul

def stress_proof (sigma_vorh, sigma_zul): # Funkcja sprawdzająca, czy naprężenia są mniejsze niż wartość dopuszczalna
    if abs(sigma_vorh) < sigma_zul:
        print("Stress is less than allowable stress.")
    else:
        print("Stress is greater than allowable stress.")

def main():
    ##### te = [ 5, 10, 15, 20]

    # Wywołanie funkcji i zwrócenie wartości he, be, My, N, Fs, n, e2, d
    he, be = geometry_decision()

    My, N, Fs = get_characteristic_influences()

    n, e2, d = holes_definition()

    z0 = z0_calculation(n, Fs, N, My, he)

    hm, sigma_vorh = hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2)

    screws_in_pressured_area_check(he, hm, be, d, n)
    
    sigma_zul = screws_in_pressured_area_check(he, hm, be, d, n, sigma_zul)


if __name__ == "__main__":
    main()