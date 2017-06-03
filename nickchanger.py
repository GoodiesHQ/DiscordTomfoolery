#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import defaultdict
from itertools import cycle
import asyncio
import discord

async def nickchanger(client, member, names, delay=1.0):
    if getattr(nickchanger, "instances", None) is None:
        setattr(nickchanger, "instances", defaultdict(bool))
    nickchanger.instances[member.server] = not nickchanger.instances[member.server]
    for name in cycle(names):
        if nickchanger.instances[member.server] == False:
            break
        try:
            await client.change_nickname(member, name)
        except Exception as e:
            print("LOL: {}".format(e))
        finally:
            await asyncio.sleep(delay)

# DEFAULT_NAMES = tuple([let * 7 for let in __import__("string").ascii_uppercase])
# DEFAULT_NAMES = ["|", "/", "-", "\\",]
DEFAULT_NAMES = ["Austin... {}".format(c) for c in "|/-\\"]

def main():
    ap = ArgumentParser()
    ap.add_argument("--token", "-t", type=str, required=True, help="Token")
    ap.add_argument("--names", "-n", nargs="+", default=DEFAULT_NAMES, required=False)
    ap.add_argument("--delay", "-d", type=float, default=1.0)
    args = ap.parse_args()

    client = discord.Client()

    @client.event
    async def on_ready():
        print("Logged in as {}".format(client.user.name))

    @client.event
    async def on_message(message):
        await client.wait_until_ready()
        if message.author != client.user:
            return

        if message.content.startswith("./nick"):
            client.loop.create_task(nickchanger(client, message.author, DEFAULT_NAMES, args.delay))


    print(type(args.names))
    print(args.names)
    # client.loop.add_task(nickchanger(client, args.names, args.delay))
    client.run(args.token, bot=False)

if __name__ == "__main__":
    main()
