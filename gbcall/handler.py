import os
from aiohttp import web
from .utils import scanner,returnJson,dynamicImport
from .settings import ALIVE_SYMBOL
from .typeConverter import convertParameters

infoCache = {}
moduleCache = {}
funcCache = {}

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
    return returnJson(convertParameters(infoCache[funcName]["output"],res))


def getFuncInfo(request):
    name = request.match_info.get('funcName')
    try:
        return returnJson(infoCache[name])
    except:
        return returnJson(None,"no such func")