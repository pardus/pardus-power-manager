#!/usr/bin/env python3
import sys, os
import json

def usage():
    print(sys.argv)
    print("Usage: ppm [set/get] [mode/backlight] (value)")
    exit(1)

if len(sys.argv) <= 2:
    usage()

if not os.path.exists("/run/ppm"):
    print("Failed to connect ppm service")
    exit(127)

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
            if "=" in d:
                name = d.split("=")[0]
                value = d.split("=")[1]
                data["new-backlight"][name] = value
    with open("/run/ppm","w") as f:
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
        print(data["mode"])
    elif sys.argv[2] == "backlight":
        for d in data["backlight"].keys():
            print("[{}]".format(d))
            print("max={}".format(data["backlight"][d]["max"]))
            print("current={}".format(data["backlight"][d]["current"]))
    elif sys.argv[2] == "battery":
        for d in data["battery"].keys():
            print("[{}]".format(d))
            print("level={}".format(data["battery"][d]["level"]))
            print("status={}".format(data["battery"][d]["status"]))
            print("health={}".format(data["battery"][d]["health"]))
            print("health={}".format(data["battery"][d]["power_usage"]))
else:
    usage()
