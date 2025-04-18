"Engineering calculations functions:"

from math import pi


def geometry_decision(choice, hp=None, bp=None, dr=None, he=None, be=None):
    "Function for geometry definition"
    if choice == "p":
        he = hp - 2 * dr
        be = bp - 2 * dr
    elif choice == "b":
        he = he
        be = be
    return he, be


def get_characteristic_influences(choice, My=None, N=None, Fs=None):
    "Function for characteristic influences definition"
    if choice == "c":
        return My, N, Fs
    elif choice == "d":
        My = My / 1.4
        N = N / 1.4
        return My, N, Fs


def holes_definition(n, e2, d):
    "Function for holes definition"
    return n, e2, d


def z0_calculation(n, Fs, N, My, he):
    "Function for calculation of zero pressure point z0"
    z0 = int(((n * Fs - N) / (12 * My) * he**2) / 1000)
    return z0


def hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2):
    "Function for calculation of equivalent height hm and equialent compression stresses sigma_vorh"
    if z0 > he / 2:
        "Case 1: only compression"
        hm = int((he + 2 * My * 1000 / (N - n * Fs)))
        sigma_vorh = (
            (N - n * Fs) ** 2 * 1000 / (be * (he * (N - n * Fs) + 2 * My * 1000))
        )
        F = 0  # [kN]
    else:
        "Case 2: tension and compression"
        F = int(
            (N - n * Fs) / (he / 1000) * ((he / 1000) / 2 - z0 / 1000)
            + 6 * My / (he / 1000) ** 3 * ((he / 1000) ** 2 / 4 - (z0 / 1000) ** 2)
        )
        hm = int(he + (2 * My * 1000 - F * e2) / (N - n * Fs - F))
        sigma_vorh = (
            (N - n * Fs - F) ** 2
            * 1000
            / (be * (he * (N - n * Fs - F) + 2 * My * 1000 - F * e2))
        )
    return F, hm, abs(round(sigma_vorh, 2))


def shape_factor_and_allowable_stresses_calculation(he, hm, be, n, d, te):
    if hm <= 2 / 3 * he:
        "Case A: One row of screws under compression"
        S = (hm * be - n / 2 * pi * d**2 / 4) / (
            te * (hm * 2 + be * 2 + n / 2 * pi * d)
        )
        sigma_all = min(30, (S**2 + S + 1) / 0.70)

    else:
        hm > 2 / 3 * he
        "Case B: Two rows of screws under compression"
        S = (hm * be - n * pi * d**2 / 4) / (te * (2 * hm + 2 * be + n * pi * d))
        sigma_all = min(30, (S**2 + S + 1) / 0.70)

    return round(S, 1), round(sigma_all, 2)


def stresses_verification(sigma_vorh, sigma_all, verification_status):
    "Function for verification of stresses"
    if sigma_vorh <= sigma_all:
        verification_status = "Fulfilled"
    else:
        verification_status = "Not fulfilled"
    return verification_status
