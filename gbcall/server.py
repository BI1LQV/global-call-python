import os
from aiohttp import web
from utils import scanner,returnJson
# from utils import mapAppend
# from settings import OK_STATUS
from settings import DEFAULT_PORT, ALIVE_SYMBOL
import importlib.util
import sys
import json
from colorama import Fore

infoCache = {}
moduleCache = {}
funcCache = {}
# bindingCache = {}


def dynamicImport(path):
    spec = importlib.util.spec_from_file_location(
        path, path)
    foo = importlib.util.module_from_spec(spec)
    sys.modules[path] = foo
    spec.loader.exec_module(foo)
    return foo


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def handshake(_request):
    return web.Response(text=ALIVE_SYMBOL["python"])


async def funcRegister(request):
    file = request.rel_url.query['filePath']
    base = request.rel_url.query['workingPath']

    absPath = os.path.join(base, file)
    try:
        module = dynamicImport(absPath)
    except:
        return returnJson(None,"no file or error in file")
    with open(os.path.join(base, file), 'r') as source:
        funcName, input, output = scanner(source.read())
        funcCache[funcName] = getattr(module,funcName)
        infoCache[funcName] = {"input": input, "output": output}
    return returnJson(funcName)



async def callFunc(request):
    data=await request.json()
    funcName = request.match_info.get('funcName', "Anonymous")
    res=funcCache[funcName](*data["args"])
    return returnJson(res)


def getFuncInfo(request):
    name = request.match_info.get('funcName')
    try:
        return returnJson(infoCache[name])
    except:
        return returnJson(None,"no such func")


app = web.Application()
app.add_routes([
    web.get('/isAlive', handshake),
    web.get('/funcRegister', funcRegister),
    web.post('/call/{funcName}', callFunc),
    web.get('/info/{funcName}', getFuncInfo),
    web.get('/b/{name}', handle)
])


print(f"python_server on: {Fore.RED}http://localhost:{DEFAULT_PORT}")
web.run_app(app, port=DEFAULT_PORT, print=None)
