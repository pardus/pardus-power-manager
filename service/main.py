#!/usr/bin/env python3
from util import *
from service import main
from backends.power import set_mode
from backends.gpu import disable_3d_controller
import time
import os
import json

if not get("enabled",True,"service") or os.path.exists("/run/ppm"):
    exit(0)

import traceback
singleinstance()

log_begin()
log("Starting Pardus Power Manager Service")

if os.fork():
    interval = int(get("update-interval",60))
    while True:
        time.sleep(interval)
        data = {}
        data["pid"] = os.getpid()
        data["update"] = "service"
        writefile("/run/ppm",json.dumps(data))

# set initial mode state
mode = get("ac-mode","performance","modes")
if not get_ac_online():
    mode = get("bat-mode","powersave","modes")
set_mode(mode)

if get("disable-3d-controller",False):
    disable_3d_controller()

while True:
    try:
        listen(main)
    except Exception as e:
        log(traceback.format_exc())
