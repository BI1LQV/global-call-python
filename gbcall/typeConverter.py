import mpld3
import re
def __number(maybeNumber):
  return float(maybeNumber)

def __text(maybeText):
  return str(maybeText)

def __boolean(maybeBoolean):
  return bool(maybeBoolean)

def __null(maybeNull):
  return None

def __plot(maybePlot):
  return mpld3.fig_to_html(maybePlot)

def typeConvert(maybeType,val):
  if re.compile(".*Number$").match(maybeType):
    return __number(val)
  elif re.compile(".*Text$").match(maybeType):
    return __text(val)
  elif re.compile(".*Boolean$").match(maybeType):
    return __boolean(val)
  elif re.compile(".*Null$").match(maybeType):
    return __null(val)
  elif re.compile(".*Plot$").match(maybeType):
    return __plot(val)
  elif re.compile(".*Complex$").match(maybeType):
    return val
  else:
    raise Exception("unknown type")

def convertParameters(types,parameters):
  return list(map(lambda type,val:typeConvert(type,val),types,parameters))