#!/usr/bin/env python
from argparse import ArgumentParser
import asyncio
import aiohttp
import json

class WebHooker:
    _headers = {"Content-Type": "application/json"}

    def __init__(self, webhook:str, username:str, avatar_url:str, content:str, count:int, loop:asyncio.AbstractEventLoop=None):
        self.__loop = loop or asyncio.get_event_loop()
        self.__webhook = webhook
        self.__count = count
        self.__sem = asyncio.BoundedSemaphore(1)  # maybe support multiple webhooks later?
        self.__data = json.dumps(dict(avatar_url=avatar_url, content=content, username=username))

    async def __aenter__(self, *args,  **kwargs):
        return self

    async def __aexit__(self, *args, **kwargs):
        """Might do something later"""
        return True

    async def _send(self, session):
        async with self.__sem:
            try:
                async with session.post(self.__webhook, headers=self._headers, data=self.__data) as resp:
                    x = await resp.text()
                    print(x)
            except Exception as e:
                print(e)
            finally:
                await asyncio.sleep(0.35)

    async def spam(self):
        print("Spamming...")
        async with aiohttp.ClientSession(loop=self.__loop) as session:
            tasks = [self._send(session) for _ in range(self.__count)]
            await asyncio.gather(*tasks, loop=self.__loop)

async def main():
    ap = ArgumentParser()
    ap.add_argument("--webhook", "-w", type=str, required=True, help="The Webhook URL")
    ap.add_argument("--name", "-n", type=str, required=True, help="The name you want to appear on the Bot")
    ap.add_argument("--avatar-url", "-a", type=str, default="", help="The avatar image file")
    ap.add_argument("--message", "-m", type=str, required=True, help="The content of the message")
    ap.add_argument("--count", "-c", type=int, default=10, help="The number of messages to spam.")
    args = ap.parse_args()
    async with WebHooker(args.webhook, args.name, args.avatar_url, args.message, args.count) as wh:
        await wh.spam()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
