#!/usr/bin/env python3

import argparse
import json
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

au_to_cm = 219474.629370


def poly_2(x: float, a: float, b: float, c: float) -> float:
    return 0.5 * a * x ** 2 + b * x + c


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

    fig, ax = plt.subplots(figsize=(3.555555, 2), layout='constrained')

    dq = pes["displacements, dQ (DNC)"]
    b3u = pes['B3u, cm-1']
    ax.plot(dq, b3u, label=r"$1^1B_{3u}$")
    ax.set_xlabel("dQ (DNC)")
    ax.set_ylabel(r"E, cm$^{-1}$")

    b2u = pes['B2u, cm-1']
    min_e_b2u = min(b2u)
    b2u = [ee - min_e_b2u for ee in b2u]
    ax.plot(dq, b2u, label=r"$1^1B_{2u}$")

    kappas_b3u, pcov = curve_fit(f=poly_2, xdata=dq, ydata=b3u)
    print("Kappas for B3u:")
    print(f" 1st: {kappas_b3u[0]:6.1f}")
    print(f" 2nd: {kappas_b3u[1]:6.1f}")

    kappas_b2u, pcov = curve_fit(f=poly_2, xdata=dq, ydata=b2u)
    print("Kappas for B2u:")
    print(f" 1st: {kappas_b2u[0]:6.1f}")
    print(f" 2nd: {kappas_b2u[1]:6.1f}")

    ax.legend()

    plt.show()


if __name__ == "__main__":
    main()
