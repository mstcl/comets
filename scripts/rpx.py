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


def overwrite_data(data):
    """
    Overwrite data with the offset
    """
    start_position = 4
    start_velocity = 7
    au_m = 1.49597870691e11
    km_au = 6.68e-9
    pkdtime_s = 5.019e6
    # convert km to AU
    offset_position = (
        np.array([-414139.74434847705, 277323.6402236369, -1231468.367968793]) * km_au
    )
    # convert m/s to AU/year/2pi
    offset_velocity = (
        np.array([3491.2634066288088, -6314.208154956334, 11582.300480804977])
        * pkdtime_s
        / au_m
    )
    for i, line in enumerate(data):
        # offset positions on line i
        for position in range(start_position, start_position + 3):
            data[i][position] = str(np.format_float_scientific(
                float(line[position]) + offset_position[position - start_position]
            ))
        # offset velocities on line i
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
