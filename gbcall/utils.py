from colorama import Fore, Style


import importlib.util
import sys

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
