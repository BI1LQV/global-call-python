import os
from aiohttp import web
from utils import scanner
# from utils import mapAppend
from settings import OK_STATUS
from settings import DEFAULT_PORT, ALIVE_SYMBOL
import importlib.util
import sys

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
    module = dynamicImport(absPath)
    with open(os.path.join(base, file), 'r') as source:
        funcName, input, output = scanner(source.read())
        funcCache[funcName] = getattr(module,funcName)
        infoCache[funcName] = {"input": input, "output": output}
    return web.Response(text=OK_STATUS)


# def infoRegister(request):
#     funcName = request.rel_url.query['funcName']
#     fileAbsPath = request.rel_url.query['fileAbsPath']
#     input = request.rel_url.query['input']
#     output = request.rel_url.query['output']
#     mapAppend(bindingCache, fileAbsPath, {
#         "funcName": funcName,
#         "input": json.loads(input),
#         "output": json.loads(output)
#     })

#     return web.Response(text=OK_STATUS)

async def callFunc(request):
    data=await request.json()
    res=funcCache[data["funcName"]](*data["args"])
    return web.Response(text=str(res))


def getFuncInfo(request):
    name = request.match_info.get('name')
    return web.Response(text=name)


app = web.Application()
app.add_routes([
    web.get('/isAlive', handshake),
    web.get('/funcRegister', funcRegister),
    web.post('/call/{funcName}', callFunc),
    web.get('/info/{funcName}', getFuncInfo),
    # web.get('/infoRegister', infoRegister),
    web.get('/b/{name}', handle)
])

if __name__ == '__main__':
    print(f"python_server on: http://localhost:{DEFAULT_PORT}")
    web.run_app(app, port=DEFAULT_PORT, print=None)
