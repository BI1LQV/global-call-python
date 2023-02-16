from . import types
import re
import io, base64

def __number(maybeNumber):
  return float(maybeNumber)

def __text(maybeText):
  return str(maybeText)

def __boolean(maybeBoolean):
  return bool(maybeBoolean)

def __null(maybeNull):
  return None

def __plot(maybePlot):
  import mpld3
  return  mpld3.fig_to_dict(maybePlot)

def __complex(val):
  return val

def __img(maybePlot):
  import matplotlib.pyplot as plt
  buf = io.BytesIO()
  if hasattr(maybePlot,"__dpi"):
    maybePlot.savefig(buf, format='png',dpi=maybePlot.__dpi)
  else:
    maybePlot.savefig(buf, format='png')
  plt.close(maybePlot)
  buf.seek(0)
  img_str = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('UTF-8')
  return img_str

typeConverter={
  "Number":__number,
  "Text":__text,
  "Boolean":__boolean,
  "Null":__null,
  "Plot":__plot,
  "Complex":__complex,
  "Img":__img
}

def convertParameters(types,parameters):
  if len(types)==1 and not isinstance(parameters,list):
    parameters=[parameters]
  try:
    return list(map(lambda type,val:typeConverter[type](val),types,parameters))
  except Exception:
    raise Exception("unknown type")

allTypes=list(filter(lambda name:not name.startswith("__"),dir(types)))

def typeNameConvert(typeName):
    for type in allTypes:
        if re.compile(f".*{type}$").match(typeName):
            return type
    print(typeName)
    raise Exception("unknown type")