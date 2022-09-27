#! python3
import argparse
from aiohttp import ClientSession
import asyncio
from settings import DEFAULT_PORT, DESCRIPTION, ALIVE_SYMBOL


def prompt():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION)

    parser.add_argument("filePath",
                        nargs='*', metavar="file_Pame", type=str,
                        help="The file containing function to be exposed.")

    args = parser.parse_args()

    if not args.filePath:
        print("No file path provided")
        return
    files = args.filePath

    targetServer = f'http://localhost:{DEFAULT_PORT}'

    async def main():
        async with ClientSession() as session:
            async with session.get(targetServer+'/isAlive') as resp:
                if resp.status == 200 and await resp.text() == ALIVE_SYMBOL["python"]:
                    for fileName in files:
                        async with session.get(targetServer+f'/register?filePath={fileName}') as resp:
                            t = await resp.text()
                            print(t)
                else:
                    print('fff')

            print('enddd')

    asyncio.run(main())


prompt()
