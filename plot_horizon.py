#!/usr/bin/env python3

position = 60
velocity = 61

with open("horizons_results.txt", "r", encoding="utf-8") as file:
    data = [line.strip("\n").split() for line in file.readlines()[velocity:133:3]]

exponent = 0
for j, coords in enumerate(data):
    for i, coord in enumerate(coords):
        if coord[-3] == "+":
            exponent = 10**(int(coord[-2:]))
        else:
            exponent = 10**(-int(coord[-2:]))
        if i == 2:
            data[j][i] = str(float(coord[:-4])*exponent) + "\n"
        else:
            data[j][i] = str(float(coord[:-4])*exponent)
        


with open("./velocities.txt", "w", encoding="utf-8") as file:
    file.writelines([" ".join(line) for line in data])
