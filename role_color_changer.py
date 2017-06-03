#!/usr/bin/env python3
from argparse import ArgumentParser
from colorsys import hsv_to_rgb
import asyncio
import discord
import random
import sys

__author__ = "Austin Archer (Goodies)"

def make_gradient(count):
    colors = []
    for i in range(count):
        r, g, b = [int(f * 255 + 0.5) for f in hsv_to_rgb(i / count, 1, 1)]
        colors.append(r << 16 | g << 8 | b)
    return colors

if __name__ == "__main__":
    ap = ArgumentParser()
    ap.add_argument("--server-name", "-s", type=str, required=True, help="The name of the server")
    ap.add_argument("--role-name", "-r", type=str, required=True, help="The name of the role")
    ap.add_argument("--delay", "-d", type=float, default=0.1, help="Delay between color changes")
    ap.add_argument("--colors", "-c", type=int, default=50, help="The number of colors for the gradient (higher = more subtle color changes)")
    args = ap.parse_args()
    SERVER_NAME = args.server_name
    ROLE_NAME = args.role_name
    DELAY = args.delay
    COLORS = make_gradient(args.colors)
    REVERSE = False

client = discord.Client()

def get_role_by_name(server, role_name):
    for role in server.roles:
        if role.name == role_name:
            return role
    return None

def get_server_by_name(server_name):
    for server in client.servers:
        if server.name == server_name:
            return server
    return None

async def change_color(server_name, role_name):
    global COLORS
    server = get_server_by_name(server_name)
    if server is None:
        print("No server with the name '{}' exists.".format(server_name))
        return False
    role = get_role_by_name(server, role_name)
    if role is None:
        print("No role with the name '{}' exists.".format(role_name))
        return False
    while True:
        for color in COLORS:
            try:
                await client.edit_role(server, role, color=discord.Color(color))
                await asyncio.sleep(DELAY)
            except Exception as e:
                print(color)
                print(e)
        if REVERSE:
            COLORS = list(reversed(COLORS))

@client.event
async def on_ready():
    print("Logged in as {} ({})".format(client.user.name, client.user.id))
    client.loop.create_task(change_color(SERVER_NAME, ROLE_NAME))

client.run("TOKEN", bot=False)
