def fint(ctx):
    ret = ""
    for c in ctx:
        if c in "0123456789":
            ret += c
    return int(ret)