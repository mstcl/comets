#!/usr/bin/env python
"""
Fetch dynamical time from sl9_stats.txt
and update ss.par with it
"""

import os
from modules import helper
import numpy as np


def main():
    """
    Calculate dDelta from dynamical time
    and write it to ss.par
    """
    files = ["sl9_stats.txt", "ss.par"]
    for file in files:
        helper.check_file(file)
    with open("sl9_stats.txt", "r", encoding="utf-8") as stats:
        data = [line.split("=") for line in stats.readlines()]
    ddelta = np.format_float_scientific(
        float(data[15][1][1:-1]) / 10 / 5020000, precision=1
    )

    with open("ss.par", "r", encoding="utf-8") as sspar:
        data = [line.split("\t\t") for line in sspar.readlines()]
    data[9][1] = f"= {ddelta}"

    # uncomment this block to vary normal coefficient of restitution
    # current_val = int(os.getcwd().split("/")[-1])/100
    # data[61][1] = f"= {current_val}"

    with open("ss.par", "w", encoding="utf-8") as sspar:
        sspar.writelines(["\t\t".join(line) for line in data])



if __name__ == "__main__":
    main()

