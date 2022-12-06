from gbcall import defineExpose


@defineExpose(input=[int, int], output=int)
def add(a, b):
    return a+b
