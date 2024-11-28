#!/usr/bin/env python3

import argparse
import json
import matplotlib
import matplotlib.pyplot as plt
from fit_kdc import ab_initio_up, ab_initio_down
from sp_text import str_to_tex

au_to_cm = 219474.629370


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('pes_file')
    parser.add_argument(
        '--kappas_json',
        help='Plot also the fitted potential.',
    )
    args = parser.parse_args()
    return args


def plot_adiabatic_pes(
        ax: matplotlib.axes.Axes,
        dq: list[float],
        states: list[dict]):
    """
    each of states has:
        'name': str
        'min energy, cm-1': float
        'energies, cm-1': list[float]
    """
    global_pes_min = min([state['min energy, cm-1'] for state in states])
    for state in states:
        pes = state['energies, cm-1']
        pes_min = state['min energy, cm-1']
        energy_shift = pes_min - global_pes_min

        label = str_to_tex(state['name'])
        if energy_shift > 1.0:
            label += f"$ - {energy_shift:.0f}$" + r" cm$^{-1}$"

        ax.plot(dq, pes, label=label)

    ax.set_xlabel(r"$Q$ (DNC)")
    ax.set_ylabel(r"E, cm$^{-1}$")
    ax.legend(
        draggable=True,
        handlelength=0.8,
        handletextpad=0.4,
        borderpad=0.4,
        labelspacing=0.2,
    )
    return ax


def main():
    args = get_args()
    filename = args.pes_file
    # filename = '../sample_data/pyrazine/nu5-mulliken-pes_cm.json'
    # filename = '../sample_data/pyrazine/nu8-mulliken-pes_cm.json'
    # filename = '../sample_data/pyrazine/nu8-mulliken-broad-pes_cm.json'
    with open(filename, 'r') as pes_file_obj:
        pes = json.load(pes_file_obj)

    fig_height_in = 2
    fig, ax = plt.subplots(
        figsize=(fig_height_in * 16 / 9, fig_height_in),
        layout='constrained',
    )

    dq = pes['displacements, DNC']
    ax = plot_adiabatic_pes(ax, dq, pes['states'])
    if args.kappas_json is not None:
        with open(args.kappas_json, 'r') as kappas_json:
            fitted_kappas = json.load(kappas_json)

        dq = pes['displacements, DNC']
        gap = pes['states'][1]['min energy, cm-1']
        gap -= pes['states'][0]['min energy, cm-1']
        fitted_lower = [ab_initio_down(q, gap, **fitted_kappas) for q in dq]
        fitted_upper = [ab_initio_up(q, gap, **fitted_kappas) for q in dq]

        ax.scatter(dq, fitted_lower, s=8)
        ax.scatter(dq, fitted_upper, s=8)

    plt.show()


if __name__ == "__main__":
    main()
