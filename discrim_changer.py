#!/usr/bin/env python3
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
import asyncio
import discord
import random
import re
import threading

MAIN_THREAD = threading.current_thread()
UPDATE_DELAY = 10
DEFAULT_DISCRIMS = ("(\\d)\\1{3}", "1234", "9876", "(\\d)\\1(\\d)\\2", "000\\d")

class DiscrimChanger(discord.Client):
    def __init__(self, username, password, desired_discrims, **kwargs):
        super().__init__(**kwargs)
        self.__dc_username = username
        self.__dc_password = password
        self.__dc_discrims = desired_discrims
        self.loop.create_task(self.change_discrim())

    async def change_discrim(self):
        await self.wait_until_ready()
        await asyncio.sleep(UPDATE_DELAY)  # let all the accounts update
        print("Checking {} servers".format(len(self.servers)))

        sleep = False
        while True:
            try:
                if sleep:
                    await asyncio.sleep(60 * 30)  # only once per 30 minutes
                    sleep = False
                discrim = lambda m: m.discriminator
                collisions = tuple({m.name for m in self.get_all_members() if discrim(m) == discrim(self.user) and m != self.user})
                print(collisions)

                if len(collisions) == 0:
                    print("No valid collisions just yet")
                    sleep = True
                    continue
                await self.edit_profile(username=random.choice(collisions), password=self.__dc_password)
                await asyncio.sleep(UPDATE_DELAY)  # wait for server to update info
                msg = "Email: {:<30} Discrim: {:<5} Username: {:<30} ID: {}"
                print(msg.format(self.__dc_username, self.user.discriminator, self.user.name, self.user.id))
                if any(pat.search(self.user.discriminator) for pat in self.__dc_discrims):
                    print("Good one found! Stopping")
                    return
            except KeyboardInterrupt:
                exit(0)
            except Exception as e:
                raise
                print(e)
            finally:
                sleep = True

def run_bot(username, password, token, preferred_discrims):
    if threading.current_thread() != MAIN_THREAD:
        t = threading.current_thread()
        asyncio.set_event_loop(asyncio.new_event_loop())

    loop = asyncio.get_event_loop()
    client = DiscrimChanger(username, password, preferred_discrims, loop=loop)

    @client.event
    async def on_ready():
        print("Logged in with {} ID: {}".format(client.user.name, client.user.id))

    client.run(token, bot=False)

def readfile(filename):
    if filename is None:
        return None
    try:
        with open(filename, "r") as f:
            return list(map(str.rstrip, f))
    except Exception:
        raise

def parse_accounts(accounts):
    parsed = []
    for account in accounts:
        if account.count(":") < 2:
            continue
        tmp = account.split(":")
        u, p, t = tmp[0], ':'.join(tmp[1:-1]), tmp[-1]
        parsed.append((u, p, t))
    return parsed

def main():
    ap = ArgumentParser()
    ap.add_argument("--accounts", "-a", type=str, required=True, help="Text file containing username:password:token")
    ap.add_argument("--discrims", "-d", type=str, default=None, help="Text file containing the preferred discriminators in regex format")
    args = ap.parse_args()

    accounts = parse_accounts(readfile(args.accounts))
    discrims = list(map(re.compile, readfile(args.discrims) or DEFAULT_DISCRIMS))

    pool = ThreadPoolExecutor(len(accounts))
    futures = [pool.submit(partial(run_bot, *login, discrims)) for login in accounts]

    for x in as_completed(futures):
        print(x.exception())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
