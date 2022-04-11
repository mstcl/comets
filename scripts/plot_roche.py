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
    quantity = data[1][0:]
    roche_limit = data[2][0:]
    errors = data[3][0:]
    perijove = data[4][0:]
    quantity, roche_limit, errors = zip(*sorted(zip(quantity, roche_limit, errors)))
    minimum_quantity_no_disruption = quantity[np.array(roche_limit).argmin()]
    quantity = np.array(quantity)
    dummy_quantity = np.linspace(100, 1000, 100)
    closest_distance = [99305.6547187192] * len(dummy_quantity)

    rho_jupiter = 1326
    r_jupiter = 71492000

    roche_estimated_rigid = (
        r_jupiter * (2 * (rho_jupiter / dummy_quantity)) ** (1 / 3) / 1000
    )
    roche_estimated_fluid = (
        r_jupiter * 2.4823 * (rho_jupiter / dummy_quantity) ** (1 / 3) / 1000
    )

    ########################
    #  GENERAL PLOT STUFF  #
    ########################

    plt.clf()
    plt.tight_layout()

    plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

    plt.ylim([np.max(closest_distance) - 2e04, np.min(roche_estimated_fluid) + 4e04])
    plt.xlim([np.min(quantity) - 30, np.max(quantity) + 30])

    plt.ylabel(r"Disruption distance at threshold separation / km", fontsize=13)

    plt.errorbar(
        quantity,
        roche_limit,
        yerr=errors,
        color="mediumpurple",
        marker="x",
        label="estimated disrupted distance",
        ls="None",
        ms=1,
        capsize=2,
    )

    plt.plot(
        dummy_quantity,
        closest_distance,
        color="k",
        linestyle="-",
        alpha=0.2,
        linewidth=1,
        label="actual perijove",
    )

    plt.plot(
        quantity,
        perijove,
        color="k",
        marker=".",
        ls="None",
        ms=1,
        label="perijove",
    )
    if minimum_quantity_no_disruption < 0:
        plt.axvline(
            minimum_quantity_no_disruption,
            color="r",
            linestyle="-",
            linewidth=1,
            alpha=0.2,
            label="minimum distance of coalescence",
        )

    #####################
    #  PARTICLE NUMBER  #
    #####################

    plt.xlabel(
        r"Number of particles", fontsize=13
    )

    plt.title(
        "Effect of number of particles of a comet rubber pile on its\n Roche limit (wrt Jupiter) as produced by pkdgrav",
        fontsize=13,
    )

    ####################
    #  BULK SEMI-AXES  #
    ####################

    # plt.xlabel(
    #     r"Comet's average radius / m", fontsize=13
    # )

    # plt.title(
    #     "Effect of radius of a comet on its\n Roche limit (wrt Jupiter) as produced by pkdgrav",
    #     fontsize=13,
    # )

    #############
    #  DENSITY  #
    #############

    plt.xlabel(r"Comet's bulk density / kg/m$^3$", fontsize=13)

    plt.title(
        "Effect of bulk density of a comet on its\n Roche limit (wrt Jupiter) as produced by pkdgrav",
        fontsize=13,
    )

    plt.plot(
        dummy_quantity, roche_estimated_rigid, color="g", label="rigid satellite", alpha=0.2
    )

    plt.plot(
        dummy_quantity,
        roche_estimated_fluid,
        color="y",
        label="fluid satellite",
        alpha=0.2,
    )

    #######################
    #  ADD LEGEND & SAVE  #
    #######################

    plt.legend(loc="best", fontsize="small")
    plt.savefig("./roche_limit_plot.png", format="png", dpi=150)


if __name__ == "__main__":
    main()
