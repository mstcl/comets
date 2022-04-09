#!/usr/bin/env python
"""
Set up folders of bulk density values from 400-700
in increments of 10
"""

import os
import shutil
import numpy as np
from modules import helper


def make_directories():
    """
    Create folders if they don't exist
    """
    values = np.linspace(400,700,31,endpoint=True)
    for val in values:
        path = f'{int(val)}'
        if not os.path.exists(path):
            os.makedirs(path)

def copy_files():
    """
    :returns: TODO

    """
    values = np.linspace(400,700,31,endpoint=True)
    files = ["rpg.par", "ss.par", "ssdraw.par"]
    for val in values:
        val = int(val)
        for file in files:
            helper.check_file(f'./default/{file}')
            shutil.copy(f'./default/{file}', f'./{val}/ssdraw.par')

def change_density():
    """
    :returns: TODO

    """
    values = np.linspace(400,700,31,endpoint=True)
    for val in values:
        val = int(val)
        helper.check_file(f"./{val}/rpg.par")
        with open(f"./{val}/rpg.par", "r", encoding="utf-8") as file:
            data = [line.split("\t\t") for line in file.readlines()]
        data[36][1] = str(val)
        with open(f"./{val}/rpg.par", "w", encoding="utf-8") as new_file:
            new_file.writelines(['\t\t'.join(line) for line in data])

if __name__ == "__main__":
    make_directories()
    copy_files()
    change_density()
