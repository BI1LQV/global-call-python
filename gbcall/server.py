import os
from aiohttp import web
from settings import DEFAULT_PORT

from settings import ALIVE_SYMBOL


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def handshake(_request):
    return web.Response(text=ALIVE_SYMBOL["python"])


async def register(request):
    file = request.rel_url.query['filePath']
    base = request.rel_url.query['workingPath']
    with open(os.path.join(base, file), 'r') as source:
        return web.Response(text=source.read())


app = web.Application()
app.add_routes([
    web.get('/isAlive', handshake),
    web.get('/register', register),
    web.get('/b/{name}', handle)
])

if __name__ == '__main__':
    print(f"python_server on: http://localhost:{DEFAULT_PORT}")
    web.run_app(app, port=DEFAULT_PORT, print=None)
