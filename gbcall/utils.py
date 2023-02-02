import re
from colorama import Fore, Style
from . import types

import importlib.util
import sys

def scanner(code):
    regex = re.compile("@defineExpose\((.+)\)\ndef (.+):", re.S)
    IOStr = re.search(regex, code).group(1)
    SignStr = re.search(regex, code).group(2)
    args = re.search(re.compile(
        "input=\[(.*?)\]", re.S), IOStr).group(1).split(',')
    args = list(map(lambda s: s.strip(), args))
    args = list(filter(lambda s: s != '', args))
    ret = re.search(re.compile("output=\[(.*?)\]", re.S), IOStr).group(1).split(',')
    ret = list(map(lambda s: s.strip(), ret))
    ret = list(filter(lambda s: s != '', ret))
    funcName = re.search(re.compile("(.+?)\(.+?\)", re.S), SignStr).group(1)
    return funcName, args, ret


def mapAppend(m, key, val):
    if key in m:
        m.append(val)
    else:
        m[key] = [val]


def printError(txt):
    print(f"{Fore.RED}ERROR:{Style.RESET_ALL} {txt}")

def dynamicImport(path):
    spec = importlib.util.spec_from_file_location(
        path, path)
    foo = importlib.util.module_from_spec(spec)
    sys.modules[path] = foo
    spec.loader.exec_module(foo)
    return foo


allTypes=list(filter(lambda name:not name.startswith("__"),dir(types)))

def typeNameConvert(typeName):
    for type in allTypes:
        if re.compile(f".*{type}$").match(typeName):
            return type
    print(typeName)
    raise Exception("unknown type")