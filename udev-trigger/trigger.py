#!/usr/bin/env python3
import os
import json
data={}
data["CLIENT"]="udev-trigger"
data["ENV"]=os.environ.copy()

if os.path.exists("/run/ppm"):
    with open("/run/ppm", "w") as f:
        f.write(json.dumps(data))
