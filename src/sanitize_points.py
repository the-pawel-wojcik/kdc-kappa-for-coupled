#!/usr/bin/env python3

import argparse
import json

au_to_cm = 219474.629370


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('pes_file')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    with open(args.pes_file, 'r') as pes_file_obj:
        pes = json.load(pes_file_obj)

    min_energy_au = min(pes['B3u au'])
    b3u = [
        (energy_au - min_energy_au) * au_to_cm for energy_au in pes['B3u au']
    ]
    b2u = [
        (energy_au - min_energy_au) * au_to_cm for energy_au in pes['B2u au']
    ]

    print(json.dumps({
        'displacements, dQ (DNC)': pes['displacements'],
        'B3u, cm-1': b3u,
        'B2u, cm-1': b2u,
    }))


if __name__ == "__main__":
    main()
