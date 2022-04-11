#!/usr/bin/env python
"""Change into 5 directories at a time, run automate.sh in each directory"""

from asyncio.subprocess import PIPE
import time
import asyncio
import warnings
import numpy as np
from modules import helper

warnings.filterwarnings("ignore", category=DeprecationWarning)


async def run(shell_command):
    """
    Run shell command in the background
    Print stdout and stderr to async.log
    """
    logfile = open("async.log", "ab")
    prg = await asyncio.create_subprocess_shell(
        shell_command, stdin=PIPE, stdout=PIPE, stderr=logfile
    )
    return (await prg.communicate())[0].splitlines()


async def main():
    """
    Driver code
    """
    # It is recommended to keep the maximmum async tasks to around 10-20.
    helper.check_file("./scripts/initiate.py")
    with open("./scripts/initiate.py", "r", encoding="utf-8") as file:
        data = [line.strip("\n") for line in file.readlines()]

    # This should point to the correct lines in initiate.py
    start_val = int(data[62].split(" = ")[-1])
    end_val = int(data[63].split(" = ")[-1])
    step = int(data[64].split(" = ")[-1])

    groups = [
        [start_val + (step * 10) * i + 5, start_val + (step * 10) * (i + 1)]
        for i in range(0, int((end_val - start_val) / (step * 10)))
    ]
    groups[0][0] -= 5
    for group in groups:
        print(f"Running for values between {group[0]}-{group[1]}")
        start_density = group[0]
        end_density = group[1]
        values = np.linspace(
            start_density,
            end_density,
            int((end_density - start_density) / step) + 1,
            endpoint=True,
        )
        commands = [
            run(f"./scripts/automate_from_parent.sh {int(val)}") for val in values
        ]
        for task in asyncio.as_completed(commands):
            await task


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    total = time.time() - start
    print(f"Total time {total} s.")
