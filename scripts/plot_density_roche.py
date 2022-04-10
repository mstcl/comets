#!/usr/bin/env python
"""
Plot the roche limit vs density
"""

from modules import helper
import matplotlib.pyplot as plt
import numpy as np


def main():
    """
    Driver code
    """
    helper.check_file("./results.txt")
    with open("./results.txt", "r", encoding="utf-8") as file:
        data = np.array(
            [list(map(float, line.strip("\n").split(" "))) for line in file.readlines()]
        ).T
    density = data[1][0:]
    roche_limit = data[2][0:]
    errors = data[3][0:]

    rho_jupiter = 1326
    r_jupiter = 71492000

    roche_estimated_rigid = r_jupiter * (2 * (rho_jupiter / density)) ** (1 / 3) / 1000
    roche_estimated_fluid = r_jupiter * 2.4823 * (rho_jupiter / density) ** (1 / 3) / 1000

    plt.ylabel(r"Disruption distance at threshold separation / km", fontsize=13)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.xlabel(r"Comet's bulk density / kg/m$^3$", fontsize=13)
    plt.title(
        "Effect of bulk density of a comet on its\n Roche limit (wrt Jupiter) as produced by pkdgrav",
        fontsize=13,
    )
    plt.errorbar(
        density,
        roche_limit,
        yerr=errors,
        color="mediumpurple",
        marker="x",
        label="estimated",
        ls="None",
        ms=2,
        capsize=2,
    )
    # plt.plot(density, roche_estimated_rigid, 'g*', label="rigid")
    # plt.plot(density, roche_estimated_fluid, 'y*', label="fluid")
    plt.tight_layout()
    plt.savefig("./roche_limit_density.png", format="png", dpi=150)


if __name__ == "__main__":
    main()
