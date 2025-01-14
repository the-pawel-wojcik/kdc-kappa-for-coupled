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

    displacements = pes['displacements, DNC']
    del pes['displacements, DNC']
    cleared_states = dict()
    for state_name, state_props in pes.items():
        energies_au = state_props['energies, au']
        min_energy_au = min(energies_au)
        energies_cm = [(energy_au - min_energy_au) * au_to_cm
                       for energy_au in energies_au]
        cleared_states[state_name] = {
            'energies, cm-1': energies_cm,
            'min energy, cm-1': min_energy_au * au_to_cm,
        }

    states = [
        {'name': state_name, **cleared_states[state_name]}
        for state_name in cleared_states
    ]
    states.sort(key=lambda x: x['min energy, cm-1'])

    out_pack = {
        'displacements, DNC': displacements,
        'states': states,
    }

    print(json.dumps(out_pack))


if __name__ == "__main__":
    main()
