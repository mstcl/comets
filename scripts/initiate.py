#!/usr/bin/env python
"""
Set up folders of bulk density values from 400-700
in increments of 10
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
    for val in values:
        val = int(val)
        for file in files:
            helper.check_file(f"./default/{file}")
            shutil.copy(f"./default/{file}", f"./{val}/{file}")


def change_density(start: int, end: int, step: int):
    """
    Open rpg.par and change the appropriate value (density in the default case)
    """
    values = np.linspace(start, end, int((end - start) / step) + 1, endpoint=True)
    for val in values:
        val = int(val)
        helper.check_file(f"./{val}/rpg.par")
        with open(f"./{val}/rpg.par", "r", encoding="utf-8") as file:
            data = [line.split("\t\t") for line in file.readlines()]
        # line 50 is the bulk density quantity, to alter another quantity,
        # read 'rpg.par' to find out which line needs to be changed
        # data[36][1] = str(val)  # density
        data[38][1] = f"{str(val)} {str(val)} {str(val)}"  # bulk semi-axes
        with open(f"./{val}/rpg.par", "w", encoding="utf-8") as new_file:
            new_file.writelines(["\t\t".join(line) for line in data])


if __name__ == "__main__":
    START_DENSITY = 400
    END_DENSITY = 1015
    STEP = 5
    make_directories(START_DENSITY, END_DENSITY, STEP)
    copy_files(START_DENSITY, END_DENSITY, STEP)
    change_density(START_DENSITY, END_DENSITY, STEP)
