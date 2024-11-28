#!/usr/bin/env python3

import argparse
import json
import matplotlib
import matplotlib.pyplot as plt
from sp_text import str_to_tex

au_to_cm = 219474.629370


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('pes_file')
    args = parser.parse_args()
    return args


def plot_adiabatic_pes(ax: matplotlib.axes.Axes, pes: dict):
    """
    pes['displacements, DNC'] is a list of floats
    pes['states'] is a dictionary:
        its keys are the state names
        its values are:
            'min energy, cm-1': float
            'energies, cm-1': list[float]
    """
    dq: list[float] = pes["displacements, DNC"]
    states: dict = pes['states']
    global_pes_min = min(
        [state['min energy, cm-1'] for state in states.values()]
    )
    for state_name, state_props in states.items():
        pes = state_props['energies, cm-1']
        pes_min = state_props['min energy, cm-1']
        energy_shift = pes_min - global_pes_min

        label = str_to_tex(state_name.split()[0])
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

    plot_adiabatic_pes(ax, pes)

    # fitted_kappas = {
    #     'kappa1A': 0.0,
    #     'kappa2A': 651.9,
    #     'kappa1B': 0.0,
    #     'kappa2B': 861.4,
    # }
    # fitted_lower = [ab_initio_down(q, **fitted_kappas) for q in dq]
    # fitted_upper = [ab_initio_up(q, **fitted_kappas) for q in dq]

    # ax.scatter(dq, fitted_lower, s=8)
    # ax.scatter(dq, fitted_upper, s=8)

    plt.show()


if __name__ == "__main__":
    main()
