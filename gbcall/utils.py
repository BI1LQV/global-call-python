import re
from aiohttp import web
import json

def scanner(code):
    regex = re.compile("@defineExpose\((.+)\)\ndef (.+):", re.S)
    IOStr = re.search(regex, code).group(1)
    SignStr = re.search(regex, code).group(2)
    args = re.search(re.compile(
        "input=\[(.+?)\]", re.S), IOStr).group(1).split(',')
    args = list(map(lambda s: s.strip(), args))
    ret = re.search(re.compile("output=\[(.+?)\]", re.S), IOStr).group(1).split(',')
    ret = list(map(lambda s: s.strip(), ret))
    funcName = re.search(re.compile("(.+?)\(.+?\)", re.S), SignStr).group(1)
    return funcName, args, ret


def mapAppend(m, key, val):
    if key in m:
        m.append(val)
    else:
        m[key] = [val]

def returnJson(data,error=None):
    if error:
        res={"res":error,"status":"ERR"}
    else:
        res={"res":data,"status":"OK"}
    return web.Response(
        text=json.dumps(res),
        content_type="application/json",
        headers={"Access-Control-Allow-Origin":"*"}
    )
