#! /usr/bin/env python3
"""
This file does 4 things:
    1. Find the average coordinates for each frame in <x,y,z>
    2. Find the range of coordinates for each frame in <x,y,z>
    3. Produce a plot with the range and averages.
    4. Output a value for the Roche limit and write it to results.txt
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from modules import helper


def get_coords_range():
    """
    Return range in radius
    """
    xs_range = get_cluster_data("x", "range")
    ys_range = get_cluster_data("y", "range")
    zs_range = get_cluster_data("z", "range")
    return (xs_range**2 + ys_range**2 + zs_range**2) ** (0.5)


def get_coords_avg():
    """
    Get errors
    """
    xs_average = get_cluster_data("x", "mean")
    ys_average = get_cluster_data("y", "mean")
    zs_average = get_cluster_data("z", "mean")
    xs_std = get_cluster_data("x", "std")
    ys_std = get_cluster_data("y", "std")
    zs_std = get_cluster_data("z", "std")
    rs_average = (xs_average**2 + ys_average**2 + zs_average**2) ** (0.5)
    return (
        (
            (
                (xs_average * xs_std) ** 2
                + (ys_average * ys_std) ** 2
                + (zs_average * zs_std) ** 2
            )
            ** (0.5)
            / rs_average
        ),
        rs_average,
    )


def get_coords(quantity, particles: int, density: float):
    """
    Get the coordinates <x,y,z>
    for each frame, both range and mean
    """
    rs_range = get_coords_range()
    rs_std, rs_average = get_coords_avg()
    plot_coords("r", rs_average, quantity, particles, rs_std, density)

    threshold = 100  # uncomment for everything else?
    # threshold = 5 * quantity / 1000  # uncomment for bulk semi-axes

    if exceed_threshold(np.max(rs_range) - np.min(rs_range), threshold):
        index_disrupted = get_index_disrupted(rs_std)
        return (
            rs_average[index_disrupted - 0],
            rs_std[index_disrupted - 0],
            np.min(rs_average),
        )
    return (-1, 0, np.min(rs_average))


def get_index_disrupted(rs_std: np.ndarray):
    """
    Get index at disrupted distance
    """
    smooth_std = np.diff(rs_std, 4)[4:]
    range_std = (np.min(smooth_std), np.max(smooth_std))
    range_std_arg = (smooth_std.argmin(), smooth_std.argmax())
    if np.absolute(range_std_arg[1] - range_std_arg[0]) >= 10:
        index_disrupted = range_std_arg[get_biggest_index(range_std[1], range_std[0])]
    else:
        index_disrupted = np.min([range_std_arg[0], range_std_arg[1]])
    return index_disrupted


def get_biggest_index(big: float, small: float):
    """
    Return the value of the biggest absolute (keep signed)
    """
    values = [small, big]
    biggest = np.abs(values).max()
    for i, val in enumerate(values):
        if np.absolute(val) == biggest:
            return i
    return -1


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
    quantity: float,
    particles: int,
    distance_error: np.ndarray,
    density: float,
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
    plt.tight_layout()
    plt.plot(
        timesteps[5:-4],
        np.diff(distance_error, 4)[5:],
        "bx",
        label="average",
        ms=0.5,
    )

    index_smallest_diff_rigid = helper.smallest_index(positions, 0, last, roche_rigid)
    index_smallest_diff_fluid = helper.smallest_index(positions, 0, last, roche_fluid)

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
        f"4th differential of standard deviations in {dimension}-displacements\n of {particles} particles, {quantity} kg/m$^3$",
        fontsize=15,
    )  # uncomment for density

    # plt.title(
    #     f"4th differential of standard deviations in {dimension}-displacements\n of {particles} particles, {quantity} m",
    #     fontsize=15,
    # )  # uncomment for bulk semi-axes

    # plt.title(
    #     f"4th differential of standard deviations in {dimension}-displacements\n of {particles} particles",
    #     fontsize=15,
    # )  # uncomment for number of particles

    # plt.title(
    #     f"4th differential of standard deviations in {dimension}-displacements\n of {particles} particles, $e = ${quantity}",
    #     fontsize=15,
    # )  # uncomment for coefficient of restitution

    plt.legend(loc="lower right")
    plt.savefig(
        f"./{dimension}_positions_range.png", format="png", dpi=150, bbox_inches="tight"
    )

    plt.clf()
    plt.errorbar(
        timesteps,
        positions,
        yerr=distance_error,
        fmt="rx",
        label="mean",
        ms=0.5,
        capsize=2,
    )

    index_smallest_diff_rigid = helper.smallest_index(positions, 0, last, roche_rigid)
    index_smallest_diff_fluid = helper.smallest_index(positions, 0, last, roche_fluid)

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
        f"Mean in {dimension}-displacements of {particles} particles, {quantity} kg/m$^3$\n",
        fontsize=15,
    )  # uncomment for density

    # plt.title(
    #     f"Mean in {dimension}-displacements of {particles} particles\n",
    #     fontsize=15,
    # )  # uncomment for number of particles

    # plt.title(
    #     f"Mean in {dimension}-displacements of {particles} particles, {quantity} m\n",
    #     fontsize=15,
    # )  # uncomment for bulk semi-axes

    # plt.title(
    #     f"Mean in {dimension}-displacements of {particles} particles, $e = $ {quantity}\n",
    #     fontsize=15,
    # )  # uncomment for coefficient of restitution

    plt.legend(loc="best")
    plt.savefig(
        f"./{dimension}_positions_mean.png", format="png", dpi=150, bbox_inches="tight"
    )


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
            # rbp_coords[frame] = (
            #     np.max(data) + np.min(data)
            # ) / 2  # different way to calculate avg
            rbp_coords[frame] = np.average(data)
        elif avg_type == "range":
            rbp_coords[frame] = np.ptp(data)
        elif avg_type == "std":
            rbp_coords[frame] = helper.find_std(np.array(data))
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

    # quantity = (
    #     int(os.getcwd().split("/")[-1]) / 100
    # )  # uncomment for coefficient of restitution
    # in_quantity = float(quantity)  # uncomment for coefficient of resitution

    quantity = float(density)  # uncomment for density
    in_quantity = int(data[1][1][6:])  # uncomment for density

    # quantity = float(
    #     np.average(list(map(float, data[5][0][9:-1].split(","))))
    # )  # uncomment for bulk semi-axes
    # in_quantity = int(
    #     np.average(list(map(float, data[1][0][9:-1].split(","))))
    # )  # uncomment bulk semi-axes

    # quantity = int(particles)  # uncomment for particle number
    # in_quantity = int(data[1][2][3:])  # uncomment for particle number

    roche_distance, error, closest = get_coords(quantity, particles, density)
    information = [
        str(particles),
        str(quantity),
        str(roche_distance),
        str(error),
        str(closest),
        f"{in_quantity}\n",
    ]
    write_results(information)


def write_results(information: list):
    """
    Write results to results.txt
    """
    if not os.path.exists("../results.txt"):
        open("../results.txt", "x", encoding="utf-8").close()
    with open("../results.txt", "r", encoding="utf-8") as results:
        table_results = list(results.readlines())
    results.close()
    table_results.append(" ".join(information))
    with open("../results.txt", "w", encoding="utf-8") as results:
        results.writelines(table_results)
    results.close()


if __name__ == "__main__":
    main()
