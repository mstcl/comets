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
    plt.ylabel(r"Disruption distance at threshold separation / km", fontsize=13)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.xlabel(r"Comet's bulk density / kg/m$^3$", fontsize=13)
    plt.title(
        "Effect of bulk density of a comet on its\n Roche limit (wrt Jupiter) as produced by pkdgrav",
        fontsize=13,
    )
    plt.errorbar(
        data[1][1:],
        data[2][1:],
        yerr=data[3][1:],
        color="mediumpurple",
        marker="x",
        label="range",
        ls="None",
        ms=2,
        capsize=2,
    )
    plt.tight_layout()
    plt.savefig("./roche_limit_density.png", format="png", dpi=150)


if __name__ == "__main__":
    main()
