#!/usr/bin/env python3
import os
import json
from util import get_ac_online
data={}
data["pid"]="1"
data["ENV"]=os.environ.copy()

if os.path.exists("/run/ppm"):
    new_mode = "performance"
    if get_ac_online():
        new_mode = "powersave"
    data["new-mode"] = new_mode
    with open("/run/ppm", "w") as f:
        f.write(json.dumps(data))
        f.flush()
