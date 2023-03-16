from gbcall import defineExpose,types
@defineExpose(
  input=[types.Number,types.Number],
  output=[types.Number]
)
def adder(a,b):
    return a+b