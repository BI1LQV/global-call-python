from aiohttp import web
from .settings import DEFAULT_PORT
from . import handler

from colorama import Fore

app = web.Application()
app.add_routes([
    web.get('/isAlive',handler.handshake),
    web.get('/funcRegister', handler.funcRegister),
    web.post('/call/{funcName}', handler.callFunc),
    web.get('/info/{funcName}', handler.getFuncInfo),
])

def run():
    print(f"python_server on: {Fore.RED}http://localhost:{DEFAULT_PORT}")
    web.run_app(app, port=DEFAULT_PORT, print=None)

if __name__=="__main__":
    run()