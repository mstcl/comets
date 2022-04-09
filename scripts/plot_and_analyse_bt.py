#! /usr/bin/env python3
"""
This file does 4 things:
    1. Find the average coordinates for each frame in <x,y,z>
    2. Find the range of coordinates for each frame in <x,y,z>
    3. Produce a plot with the range and averages.
    4. Output a value for the Roche limit and write it to results.txt
"""

import numpy as np
import matplotlib.pyplot as plt
from modules import helper


def get_r_std(
    xs_average: np.ndarray,
    ys_average: np.ndarray,
    zs_average: np.ndarray,
    rs_average: np.ndarray,
):
    """
    Find the error in radius
    """
    xs_std = get_cluster_data("x", "std")
    ys_std = get_cluster_data("y", "std")
    zs_std = get_cluster_data("z", "std")
    rs_std = (
        (xs_average * xs_std) ** 2
        + (ys_average * ys_std) ** 2
        + (zs_average * zs_std) ** 2
    ) ** (0.5) / rs_average
    return rs_std


def get_coords(density, particles):
    """
    Get the coordinates <x,y,z>
    for each frame, both range and mean
    """
    xs_average = get_cluster_data("x", "mean")
    ys_average = get_cluster_data("y", "mean")
    zs_average = get_cluster_data("z", "mean")
    xs_range = get_cluster_data("x", "range")
    ys_range = get_cluster_data("y", "range")
    zs_range = get_cluster_data("z", "range")
    rs_average = (xs_average**2 + ys_average**2 + zs_average**2) ** (0.5)
    rs_range = (xs_range**2 + ys_range**2 + zs_range**2) ** (0.5)
    rs_std = get_r_std(xs_average, ys_average, zs_average, rs_average)
    plot_coords("x", xs_average, xs_range, density, particles)
    plot_coords("y", ys_average, ys_range, density, particles)
    plot_coords("z", zs_average, zs_range, density, particles)
    plot_coords("r", rs_average, rs_range, density, particles)
    threshold = 4.5
    is_disrupted = exceed_threshold(max(rs_range), threshold)
    index_disrupted = helper.smallest_index(rs_range, 0, None, threshold)
    return (
        (rs_average[index_disrupted], rs_std[index_disrupted])
        if is_disrupted
        else (-1, 0)
    )


def exceed_threshold(maximum_separation, threshold):
    """
    Roche limit threshold check
    """

    return maximum_separation >= threshold


def calculate_roche_limit(density: float):
    """
    Calculate and return
    Roche limits (rigid and fluid)
    """
    rho_jupiter = 1326
    r_jupiter = 71492000

    roche_rigid = r_jupiter * (2 * (rho_jupiter / density)) ** (1 / 3) / 1000
    roche_fluid = r_jupiter * 2.4823 * (rho_jupiter / density) ** (1 / 3) / 1000

    return roche_rigid, roche_fluid


def plot_coords(
    dimension: str,
    positions: np.ndarray,
    ranges: np.ndarray,
    density: float,
    particles: int,
):
    """
    Produce a plot with matplotlib
    """
    frames = 500
    timesteps = [n + 1 for n in range(frames)]

    last = None
    if positions.argmin() != 0:
        last = positions.argmin() + 1

    roche_rigid, roche_fluid = calculate_roche_limit(density)

    plt.clf()
    plt.plot(timesteps, ranges, "b:", label="range")
    if dimension == "r":
        index_smallest_diff_rigid = helper.smallest_index(
            positions, 0, last, roche_rigid
        )
        index_smallest_diff_fluid = helper.smallest_index(
            positions, 0, last, roche_fluid
        )
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
    plt.title(
        f"Range in {dimension}-displacements of {particles} particles, {density} kg/m$^3$",
        fontsize=15,
    )
    plt.legend(loc="lower right")
    plt.savefig(f"./{dimension}_positions_range.png", format="png", dpi=150)

    plt.clf()
    plt.plot(timesteps, positions, "r:", label="average")
    if dimension == "r":
        index_smallest_diff_rigid = helper.smallest_index(
            positions, 0, last, roche_rigid
        )
        index_smallest_diff_fluid = helper.smallest_index(
            positions, 0, last, roche_fluid
        )
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
    plt.title(
        f"Mean in {dimension}-displacements of {particles} particles, {density} kg/m$^3$",
        fontsize=15,
    )
    plt.legend(loc="lower right")
    plt.savefig(f"./{dimension}_positions_mean.png", format="png", dpi=150)


def get_cluster_data(dimension: str, avg_type: str):
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
        data = [float(val) * au_km for val in data.T[dimension_key[dimension]]]
        if avg_type == "mean":
            rbp_coords[frame] = np.average(data)
        elif avg_type == "range":
            rbp_coords[frame] = np.ptp(data)
        elif avg_type == "std":
            rbp_coords[frame] = helper.find_std(np.ndarray(np.array(data)))
    return rbp_coords


def main():
    """
    Driver code
    """
    helper.check_file("./sl9_stats.txt")
    with open("./sl9_stats.txt", "r", encoding="utf-8") as file:
        data = [line.strip("\n").split(" ") for line in file.readlines()]
    particles = int(data[5][1][2:])
    density = float(data[6][3][8:])

    roche_distance, error = get_coords(density, particles)
    information = [str(particles), str(density), str(roche_distance), f"{str(error)}\n"]

    helper.check_file("../results.txt")
    with open("../results.txt", "r", encoding="utf-8") as results:
        table_results = list(results.readlines())
    table_results.append(" ".join(information))
    with open("../results.txt", "w", encoding="utf-8") as results:
        results.writelines(table_results)


if __name__ == "__main__":
    main()
