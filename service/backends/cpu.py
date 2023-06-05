import os
def list_cpu():
    i = 0
    ret = []
    while os.path.exists("/sys/devices/system/cpu/cpu"+str(i)):
        i += 1
        ret.append("cpu"+str(i))
    return ret

def change_cpu_status(core, status):
    if not os.path.exists("/sys/devices/system/cpu/cpu"+str(core)+"/online"):
        return False
    f = open("/sys/devices/system/cpu/cpu"+str(core)+"/online", "w")
    if status:
        f.write("1")
    else:
        f.write("0")
    return True
