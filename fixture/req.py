from aiohttp import ClientSession


async def main():
    async with ClientSession() as session:
        async with session.get("http://localhost:23330/callFunc/paa") as resp:
            print(await resp.text())
