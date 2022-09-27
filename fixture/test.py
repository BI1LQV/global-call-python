from gbcall import defineExpose


@defineExpose(input=[str, int], output=str)
def p(a, b):
    return a+b
