#!/usr/bin/env python
"""Plot final_range.txt"""

from modules import helper
import numpy as np
import matplotlib.pyplot as plt


def main():
    """
    Driver code
    """
    helper.check_file("./final_range.txt")
    with open("./final_range.txt", "r", encoding="utf-8") as file:
        data = np.array(
            [list(map(float, line.strip("\n").split(" "))) for line in file.readlines()]
        ).T
    radius = data[0][0:]
    final_range = data[1][0:]
    plt.clf()
    plt.tight_layout()
    # plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    # plt.xlim([np.min(radius) - 30, np.max(radius) + 30])
    plt.ylabel(r"Range of extreme particles at end of simulation / km", fontsize=13)
    plt.plot(
        radius,
        final_range,
        color="k",
        marker=".",
        ls="None",
        ms=1,
    )
    plt.xlabel(
        r"Comet's average radius / m", fontsize=13
    )
    plt.title(
        "Effect of radius on comet's final disrupted length",
        fontsize=13,
    )
    plt.savefig("./final_range.png", format="png", dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    main()
