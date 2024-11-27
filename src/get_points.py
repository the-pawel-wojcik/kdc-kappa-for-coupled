#!/usr/bin/env python3

import argparse
import json
import numpy as np
import sys


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
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    pick_states = args.pick_states

    energies = {key: list() for key in pick_states}
    for file_id, fname in enumerate(args.roots):
        with open(fname, 'r') as file:
            roots = json.load(file)
            for state_name, state_number in pick_states.items():
                root = roots[state_number]
                energies[state_name].append(root['energy']['total']['au'])
                if args.verbose:
                    print(f"{state_name} amplitudes: ", end="")
                    show_amps(root)
    out_pack = {
        state_name + " au": energies[state_name]
        for state_name in pick_states
    }

    print(
        "Warning: Using x range from -0.2 to 0.2 in 17 steps",
        file=sys.stderr
    )
    displacements: np.ndarray = np.linspace(-0.2, 0.2, num=17)
    out_pack['displacements'] = displacements.tolist()

    print(json.dumps(out_pack))


if __name__ == "__main__":
    main()
