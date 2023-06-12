#!/usr/bin/env python3
import sys, os
import json

def usage():
    print(sys.argv)
    print("Usage: ppm [set/get] [mode/backlight] (value)")
    exit(1)

if len(sys.argv) <= 2:
    usage()

data = {}
data["pid"] = os.getpid()
if sys.argv[1] == "set":
    if len(sys.argv) <= 3:
        usage()
    if sys.argv[2] == "mode":
        data["new-mode"] = sys.argv[3]
    if sys.argv[2] == "backlight":
        data["new-backlight"] = {}
        for d in sys.argv[3:]:
            name = d.split("=")[0]
            value = d.split("=")[1]
            data["new-backlight"][name] = value
    with open("/run/ppm","w") as f:
        print(data)
        f.write(json.dumps(data))
elif sys.argv[1] == "get":
    ppm = "/run/user/{}/ppm".format(os.getuid())
    if not os.path.exists(ppm):
        os.mkdir(ppm)
    ppm = ppm+"/"+str(os.getpid())
    if not os.path.exists(ppm):
        os.mkfifo(ppm)
    # update request
    with open("/run/ppm","w") as f:
        f.write(json.dumps(data))
    # read from service
    data = ""
    with open(ppm,"r") as f:
        data = f.read()
    data = json.loads(data)
    if sys.argv[2] == "mode":
        print(data["current-mode"])
    elif sys.argv[2] == "backlight":
        for d in data["current-backlight"].keys():
            print("{} = {}".format(d, data["current-backlight"][d]))
else:
    usage()
