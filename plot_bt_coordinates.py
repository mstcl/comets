#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from modules import helper

def get_coords():
    with open("./sl9_stats.txt", "r", encoding="utf-8") as file:
        data = [line.strip("\n").split(" ") for line in file.readlines()]
    particles = data[5][1][2:]
    xs = get_cluster_average('x', particles)
    ys = get_cluster_average('y', particles)
    zs = get_cluster_average('z', particles)
    print(xs)
    plot_coords('x', xs)
    plot_coords('y', ys)
    plot_coords('z', zs)
    rs = (xs**2 + ys**2 + zs**2)**(0.5)
    plot_coords('r', rs)

def plot_coords(dimension: str, positions: np.ndarray):
    frames = 500 
    timesteps = [n+1 for n in range(frames)]
    plt.clf()
    plt.scatter(timesteps, positions, color="red")
    plt.savefig(f"./{dimension}_positions.png", format="png", dpi=150)

def get_cluster_average(dimension: str, particles: int):
    '''
    For each frame, get the average location
    of all particles
    '''
    frames = 500
    dimension_key = {'x': 4, 'y': 5, 'z': 6}
    rbp_coords = np.zeros(frames, dtype="float64")
    for frame in range(frames):
        helper.check_file(f"./output_bt/out_file.{str(frame + 1).rjust(5, '0')}.bt")
        with open(f"./output_bt/out_file.{str(frame + 1).rjust(5, '0')}.bt", "r", encoding="utf-8") as file:
            data = np.array([line.strip("\n").split(" ") for line in file.readlines()])
        rbp_coords[frame] = np.average([float(val) for val in data.T[dimension_key[dimension]]])
    return rbp_coords

if __name__ == '__main__':
    get_coords()
