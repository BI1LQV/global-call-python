from gbcall import defineExpose, types,VirtualFile


@defineExpose(
    input=[types.Text],
    output=[types.File]
)
def genFile(name):
    file=VirtualFile()
    open(file.name,"w").write(name)

    return file
