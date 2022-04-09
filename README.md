# Tidal disruption of a comet

This repository contains the scripts and folders necessary to analyse comet
simulations to investigate the density of a comet on its Roche's limit. The
planet used is Jupiter and the comet Shoemaker-Levy 9.

## Requirements

- python3
- `numpy`
- `matplotlib`
- POSIX-compliant systems for shell scripts.

## Required but not provided

- pkdgrav
- ssdraw
- rpg
- ss2bt & bt2ss

## Download

```
$ git clone https://github.com/mstcl/comets
$ cd comets
```
Or straight from the browser: `Code` then `Download ZIP`.

## Usage

It is recommended to keep the main branch clean and make a branch for every iteration. Then execute `initiate.py` and then in each simulation directory (named by its value, e.g. '400', '660', etc.) execute `automate.sh`. For example:

```
git checkout -b run_1
./scripts/initiate.py

```
