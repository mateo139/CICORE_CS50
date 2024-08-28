def main(hp, bp, n, d, e2, dr, My_d, Ny, Fs):
    # Krok 1: Obliczenia he i be
    he = hp - 2 * dr
    be = bp - 2 * dr
    
    # Krok 2: Znalezienie najmniejszej wartości te
    possible_te_values = [5, 10, 15, 20]
    te = min(possible_te_values)
    
    # Krok 3: Przeliczenia My i N
    My = My_d / 1.4
    N = Ny / 1.4
    
    # Krok 4: Obliczenie z0
    z0 = (n * Fs - N) / (12 * My) * he ** 2
    
    # Krok 5: Warunki
    if z0 > he / 2:
        print("Neutral axis is outside of crossection -> Only pressures appear in crossection")
        hm = he + 2 * My / (N - n * Fs)
        print ("hm= ", hm)
        Sigma_vorh = (N - n * Fs)^2 / [be * (he * (N - n * Fs) + 2 * My)]
        print ("Sigma_vorh =  ", Sigma_vorh)
    else:
        print("Neutral axis is within the cross-section -> Tension and pressure areas exist")
        F = (N - n * Fs)/he * (he/2 - z0) + 6* My/he^3 * (he^2/4 - z0^2)
        print ("F= " , F)
        hm = he + (2 * My - F * e2) / (N - n * Fs - F)
        print ("hm= " , hm)
        Sigma_vorh = (N - n * Fs - F)^2 / [be * (he * (N - n * Fs - F) + 2 * My - F * e2)]
        print ("Sigma_vorh = " , Sigma_vorh)

    # Jeśli z0 > he / 2, zwracamy tylko hm i Sigma_vorh
    return hm, Sigma_vorh


# Pobieranie danych od użytkownika
hp = int(input("Podaj wartość hp: "))
bp = int(input("Podaj wartość bp: "))
n = int(input("Podaj wartość n: "))
d = int(input("Podaj wartość d: "))
e2 = int(input("Podaj wartość e2: "))
dr = int(input("Podaj wartość dr: "))
My_d = float(input("Podaj wartość My,d: "))
Ny = float(input("Podaj wartość Ny: "))
Fs = float(input("Podaj wartość Fs: "))

# Wywołanie funkcji
result = main(hp, bp, n, d, e2, dr, My_d, Ny, Fs) 
print(result)


#def function_1():
#    ...


#def function_2():
#    ...



#def function_n():
#    ...

#if __name__ == "__main__":
#    main()