from gbcall import defineExpose


@defineExpose(input=[str, int], output=str)
def paa(a, b):
    return a+b
