#!/usr/bin/env python3

import argparse
import json
import scipy.optimize as sopt
import os
import sys
import numpy

lambda1AB = 1560
au_to_cm = 219474.629370


def poly_2(x: float, a: float, b: float, c: float) -> float:
    return 0.5 * a * x ** 2 + b * x + c


def lambda_plus(a: float, b: float, c: float) -> float:
    return 0.5 * (a + b + pow((a-b)**2 + 4 * c ** 2, 0.5))


def lambda_minus(a: float, b: float, c: float) -> float:
    return 0.5 * (a + b - pow((a-b)**2 + 4 * c ** 2, 0.5))


def ab_initio_down(
    q: float,
    vertical_gap: float,
    kappa1A: float,
    kappa2A: float,
    kappa1B: float,
    kappa2B: float,
) -> float:
    kappa0A = 0
    kappa0B = vertical_gap
    a = kappa0A + kappa1A * q + 0.5 * kappa2A * q**2
    b = kappa0B + kappa1B * q + 0.5 * kappa2B * q**2
    c = lambda1AB * q
    return lambda_minus(a, b, c)


def ab_initio_up(
    q: float,
    vertical_gap: float,
    kappa1A: float,
    kappa2A: float,
    kappa1B: float,
    kappa2B: float,
) -> float:
    kappa0A = 0
    kappa0B = vertical_gap
    a = kappa0A + kappa1A * q + 0.5 * kappa2A * q**2
    b = kappa0B + kappa1B * q + 0.5 * kappa2B * q**2
    c = lambda1AB * q
    return lambda_plus(a, b, c) - kappa0B


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('pes_file')
    out_opt = parser.add_mutually_exclusive_group()
    out_opt.add_argument(
        '--json',
        help='Save output as a JSON file.',
        default=False,
        action='store_true',
    )
    out_opt.add_argument(
        '--verbose',
        help='Print results to the standard output as a text.',
        default=False,
        action='store_true',
    )
    args = parser.parse_args()
    return args


def fit_two_states(
        lower: dict,
        upper: dict,
        dq: list[float]
) -> sopt.OptimizeResult:
    """
    Returns the fitted kappas.
    """
    shift = upper['min energy, cm-1'] - lower['min energy, cm-1']
    lower_pes = lower['energies, cm-1']
    upper_pes = upper['energies, cm-1']

    def target_function(kappas: tuple[float, float, float, float]):
        sum = 0.0
        for lwr, uppr, q in zip(lower_pes, upper_pes, dq):
            sum += abs(lwr - ab_initio_down(q, shift, *kappas))
            sum += abs(uppr - ab_initio_up(q, shift, *kappas))
        return sum

    initial_guess = (0, 1000, 0, 1000)
    optimization_result: sopt.OptimizeResult = sopt.minimize(
        fun=target_function,
        x0=initial_guess,
        method='nelder-mead',
    )
    return optimization_result


def print_optimized_kappas(kappas: list[float], lower, upper):
    print("Fitted kappas:")
    print(f"{lower['name']}:")
    print(f" 1st: {kappas[0]:6.1f}")
    print(f" 2nd: {kappas[1]:6.1f}")
    print(f"{upper['name']}:")
    print(f" 1st: {kappas[2]:6.1f}")
    print(f" 2nd: {kappas[3]:6.1f}\n")


def main():
    args = get_args()
    filename = args.pes_file
    with open(filename, 'r') as pes_file_obj:
        pes = json.load(pes_file_obj)

    dq = pes["displacements, DNC"]
    states = pes['states']

    if len(states) == 2:
        fitting_out = fit_two_states(lower=states[0], upper=states[1], dq=dq)

        success = fitting_out.success
        if success is False:
            raise RuntimeError("The minimization failed.")

        if args.verbose is True:
            print("The minimization converged.")
        kappas: numpy.ndarray = fitting_out.x
        if args.verbose is True:
            print_optimized_kappas(
                kappas=kappas,
                lower=states[0],
                upper=states[1],
            )
        elif args.json is True:
            print(json.dumps({
                'kappa1A': kappas[0],
                'kappa2A': kappas[1],
                'kappa1B': kappas[2],
                'kappa2B': kappas[3],
            }))
    else:
        print("Only two-state fit is implemented."
              f" Input aks for a {len(states)}-state fit.",
              file=sys.stderr)
        exit(0)


if __name__ == "__main__":
    main()
