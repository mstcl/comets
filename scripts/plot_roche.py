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
    perijove = data[4][0:]
    density, roche_limit, errors = zip(*sorted(zip(density, roche_limit, errors)))
    density = np.array(density)
    dummy_density = np.linspace(100, 1000, 100)

    rho_jupiter = 1326
    r_jupiter = 71492000

    roche_estimated_rigid = (
        r_jupiter * (2 * (rho_jupiter / dummy_density)) ** (1 / 3) / 1000
    )
    roche_estimated_fluid = (
        r_jupiter * 2.4823 * (rho_jupiter / dummy_density) ** (1 / 3) / 1000
    )
    plt.clf()
    plt.ylabel(r"Disruption distance at threshold separation / km", fontsize=13)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    # plt.xlabel(r"Comet's bulk density / kg/m$^3$", fontsize=13)  # density
    plt.xlabel(r"Comet's average radius / m", fontsize=13)
    # plt.title(
    #     "Effect of bulk density of a comet on its\n Roche limit (wrt Jupiter) as produced by pkdgrav",
    #     fontsize=13,
    # )  # density
    plt.title(
        "Effect of radius of a comet on its\n Roche limit (wrt Jupiter) as produced by pkdgrav",
        fontsize=13,
    )  # bulk semi-axes
    plt.errorbar(
        density,
        roche_limit,
        yerr=errors,
        color="mediumpurple",
        marker="x",
        label="estimated disrupted distance",
        ls="None",
        ms=1,
        capsize=2,
    )
    # plt.plot(dummy_density, roche_estimated_rigid, color="g", label="rigid", alpha=0.4)  # density
    # plt.plot(
    #     dummy_density,
    #     roche_estimated_fluid,
    #     color="y",
    #     label="fluid",
    #     alpha=0.4,
    # )  # density
    plt.tight_layout()
    closest_distance = [99305.6547187192] * len(dummy_density)
    plt.ylim([np.max(closest_distance) - 2e04, np.min(roche_estimated_fluid) + 4e04])
    plt.xlim([np.min(density) - 30, np.max(density) + 30])
    plt.plot(
        dummy_density,
        closest_distance,
        color="k",
        linestyle="-",
        alpha=0.4,
        linewidth=1,
        label="actual perijove",
    )
    plt.plot(
        density,
        perijove,
        color="k",
        marker=".",
        ls="None",
        ms=1,
        label="perijove",
    )
    plt.legend(loc="best", fontsize="small")
    plt.savefig("./roche_limit_plot.png", format="png", dpi=150)


if __name__ == "__main__":
    main()
