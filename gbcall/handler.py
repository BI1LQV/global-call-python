import os

from .callWithTypeCheck import callWithTypeCheck
from .utils import dynamicImport
from .settings import ALIVE_SYMBOL
from .scanner import scanner

infoCache = {}
moduleCache = {}
funcCache = {}

async def handshake(_request):
    return ALIVE_SYMBOL["python"]


async def funcRegister(request):
    file = request.rel_url.query['filePath']
    base = request.rel_url.query['workingPath']

    absPath = os.path.join(base, file)
    try:
        module = dynamicImport(absPath)
    except:
        raise Exception("no file or error in file")
    with open(os.path.join(base, file), 'r') as source:
        funcName, input, output = scanner(source.read())
        funcCache[funcName] = getattr(module,funcName)
        infoCache[funcName] = {
            "input": input,
            "output": output
        }
    return funcName


async def callFunc(request):
    data=await request.json()
    funcName = request.match_info.get('funcName', "Anonymous")
    return callWithTypeCheck(funcCache[funcName],
                             infoCache[funcName]["input"],
                             infoCache[funcName]["output"],
                             data["args"])


async def getFuncInfo(request):
    name = request.match_info.get('funcName')
    try:
        return infoCache[name]
    except:
        raise Exception("no such function")