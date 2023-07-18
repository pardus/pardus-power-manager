#!/usr/bin/env python3
import sys, os, json
sys.path.insert(0, os.path.dirname( os.path.realpath(__file__) )+"/../common")
from common import *
os.environ["PATH"]="/bin:/sbin:/usr/bin:/usr/sbin"
def write_settings(data):
    ctx = ""
    for section in data:
        ctx += "[" + section + "]\n"
        for var in data[section]:
            ctx += str(var) + "=" + str(data[section][var]) +"\n"
        ctx += "\n"
    writefile("/etc/pardus/ppm.conf.d/99-ppm-settings.conf",ctx)


print(sys.argv)
if len(sys.argv) == 1:
    exit(1)
if sys.argv[1] == "stop_service":
    service_stop()
elif sys.argv[1] == "start_service":
    service_start()
elif sys.argv[1] == "save":
    data = readfile(sys.argv[2])
    data = json.loads(data)
    write_settings(data)
