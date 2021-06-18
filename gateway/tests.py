import asyncio
from aiohttp import ClientSession
import aiohttp

urls = ['http://39.103.236.234:10003/', 'http://39.103.236.234:10003/']


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        print(html)


tasks = [get(x) for x in urls]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*tasks))
