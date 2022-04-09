#!/usr/bin/env python
"""Change into 5 directories at a time, run automate.sh in each directory"""

import time
import asyncio
from asyncio.subprocess import PIPE, STDOUT


async def run(shell_command):
    p = await asyncio.create_subprocess_shell(shell_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    return (await p.communicate())[0].splitlines()


async def main():
    commands = [run('./automate_from_parent.sh'.format(i=i)) for i in range(5)]
    for f in asyncio.as_completed(commands):
        print(await f)


start = time.time()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

total = time.time() - start

print("Total time {} s".format(total))
