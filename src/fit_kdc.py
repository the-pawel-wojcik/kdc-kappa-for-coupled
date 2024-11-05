#!/usr/bin/env python3

import argparse
import json
from scipy.optimize import curve_fit
import os

au_to_cm = 219474.629370


def poly_2(x: float, a: float, b: float, c: float) -> float:
    return 0.5 * a * x ** 2 + b * x + c


def lambda_plus(a: float, b: float, c: float) -> float:
    return 0.5 * (a + b + pow((a-b)**2 + 4 * c ** 2, 0.5))


def lambda_minus(a: float, b: float, c: float) -> float:
    return 0.5 * (a + b - pow((a-b)**2 + 4 * c ** 2, 0.5))


def ab_initio_down(
    q: float,
    kappa1A: float,
    kappa2A: float,
    kappa1B: float,
    kappa2B: float,
) -> float:
    kappa0A = 0
    kappa0B = 7708.064447455473
    lambda1AB = 1560
    a = kappa0A + kappa1A * q + 0.5 * kappa2A * q**2
    b = kappa0B + kappa1B * q + 0.5 * kappa2B * q**2
    c = lambda1AB * q
    return lambda_minus(a, b, c)


def ab_initio_up(
    q: float,
    kappa1A: float,
    kappa2A: float,
    kappa1B: float,
    kappa2B: float,
) -> float:
    kappa0A = 0
    kappa0B = 7708.064447455473
    lambda1AB = 1560
    a = kappa0A + kappa1A * q + 0.5 * kappa2A * q**2
    b = kappa0B + kappa1B * q + 0.5 * kappa2B * q**2
    c = lambda1AB * q
    return lambda_plus(a, b, c) - kappa0B


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('pes_file')
    args = parser.parse_args()
    return args


def main():
    # args = get_args()
    # with open(args.pes_file, 'r') as pes_file_obj:
    #     pes = json.load(pes_file_obj)

    filename = '../sample_data/nu5-mulliken-pes_cm.json'
    filename = '../sample_data/nu8-mulliken-pes_cm.json'
    print(f"Using {os.path.basename(filename)}")
    with open(filename, 'r') as pes_file_obj:
        pes = json.load(pes_file_obj)

    dq = pes["displacements, dQ (DNC)"]
    b3u = pes['B3u, cm-1']

    initial_guess = [0, 1000, 0, 1000]
    kappas_from_b3u, pcov = curve_fit(
        f=ab_initio_down,
        xdata=dq,
        ydata=b3u,
        p0=initial_guess,
    )
    print("Kappas from fitting to B3u:")
    print("B3u:")
    print(f" 1st: {kappas_from_b3u[0]:6.1f}")
    print(f" 2nd: {kappas_from_b3u[1]:6.1f}")
    print("B2u:")
    print(f" 1st: {kappas_from_b3u[2]:6.1f}")
    print(f" 2nd: {kappas_from_b3u[3]:6.1f}\n")

    b2u = pes['B2u, cm-1']
    min_b2u = min(b2u)
    b2u_shifted = [b - min_b2u for b in b2u]
    kappas_from_b2u, pcov = curve_fit(
        f=ab_initio_up,
        xdata=dq,
        ydata=b2u_shifted,
        p0=initial_guess,
    )
    print("Kappas from fitting to B2u:")
    print("B3u:")
    print(f" 1st: {kappas_from_b2u[0]:6.1f}")
    print(f" 2nd: {kappas_from_b2u[1]:6.1f}")
    print("B2u:")
    print(f" 1st: {kappas_from_b2u[2]:6.1f}")
    print(f" 2nd: {kappas_from_b2u[3]:6.1f}\n")


if __name__ == "__main__":
    main()
