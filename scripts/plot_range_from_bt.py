#! /usr/bin/env python3
"""
This file does 4 things:
    1. Find the average coordinates for each frame in <x,y,z>
    2. Find the range of coordinates for each frame in <x,y,z>
    3. Produce a plotwith the range and averages.
    4. Output a value for the Roche limit and write it to results.txt
"""

import numpy as np
import matplotlib.pyplot as plt
from modules import helper


def get_coords():
    """
    Get the coordinates <x,y,z>
    for each frame, both range and mean
    """
    with open("./sl9_stats.txt", "r", encoding="utf-8") as file:
        data = [line.strip("\n").split(" ") for line in file.readlines()]
    particles = int(data[5][1][2:])
    density = float(data[6][3][8:])
    xs_average = get_cluster_data("x", True)
    ys_average = get_cluster_data("y", True)
    zs_average = get_cluster_data("z", True)
    xs_range = get_cluster_data("x", False)
    ys_range = get_cluster_data("y", False)
    zs_range = get_cluster_data("z", False)
    plot_coords("x", xs_average, xs_range, density)
    plot_coords("y", ys_average, ys_range, density)
    plot_coords("z", zs_average, zs_range, density)
    rs_average = (xs_average**2 + ys_average**2 + zs_average**2) ** (0.5)
    print(f"Closest distance {min(rs_average)}")
    rs_range = (xs_range**2 + ys_range**2 + zs_range**2) ** (0.5)
    print(f"Range at this distance {rs_range[rs_average.argmin()]}")
    plot_coords("r", rs_average, rs_range, density)


def plot_coords(
    dimension: str, positions: np.ndarray, ranges: np.ndarray, density: float
):
    """
    Produce a plot with matplotlib
    """
    frames = 500
    timesteps = [n + 1 for n in range(frames)]

    # Jupiter's values
    rho_jupiter = 1326
    r_jupiter = 71492000

    # roche limits in km
    roche_rigid = r_jupiter * (2 * (rho_jupiter / density)) ** (1 / 3) / 1000
    roche_fluid = r_jupiter * 2.4823 * (rho_jupiter / density) ** (1 / 3) / 1000
    last = None
    if positions.argmin() != 0:
        last = positions.argmin() + 1
    plt.clf()
    plt.plot(timesteps, ranges, "b:", label="range")
    if dimension == "r":
        # find nearest value and index to the roche limits
        index_smallest_diff_rigid = np.absolute(positions[:last] - roche_rigid).argmin()
        index_smallest_diff_fluid = np.absolute(positions[:last] - roche_fluid).argmin()
        plt.axvline(
            index_smallest_diff_rigid,
            color="g",
            linestyle="-",
            linewidth=1,
            label="rigid body",
        )
        plt.axvline(
            index_smallest_diff_fluid,
            color="y",
            linestyle="-",
            linewidth=1,
            label="fluid body",
        )
    plt.ylabel(rf"$\Delta$ ${dimension}$ / km", fontsize=13)
    plt.xlabel(r"Timestep / frame", fontsize=13)
    plt.title(f"Range in {dimension}-displacements of particles", fontsize=15)
    plt.legend(loc="lower right")
    plt.savefig(f"./{dimension}_positions_range.png", format="png", dpi=150)

    plt.clf()
    plt.plot(timesteps, positions, "r:", label="average")
    if dimension == "r":
        # find nearest value and index to the roche limits
        index_smallest_diff_rigid = np.absolute(positions[:last] - roche_rigid).argmin()
        index_smallest_diff_fluid = np.absolute(positions[:last] - roche_fluid).argmin()
        plt.axvline(
            index_smallest_diff_rigid,
            color="g",
            linestyle="-",
            linewidth=1,
            label="rigid body",
        )
        plt.axvline(
            index_smallest_diff_fluid,
            color="y",
            linestyle="-",
            linewidth=1,
            label="fluid body",
        )
    plt.ylabel(rf"${dimension}$ / km", fontsize=13)
    plt.xlabel(r"Timestep / frame", fontsize=13)
    plt.title(f"Mean in {dimension}-displacements of particles", fontsize=15)
    plt.legend(loc="lower right")
    plt.savefig(f"./{dimension}_positions_mean.png", format="png", dpi=150)


def get_cluster_data(dimension: str, mean: bool):
    """
    For each frame, get the average location
    of all particles if true, else get range
    """
    frames = 500
    dimension_key = {"x": 4, "y": 5, "z": 6}
    au_km = 1.49597870691e8
    rbp_coords = np.zeros(frames, dtype="float64")
    for frame in range(frames):
        helper.check_file(f"./bt_files/out_file.{str(frame + 1).rjust(5, '0')}.bt")
        with open(
            f"./bt_files/out_file.{str(frame + 1).rjust(5, '0')}.bt",
            "r",
            encoding="utf-8",
        ) as file:
            data = np.array([line.strip("\n").split(" ") for line in file.readlines()])
        if mean:
            rbp_coords[frame] = np.average(
                [float(val) * au_km for val in data.T[dimension_key[dimension]]]
            )
        else:
            rbp_coords[frame] = np.ptp(
                [float(val) * au_km for val in data.T[dimension_key[dimension]]]
            )
    return rbp_coords


if __name__ == "__main__":
    get_coords()
