#!/usr/bin/env python3
"""
A collection of various discord-related tools.
"""

from argparse import ArgumentParser, ArgumentError
import re
import asyncio
import aiohttp


def create_headers(token):
    "Template for headers"

    return {
        "authorization": token,
        "X-Context-Properties": token,
    }

def readfile(filename):
    "Reads a file and returns file.readlines equivalent output."

    with open(filename) as fin:
        return list(map(str.strip, fin))

def inv_to_api(invite):
    "Changes an abstracted invite link into its API constituent"

    code = re.search(r"https://discord.gg/(\S*)", invite)
    if not code:
        raise ArgumentError
    return "https://discordapp.com/api/v6/invite%s" % code.groups(1)[0]

async def join_server(api_url, token, sem):
    "Joins a Discord server"

    try:
        async with sem:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=create_headers(token), timeout=3) as resp:
                    if resp.status != 200:
                        print("Failure: (%s) %s" % (resp.status, api_url))
                        print(await resp.text())
    except Exception as exc:
        print(exc)

async def main():
    parser = ArgumentParser()
    parser.add_argument("--tokens", "-t",
                        required=True,
                        type=str,
                        help="Filename containing a list of okens")

    parser.add_argument("--invite",
                        "-i",
                        required=True,
                        type=inv_to_api,
                        help="The discord invite link code.")

    parser.add_argument("--connections",
                        "-c",
                        type=int,
                        default=50,
                        help="Number of concurrent connections")

    args = parser.parse_args()
    tokens = readfile(args.tokens)
    sem = asyncio.BoundedSemaphore(args.connections)
    tasks = [join_server(args.invite, token, sem) for token in tokens]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
