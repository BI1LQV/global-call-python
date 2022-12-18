#! python3
import argparse
import os
from aiohttp import ClientSession
import asyncio
from settings import DEFAULT_PORT, DESCRIPTION, ALIVE_SYMBOL
import urllib.parse
from colorama import Fore, Style


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
            try:
                async with session.get(targetServer+'/isAlive') as resp:
                    if (resp.status == 200 and
                            await resp.text() == ALIVE_SYMBOL["python"]):
                        for fileName in files:
                            params = urllib.parse.urlencode({
                                "filePath": fileName,
                                "workingPath": os.getcwd()
                            })
                            async with session.get(
                                f'{targetServer}/funcRegister?{params}'
                            ) as resp:
                                funcName = await resp.text()
                                print(f'{Fore.BLUE}{funcName}{Style.RESET_ALL} \
                                registered on {Fore.RED}{targetServer}{Style.RESET_ALL}')
            except:
                pass

            print('Done')

    asyncio.run(main())


prompt()
