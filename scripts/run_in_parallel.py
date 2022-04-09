#!/usr/bin/env python
"""Change into 5 directories at a time, run automate.sh in each directory"""

from asyncio.subprocess import PIPE, STDOUT
import time
import asyncio
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


async def run(shell_command):
    """
    Run shell command in the background
    Print stdout and stderr to async.log
    """
    logfile = open("async.log", 'ab')
    prg = await asyncio.create_subprocess_shell(
        shell_command, stdin=PIPE, stdout=PIPE, stderr=logfile
    )
    return (await prg.communicate())[0].splitlines()


async def main():
    """
    Driver code
    """
    start_density = 300
    end_density = 600
    step = 5
    values = np.linspace(
        start_density, end_density, int((end_density - start_density)/step) + 1, endpoint=True
    )
    commands = [run(f"./scripts/automate_from_parent.sh {int(val)}") for val in values]
    for task in asyncio.as_completed(commands):
        await task


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    total = time.time() - start
    print(f"Total time {total} s.")
