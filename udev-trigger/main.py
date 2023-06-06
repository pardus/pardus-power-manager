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
    new_mode = "performance"
    if not get_ac_online():
        new_mode = "powersave"
    data["new-mode"] = new_mode
    with open("/run/ppm", "w") as f:
        f.write(json.dumps(data))
        f.flush()
