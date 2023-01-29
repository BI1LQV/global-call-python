#! python3
import argparse
import os
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
import asyncio
from settings import DEFAULT_PORT, DESCRIPTION, ALIVE_SYMBOL, LOAD_ERROR
import urllib.parse
from colorama import Fore, Style
import subprocess
import sys


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

    async def main(reRun):
        if not reRun:
            return
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
                                if funcName == LOAD_ERROR:
                                    print(f"{Fore.RED}模块路径或模块内部错误")
                                    continue
                                print(f'{Fore.BLUE}{funcName}{Style.RESET_ALL} registered on {Fore.RED}{targetServer}{Style.RESET_ALL}')
            except ClientConnectorError:
                t=subprocess.Popen([sys.executable, os.path.split(os.path.realpath(__file__))[0]+'/server.py'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
                if not reRun:
                    asyncio.run(main(True))


    asyncio.run(main(True))


prompt()
