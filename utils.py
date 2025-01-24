"Engineering calculations functions:"


def geometry_decision(choice, hp=None, bp=None, dr=None, he=None, be=None):
    "Function for geometry definition"
    if choice == "p":
        he = hp - 2 * dr
        be = bp - 2 * dr
    elif choice == "b":
        he = he
        be = be
    return he, be


def get_characteristic_influences(choice, My=None, N=None, My_d=None, Nd=None, Fs=None):
    "Function for characteristic influences definition"
    if choice == "c":
        return My, N, Fs
    elif choice == "d":
        My = My_d / 1.4
        N = Nd / 1.4
        return My, N, Fs


def holes_definition(n, e2, d):
    "Function for holes definition"
    return n, e2, d


def z0_calculation(n, Fs, N, My, he):
    "Function for calculation of zero pressure point z0"
    z0 = int(((n * Fs - N) / (12 * My) * he**2) / 1000)
    return z0


def hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2):
    "Function for calculation of equivalent height hm and stress sigma_vorh"
    if z0 > he / 2:
        hm = int((he + 2 * My * 1000 / (N - n * Fs)))
        sigma_vorh = (
            (N - n * Fs) ** 2 * 1000 / (be * (he * (N - n * Fs) + 2 * My * 1000))
        )
    else:
        F = int(
            (N - n * Fs) / he * (he / 2 - z0)
            + 6 * My * 1000 / he**3 * (he**2 / 4 - z0 * 2)
        )
        hm = int(he + (2 * My * 1000 - F * e2) / (N - n * Fs - F))
        sigma_vorh = (
            (N - n * Fs - F) ** 2
            * 1000
            / (be * (he * (N - n * Fs - F) + 2 * My * 1000 - F * e2))
        )
    return F, hm, round(sigma_vorh, 2)
