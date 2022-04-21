#!/usr/bin/env python
"""
1. Set up folders of values in a given range
in increments of given step
2. Change the necessary value in rpg.par
"""

import os
import shutil
import numpy as np
from modules import helper


def make_directories(start: int, end: int, step: int):
    """
    Create the following directories if they don't exist
    """
    values = np.linspace(start, end, int((end - start) / step) + 1, endpoint=True)
    for val in values:
        path = f"{int(val)}"
        if not os.path.exists(path):
            os.makedirs(path)


def copy_files(start: int, end: int, step: int):
    """
    Copy all parameter files from the default folder
    to newly created directories
    """
    values = np.linspace(start, end, int((end - start) / step) + 1, endpoint=True)
    files = ["rpg.par", "ss.par", "ssdraw.par"]
    # files = [
    #     "rpg.par",
    #     "ss.par",
    #     "ssdraw.par",
    #     "sl9_stats.txt",
    #     "sl9_crash.ss",
    # ]  # uncomment this to vary coefficient of restitution
    for val in values:
        val = int(val)
        for file in files:
            helper.check_file(f"./default/{file}")
            shutil.copy(f"./default/{file}", f"./{val}/{file}")


def change_value(start: int, end: int, step: int):
    """
    Open rpg.par and change the appropriate value (density in the default case)
    """
    values = np.linspace(start, end, int((end - start) / step) + 1, endpoint=True)
    for val in values:
        val = int(val)
        helper.check_file(f"./{val}/rpg.par")
        with open(f"./{val}/rpg.par", "r", encoding="utf-8") as file:
            data = [line.split("\t\t") for line in file.readlines()]

        # data[36][1] = str(val)  # uncomment to change to density

        data[38][
            1
        ] = f"{str(val)} {str(val)} {str(val)}"  # uncomment to change to bulk semi-axes

        # data[39][1] = str(val)  # uncomment to change to particle number

        with open(f"./{val}/rpg.par", "w", encoding="utf-8") as new_file:
            new_file.writelines(["\t\t".join(line) for line in data])


if __name__ == "__main__":
    START_VALUE = 400
    END_VALUE = 1000
    STEP = 5
    make_directories(START_VALUE, END_VALUE, STEP)
    copy_files(START_VALUE, END_VALUE, STEP)
    change_value(
        START_VALUE, END_VALUE, STEP
    )  # comment this out if varying coefficient of restitution
