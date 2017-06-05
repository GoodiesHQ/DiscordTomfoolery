#!/usr/bin/env python3
from argparse import ArgumentParser, ArgumentError
import aiohttp
import asyncio
import re

def create_headers(token):
    return {
        "authorization": token,
        "X-Context-Properties": token,
    }

def readfile(filename):
    with open(filename, "r") as fin:
        return [line.strip() for line in fin]

def inv_to_api(invite):
    code = re.search(r"https://discord.gg/(\S*)", invite)
    if not code:
        raise ArgumentError
    return "https://discordapp.com/api/v6/invite/{}".format(code.groups(1)[0])

async def join_server(api_url, token, sem):
    try:
        async with sem:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=create_headers(token), timeout=3.0) as resp:
                    if resp.status != 200:
                        print("Failure: ({}) {}".format(rep.status, api_url))
    except Exception as e:
        print(e)

async def main():
    ap = ArgumentParser()
    ap.add_argument("--tokens", "-t", required=True, type=str, help="Filename containing a list of okens")
    ap.add_argument("--invite", "-i", required=True, type=inv_to_api, help="The discord invite link code.")
    ap.add_argument("--connections", "-c", type=int, default=50, help="Number of concurrent connections")
    args = ap.parse_args()
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
