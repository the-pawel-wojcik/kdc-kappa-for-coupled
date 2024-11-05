#!/usr/bin/env python3

import argparse
import json
import numpy as np


def show_amps(root):
    singles = root['converged root']['singles']
    for single in singles:
        amp = single['amplitude']
        if abs(amp) < 0.1:
            continue
        print(f"{single['A']:3d} {single['I']:3d} {amp:4.2f}")

    doubles = root['converged root']['doubles']
    for double in doubles:
        amp = double['amplitude']
        if abs(amp) < 0.1:
            continue
        print(f"{double['A']:3d} {double['B']:3d}"
              f" {double['I']:3d} {double['I']:3d}"
              f" {amp:4.2f}")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('roots', nargs='+')
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    b3u_energies = list()
    b2u_energies = list()
    for file_id, fname in enumerate(args.roots):
        with open(fname, 'r') as file:
            roots = json.load(file)
            b3u_root = roots[0]
            b3u_energies.append(b3u_root['energy']['total']['au'])
            if args.verbose:
                print("1B3u amplitudes: ", end="")
                show_amps(b3u_root)
            b2u_root = roots[1]
            b2u_energies.append(b2u_root['energy']['total']['au'])
            if args.verbose:
                print("1B2u amplitudes: ", end="")
                show_amps(b2u_root)

    displacements = np.linspace(-0.2, 0.2, num=17)

    print(json.dumps({
        'displacements': [d for d in displacements],
        'B3u au': b3u_energies,
        'B2u au': b2u_energies,
    }))


if __name__ == "__main__":
    main()
