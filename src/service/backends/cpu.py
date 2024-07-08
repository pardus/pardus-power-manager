import os
from common import *
def list_cpu():
    ret = []
    for i in range(0, get_num_of_cpu()):
        ret.append("cpu"+str(i))
    return ret

def get_num_of_cpu():
    i = 0
    while os.path.exists("/sys/devices/system/cpu/cpu"+str(i)):
        i += 1
    return i

def list_little_cpu():
    max_all = 0
    ret = []
    for i in range(0, get_num_of_cpu()):
        with open("/sys/devices/system/cpu/cpu{}//cpufreq/scaling_max_freq".format(i), "r") as f:
            freq = int(f.read())
            if freq > max_all:
                max_all = freq
    for i in range(0, get_num_of_cpu()):
        with open("/sys/devices/system/cpu/cpu{}//cpufreq/scaling_max_freq".format(i), "r") as f:
            freq = int(f.read())
            if freq < max_all:
                ret.append("cpu"+str(i))
    return ret

def list_big_cpu():
    all_cpu = list_cpu()
    for cpu in list_little_cpu():
        all_cpu.remove(cpu)
    return all_cpu

def change_cpu_status(core, status):
    log("New core status: {} = {}".format(core, status))
    if not os.path.exists("/sys/devices/system/cpu/cpu"+str(core)+"/online"):
        return False
    f = open("/sys/devices/system/cpu/cpu"+str(core)+"/online", "w")
    if status:
        f.write("1")
    else:
        f.write("0")
    return True
