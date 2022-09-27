import re


def scanner(code):
    regex = re.compile("@defineExpose\((.+)\)\ndef (.+):", re.S)
    IOStr = re.search(regex, code).group(1)
    SignStr = re.search(regex, code).group(2)
    args = re.search(re.compile(
        "input=\[(.+)\]", re.S), IOStr).group(1).split(',')
    args = list(map(lambda s: s.strip(), args))
    ret = re.search(re.compile("output=(.+)", re.S), IOStr).group(1)
    funcName = re.search(re.compile("(.+)\(.+\)", re.S), SignStr).group(1)
    return funcName, args, ret


def mapAppend(m, key, val):
    if key in m:
        m.append(val)
    else:
        m[key] = [val]
