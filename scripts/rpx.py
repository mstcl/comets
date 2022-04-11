#!/usr/bin/env python
"""
Offset velocities and positions
like what rpx would do
Reads "sl9.bt" and writes to "sl9_crash.bt"
"""

from modules import helper
import numpy as np


def main():
    """
    Driver code
    """
    helper.check_file("./sl9.bt")
    data = get_data()
    data = overwrite_data(data)
    write_data(data)


def get_data():
    """
    Get data from sl9.bt
    """
    with open("./sl9.bt", "r", encoding="utf-8") as file:
        data = [line.split(" ") for line in file.readlines()]
    return data



def get_offset(filename: str):
    """
    Get the offset for position and velocity
    """
    step = 0
    with open(f"../{filename}.txt", "r", encoding="utf-8") as file:
        data = [list(map(float, line.strip("\n").split(" "))) for line in file.readlines()]
    return np.array(data[step])

def overwrite_data(data):
    """
    Overwrite data with the offset
    """
    start_position = 4
    start_velocity = 7
    au_m = 1.49597870691e11
    km_au = 6.68e-9
    pkdtime_s = 5.019e6
    offset_position = get_offset("positions") * km_au
    offset_velocity = get_offset("velocities") * pkdtime_s / au_m
    for i, line in enumerate(data):
        for position in range(start_position, start_position + 3):
            data[i][position] = str(np.format_float_scientific(
                float(line[position]) + offset_position[position - start_position]
            ))
        for velocity in range(start_velocity, start_velocity + 3):
            data[i][velocity] = str(np.format_float_scientific(
                float(line[velocity]) + offset_velocity[velocity - start_velocity]
            ))
    return data


def write_data(data):
    """
    Write data to sl9_crash.bt
    """
    helper.check_file("./sl9_crash.bt")
    with open("./sl9_crash.bt", "w", encoding="utf-8") as file:
        file.writelines([" ".join(line) for line in data])


if __name__ == "__main__":
    main()
