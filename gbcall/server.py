from aiohttp import web
if __name__=="__main__":
    from gbcall.settings import DEFAULT_PORT
    from gbcall import handler
else:
    from .settings import DEFAULT_PORT
    from . import handler

from colorama import Fore,Style

@web.middleware
async def responseJsonWrapper(request,handler):
    try:
        return web.json_response(
            {"res":await handler(request),"status":"OK"},
            headers={"Access-Control-Allow-Origin":"*"}
        )
    except Exception as e:
        if __name__!="__main__":
            raise e
        return web.json_response(
            {"res":str(e),"status":"ERR"},
            headers={"Access-Control-Allow-Origin":"*"}
        )

def run():
    app = web.Application(middlewares=[responseJsonWrapper])
    app.add_routes([
        web.get('/isAlive',handler.handshake),
        web.get('/funcRegister', handler.funcRegister),
        web.post('/call/{funcName}', handler.callFunc),
        web.get('/info/{funcName}', handler.getFuncInfo),
    ])
    print(f"python_server on: {Fore.RED}http://localhost:{DEFAULT_PORT}{Style.RESET_ALL}")
    web.run_app(app, port=DEFAULT_PORT, print=None)

if __name__=="__main__":
    run()