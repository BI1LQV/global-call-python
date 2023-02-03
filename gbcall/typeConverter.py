import mpld3
def __number(maybeNumber):
  return float(maybeNumber)

def __text(maybeText):
  return str(maybeText)

def __boolean(maybeBoolean):
  return bool(maybeBoolean)

def __null(maybeNull):
  return None

def __plot(maybePlot):
  return  mpld3.fig_to_dict(maybePlot)

def __complex(val):
  return val

typeConverter={
  "Number":__number,
  "Text":__text,
  "Boolean":__boolean,
  "Null":__null,
  "Plot":__plot,
  "Complex":__complex
}

def convertParameters(types,parameters):
  if len(types)==1 and not isinstance(parameters,list):
    parameters=[parameters]
  try:
    return list(map(lambda type,val:typeConverter[type](val),types,parameters))
  except Exception:
    raise Exception("unknown type")