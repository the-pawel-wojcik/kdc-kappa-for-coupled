#!/usr/bin/env python3

import argparse
import json
import matplotlib.pyplot as plt

au_to_cm = 219474.629370


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('pes_file')
    args = parser.parse_args()
    return args


def main():
    # args = get_args()
    # with open(args.pes_file, 'r') as pes_file_obj:
    #     pes = json.load(pes_file_obj)

    # filename = '../sample_data/nu5-mulliken-pes_cm.json'
    filename = '../sample_data/nu8-mulliken-pes_cm.json'
    with open(filename, 'r') as pes_file_obj:
        pes = json.load(pes_file_obj)

    fig, ax = plt.subplots(figsize=(3.555555, 2), layout='constrained')

    dq = pes["displacements, dQ (DNC)"]
    ax.plot(dq, pes['B3u, cm-1'], label=r"$1^1B_{3u}$")
    ax.set_xlabel(r"$Q _8$ (DNC)")
    ax.set_ylabel(r"E, cm$^{-1}$")

    b2u = pes['B2u, cm-1']
    min_e_b2u = min(b2u)
    b2u = [ee - min_e_b2u for ee in b2u]
    lbl = r"$1^1B_{2u}$" + f" - {min_e_b2u:4.0f}" + r" cm$^{-1}$"
    ax.plot(dq, b2u, label=lbl)

    ax.legend()

    plt.show()


if __name__ == "__main__":
    main()
