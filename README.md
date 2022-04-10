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

## Usage & Documentations

### Sanitation and recommendations

It is recommended to keep the main branch clean and make a branch for every
iteration. Note that the main top directory is the repository top directory.
Whichever quantity one is varying (density, size, etc.), it is possible to
batch create multiple directories named after the value provided in `rpg.par`.
This is the intended way the scripts were written. To do this, execute
`initiate.py` to create a directory for each value of the varying quantity.

```shell
$ git checkout -b some_branch_name
$ ./scripts/initiate.py
```

### Changing default quantity and range of values

Alternatively, edit line `56-58` in `initiate.py`, i.e. the following variables
to change how many folders are generated. These variables are so-called
"densities" but to vary any other quantity such as radius, number of particles,
the code should still work. To change the quantity being varied, un/comment the
necessary files in `initiate.py`, `plot_roche.py` and
`plot_and_analyse_bt.py`.

```python3
# scripts/initiate.py
START_VALUE = 300
END_VALUE = 600
STEP = 5
```

### Running simulations asynchronously

Next, if varying **density** (default) and sticking to the default range (300-600 $kg/m^3$ bulk density), start running the automation scripts asynchronously, in the top directory, execute the following commands:

```shell
$ ./scripts/run_in_parallel.py
```

Nothing will be piped to `STDOUT` except the simulation time at the end. Look
at `async.log` created automatically in the top directory to check for runtime
errors and warnings.

If default range is changed in `initiate.py`, `run_in_parallel.py` will read
this and set the number of asynchronous tasks to 10 in the correct step size.

### Running simulations manually

If running tasks asynchronously is not preferred, or there is a need to perform
certain simulations manually, then in each simulation directory, execute
`automate.sh`. For example:

```shell
$ cd 500 # go into density value 500
$ ../scripts/automate.sh
```

### Performing some but not all tasks

In some cases, it is necessary to rerun `automate.sh`, either through
`run_in_parallel.py` or manually, not from the beginning, but at some
intermediate steps to avoid rerunning the same tasks and wasting time
(especially rerunning `plot_and_analyse_bt.py` for data analysis), to do this,
comment out any lines of `automate.sh` responsible for each task.

Note that it's not necessary to rerun a task and everything _after_ it for
completeness, however, this does apply to some:

- Modifying `rpg.par` requires rerunning everything (steps 1-7), as this changes the rubber pile itself.
- Modifying `ss.par` requires rerunning `pkdgrav` and everything after it (steps 4-7).
- Modifying `plot_and_analyse_bt.py` requires rerunning itself only, _ceteris paribus_ (step 7).
- Modifying `rpx.py` requires running `rpx.sh` and everything after it (steps 3-7).
- Running `draw.sh` is an optional step because it stitches together to produce a video of the simulation, unnecessary for data analysis it can be omitted to greatly speed up total running time (step 6).

### Post-run data analysis

Once all simulations within the range provided are completed, `results.txt`
will be populated (all results are appended, not overwritten, this means if
everything is run, there will be many duplicates. If this is a problem or
annoyance, simply delete the content of the file (or copy it elsewhere, but
don't remove `results.txt`!). Ideally, I could've used set() somewhere on the
third column (the measured value), keeping the parity of everything else, but
this is a non-issue for me.). To plot the Roche limit vs. density (or whichever
variable we're varying), run the following:

```shell
$ ./scripts/plot_roche.py
```

The file `./roche_limit_plot.png` will be generated. Copy and rename this if
it's important, because running `plot_roche.py` again will override it!

## TL;DR Summary

There are many modular scripts, but ideally, one would only need to run **in
the top directory** to get the results:

1. `initiate.py`
2. `run_in_parallel.py`
3. `plot_roche.py`

If there are anything that needs manual intervention, run
**in the simulation directory**:

1. `automate.sh`

## LICENSE

The project is licensed under GNU General Public License v3.
Scripts required but not provided are due to unknown licensing and distributing permission.
