import re
from .typeConverter import typeNameConvert

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

    return funcName, list(map(typeNameConvert,args)), list(map(typeNameConvert,ret))
