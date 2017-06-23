#!/usr/bin/env python3

import discord
import asyncio
import time
import contextlib
from random import SystemRandom
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("Running without uvloop.")

random = SystemRandom()
loop = asyncio.get_event_loop()
client = discord.Client(loop=loop)
DEFAULT_MESSAGES = ("?", "lmao", "rofl", "hey", "??", "ayy", sup)
AUTOSAYERS = dict()
DEFAULT_PERIOD = 60.0
AUTODELETE = True

class AutoSay:
    def __init__(self, client, channel, messages=DEFAULT_MESSAGES, period=DEFAULT_PERIOD):
        self.client = client
        self.channel = channel
        self.messages = messages
        self.period = period
        self.running = True
        self.task = None

    def stop(self):
        if self.running:
            with contextlib.suppress(Exception):
                self.task.cancel()
            self.task = None
            self.running = False

    def start(self):
        self.running = True
        self.task = self.client.loop.create_task(self.say())

    async def say(self):
        while True:
            msg = await self.client.send_message(self.channel, random.choice(self.messages))
            print("Sending message")
            if AUTODELETE:
                await client.delete_message(msg)
            await asyncio.sleep(self.period)

def trycast(new_type, value, default=None):
    try:
        default = new_type(value)
    finally:
        return default

@client.event
async def on_message(message):
    if message.author != client.user or not message.content.startswith("./autosay") or ' ' not in message.content:
        return
    args = message.content.split(' ')[1:]
    if len(args) < 1:
        return

    period = DEFAULT_PERIOD

    with contextlib.suppress(IndexError):
        period = trycast(float, args[1], period)

    if args[0].lower() == "start":
        if message.channel not in AUTOSAYERS:
            tmp = AutoSay(client, message.channel, period=period)
            AUTOSAYERS[message.channel] = tmp
            tmp.start()

    if args[0].lower() == "stop":
        await client.send_message(message.channel, "Stopping...")
        if message.channel in AUTOSAYERS:
            AUTOSAYERS[message.channel].stop()
            del AUTOSAYERS[message.channel]

    await client.delete_message(message)

@client.event
async def on_ready():
    print("Logged in as {} ({})".format(client.user.name, client.user.id))

client.run("mfa.B8k_lVhXet3zszeAuMkkcIJNuxjaU3AhpPUBb2icsw2WGM5M8tvLaeoaCgMHa065CkEUX6YO2_x_1XQjdwbg", bot=False) #gitignore
client.run("TOKEN", bot=False)
