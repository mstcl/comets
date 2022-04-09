#!/usr/bin/env python
"""Change into 5 directories at a time, run automate.sh in each directory"""

from asyncio.subprocess import PIPE, STDOUT
import time
import asyncio
import numpy as np


async def run(shell_command):
    """
    Run shell command in the background
    """
    prg = await asyncio.create_subprocess_shell(
        shell_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT
    )
    return (await prg.communicate())[0].splitlines()


async def main():
    """
    Driver code
    """
    values = np.linspace(400, 500, 11, endpoint=True)
    commands = [run(f"./automate_from_parent.sh {val}") for val in values]
    for task in asyncio.as_completed(commands):
        print(await task)


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    total = time.time() - start
    print(f"Total time {total} s.")
