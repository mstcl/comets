#!/usr/bin/env python
"""Extract horizon data"""

from modules import helper
import matplotlib.pyplot as plt


def get_data(start: int):
    """Get array of data in km"""
    with open("horizons_results.txt", "r", encoding="utf-8") as file:
        data = [line.strip("\n").split() for line in file.readlines()[start:134:3]]
    offset = 1
    if start == 61:
        offset = 1000
    for j, coords in enumerate(data):
        for i, coord in enumerate(coords):
            if i == 2:
                data[j][i] = str(float(coord) * offset) + "\n"
            else:
                data[j][i] = str(float(coord) * offset)
    return data


def write_data(name: str, data):
    """
    Write data to file
    """
    with open(f"./{name}.txt", "w", encoding="utf-8") as file:
        file.writelines([" ".join(line) for line in data])


def main():
    """
    Driver code
    """
    # Make sure to create these files first
    # for example: $ touch positions.txt
    helper.check_file("./positions.txt")
    helper.check_file("./distances.txt")
    helper.check_file("./velocities.txt")
    position = 60
    velocity = 61
    data_position = get_data(position)
    data_velocity = get_data(velocity)
    write_data("velocities", data_velocity)
    write_data("positions", data_position)
    get_distances()


def get_distances():
    """
    Get the distances from positions.txt
    """
    with open("./positions.txt", "r", encoding="utf-8") as file:
        data = [line.strip("\n").split(" ") for line in file.readlines()]
    distances = [
        f"{(float(line[0])**2 + float(line[1])**2 + float(line[2])**2)**(1/2)}\n"
        for line in data
    ]
    with open("./distances.txt", "w", encoding="utf-8") as write_file:
        write_file.writelines("".join(distances))
    timesteps = list(range(len(distances)))
    plt.plot(timesteps, [float(line.strip("\n")) for line in distances], "rx", label="average")
    plt.title("Distance of SL9 from Jupiter", fontsize=15)
    plt.ylabel(r"$r$ / km", fontsize=13)
    plt.xlabel(r"Timestep / frame", fontsize=13)
    plt.savefig(r"distance.png", format="png", dpi=150)


if __name__ == "__main__":
    main()
