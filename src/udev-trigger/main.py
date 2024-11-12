#!/usr/bin/env python3
import os
import json
import sys
sys.path.insert(0, os.path.dirname( os.path.realpath(__file__) )+"/../common")
from common import *
data={}
data["pid"]="1"
data["ENV"]=os.environ.copy()

if os.path.exists("/run/ppm"):
    ac_now = get_ac_online()

    # get last status
    ac_last = ""
    if os.path.isfile("/run/ppm.last"):
        with open("/run/ppm.last","r") as f:
            ac_last = f.read()

    # write last status
    with open("/run/ppm.last","w") as f:
        f.write(str(ac_now))

    # ignore if last same with now
    if str(ac_now) == str(ac_last):
        exit(0)

    new_mode = get("ac-mode","balanced","modes")
    if not ac_now:
        new_mode = get("bat-mode","powersave","modes")

    data["new-mode"] = new_mode
    with open("/run/ppm", "w") as f:
        f.write(json.dumps(data))
        f.flush()
