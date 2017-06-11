#!/usr/bin/env python3

import aiohttp
import asyncio
import discord
import json
import urllib

DEBUGGING = True

def debug(*args, **kwargs):
    if DEBUGGING:
        print(*args, **kwargs)

client = discord.Client()

def chatbot_url(user_id:str, message:str, bot_id=1):
    return "http://api.program-o.com/v2/chatbot/?bot_id={}&convo_id={}&format=json&say={}".format(bot_id, user_id, urllib.parse.quote(message, safe=''))

@client.event
async def on_ready():
    print("Running with user {}#{}".format(client.user.name, client.user.discriminator))

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    if not any(map(message.content.startswith, "<@{cid}> <@!{cid}>".format(cid=client.user.id).split())):
        if client.user in message.mentions:
            debug("Invalid Message:", message.content, sep="\n")
        return
    msg = ' '.join(message.content.split(' ')[1:])
    url = chatbot_url(message.author.id, msg)
    debug("URL: {}".format(url))
    await client.send_typing()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10.0) as resp:
                resp = json.loads(await resp.text())["botsay"]
    except asyncio.TimeoutError:
        resp = "Sorry, the API timed out."
    except json.decoder.JSONDecodeError:
        resp = "Sorry, the API returned invalid JSON."
    except Exception as e:
        resp = "Sorry, an error occurred: {}".format(e)
    finally:
        await client.send_message(message.channel, "<@!{}>, {}".format(message.author.id, resp))

client.run("TOKEN", bot=False)

