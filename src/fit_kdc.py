#!/usr/bin/env python3

import argparse
import json
import scipy.optimize as sopt
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
    # filename = args.pes_file
    # filename = '../sample_data/pyrazine/nu5-mulliken-pes_cm.json'
    filename = '../sample_data/pyrazine/nu8-mulliken-pes_cm.json'
    print(f"Using {os.path.basename(filename)}")
    with open(filename, 'r') as pes_file_obj:
        pes = json.load(pes_file_obj)

    dq = pes["displacements, dQ (DNC)"]
    b3u = pes['B3u, cm-1']
    b2u = pes['B2u, cm-1']
    min_b2u = min(b2u)
    b2u_shifted = [b - min_b2u for b in b2u]

    initial_guess = (0, 1000, 0, 1000)

    def target_function(kappas: tuple[float, float, float, float]):
        sum = 0.0
        for lower, upper, q in zip(b3u, b2u_shifted, dq):
            sum += abs(lower - ab_initio_down(q, *kappas))
            sum += abs(upper - ab_initio_up(q, *kappas))
        return sum

    optimization_result: sopt.OptimizeResult = sopt.minimize(
        fun=target_function,
        x0=initial_guess,
        method='nelder-mead',
    )

    kappas_optimized = optimization_result.x
    success = optimization_result.success

    print(f"Has the minimization converged: {success}")

    print("Fitted kappas:")
    print("B3u:")
    print(f" 1st: {kappas_optimized[0]:6.1f}")
    print(f" 2nd: {kappas_optimized[1]:6.1f}")
    print("B2u:")
    print(f" 1st: {kappas_optimized[2]:6.1f}")
    print(f" 2nd: {kappas_optimized[3]:6.1f}\n")


if __name__ == "__main__":
    main()
