from .typeConverter import convertParameters

def callWithTypeCheck(func,inputTypes,outputTypes,args):
  return convertParameters(outputTypes,func(*convertParameters(inputTypes,args)))
