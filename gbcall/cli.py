#! python3
import argparse
import os
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
import asyncio
from .settings import DEFAULT_PORT, DESCRIPTION, ALIVE_SYMBOL
import urllib.parse
from colorama import Fore, Style
import subprocess
import sys
from .utils import printError
from time import sleep

def prompt():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION)

    parser.add_argument("filePath",
                        nargs='*', metavar="file_Pame", type=str,
                        help="The file containing function to be exposed.")

    args = parser.parse_args()

    if not args.filePath:
        printError("No file path provided")
        return
    files = args.filePath

    targetServer = f'http://localhost:{DEFAULT_PORT}'

    async def main(reRun):
        async with ClientSession() as session:
            try:
                async with session.get(targetServer+'/isAlive') as resp:
                    if (resp.status == 200 and
                            (await resp.json()).get("res") == ALIVE_SYMBOL["python"]):
                        for fileName in files:
                            params = urllib.parse.urlencode({
                                "filePath": fileName,
                                "workingPath": os.getcwd()
                            })
                            async with session.get(
                                f'{targetServer}/funcRegister?{params}'
                            ) as resp:
                                funcName = await resp.json()
                                if funcName['status'] == "ERR":
                                    printError(funcName['res'])
                                else:
                                    print(f"{Fore.BLUE}{funcName['res']}{Style.RESET_ALL} registered on {Fore.RED}{targetServer}{Style.RESET_ALL}")
                    else:
                        printError("target server is not working properly or is not gbcall server")
            except ClientConnectorError:
                t=subprocess.Popen([sys.executable, os.path.split(os.path.realpath(__file__))[0]+'/server.py'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
                if not reRun:
                    sleep(0.5) #TODO: 改成读到启动再重试
                    await main(True)
                else:
                    printError("start server failed")


    asyncio.run(main(False))
