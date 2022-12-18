from gbcall import defineExpose
@defineExpose(input=[int, int, int], output=[int, int, int])
def rgb2hsv(r, g, b):
  r /= 255
  g /= 255
  b /= 255
  cMax = max(r, g, b)
  cMin = min(r, g, b)
  delta = cMax - cMin

  h = 60
  if delta == 0:
    h *= 0
  elif cMax == r:
    h *= (g - b) / delta
  elif cMax == g:
    h *= (b - r) / delta + 2
  elif  cMax == b:
    h *= (r - g) / delta + 4

  s = 0
  if cMax != 0:
    s = delta / cMax
  if h < 0:
    h += 360

  return h, s * 100, cMax * 100
