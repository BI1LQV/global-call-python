from .utils import typeNameConvert
from .typeConverter import convertParameters
def defineExpose(input, output):
    def decorator(func):
        def wrapper(*args):
            inBrowser=False
            try:
                __file__
            except:
                inBrowser=True
            if inBrowser:
                inputTypes=list(map(typeNameConvert,input))
                outputTypes=list(map(typeNameConvert,output))
                return convertParameters(outputTypes,func(*convertParameters(inputTypes,args)))
            return func(*args)
        return wrapper
    return decorator
