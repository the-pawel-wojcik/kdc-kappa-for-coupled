#!/usr/bin/env python3

import argparse
import json
import numpy as np
import sys
import matplotlib.pyplot as plt
import seaborn as sbs


class keyvalue(argparse.Action):
    def __call__(
            self,
            parser,
            namespace,
            values,
            option_string=None,
    ):
        setattr(namespace, self.dest, dict())

        for value in values:
            state, number_str = value.split('=')
            try:
                number = int(number_str)
            except Exception:
                print(
                    f"Error in parsing {value} from command line.",
                    f"{number_str} is not an integer",
                    file=sys.stderr
                )
                raise Exception
            getattr(namespace, self.dest)[state] = number


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
    parser.add_argument(
        '--pick_states',
        nargs='*',
        help="List of states that will be extracted. Format <name>=<number>,"
        "where <name> is a string and <number> is an integer.",
        action=keyvalue
    )
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('--show_overlaps', default=False, action='store_true')
    args = parser.parse_args()
    return args


def find_matching_amplitude(ket, amplitude) -> dict[str, float | int] | None:
    for right_amp in ket:
        if right_amp['A'] != amplitude['A']:
            continue
        if right_amp['I'] != amplitude['I']:
            continue
        return right_amp
    return None


def singles_overlap(bra: list[dict], ket: list[dict]) -> float:
    overlap: float = 0.0
    for bra_amplitude in bra:
        ket_amplitude = find_matching_amplitude(ket, bra_amplitude)
        if ket_amplitude is None:
            continue
        overlap += bra_amplitude['amplitude'] * ket_amplitude['amplitude']

    return overlap


def show_overlaps(amplitudes):
    for key, amps in amplitudes.items():
        fig, ax = plt.subplots()
        singles_matrix = np.zeros(
            shape=(len(amps), len(amps)), dtype=np.float64
        )
        for bra_idx, bras in enumerate(amps):
            bra = bras['singles']
            for ket_idx, kets in enumerate(amps):
                ket = kets['singles']
                singles_matrix[bra_idx][ket_idx] = singles_overlap(bra, ket)

        sbs.heatmap(singles_matrix, ax=ax, square=True)
        ax.set_title(key)
        plt.show()


def main():
    args = get_args()
    pick_states = args.pick_states

    energies_au = {key: list() for key in pick_states}
    amplitudes = {key: list() for key in pick_states}

    for file_id, fname in enumerate(args.roots):
        with open(fname, 'r') as file:
            roots = json.load(file)
            for state_name, state_number in pick_states.items():
                root = roots[state_number]
                energies_au[state_name].append(root['energy']['total']['au'])
                amplitudes[state_name].append(root['converged root'])
                if args.verbose:
                    print(f"{state_name} amplitudes: ", end="")
                    show_amps(root)

    # Test that all states declared as "the same" state have reasonably alike
    # amplitudes
    if args.show_overlaps is True:
        show_overlaps(amplitudes)

    out_pack = {
        state_name: {'energies, au': energies_au[state_name]}
        for state_name in pick_states
    }

    print(
        "Warning: Using x range from -0.2 to 0.2 in 17 steps",
        file=sys.stderr
    )
    displacements: np.ndarray = np.linspace(-0.2, 0.2, num=17)
    out_pack['displacements, DNC'] = displacements.tolist()

    print(json.dumps(out_pack))


if __name__ == "__main__":
    main()
