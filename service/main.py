#!/usr/bin/env python3
from util import *
from service import main
from backends.power import set_mode
import time
import os
import json

from util import *

if is_virtual_machine():
    exit(0)

if not get("enabled",True,"service") or os.path.exists("/run/ppm"):
    exit(0)

import traceback
singleinstance()

log_begin()
log("Starting Pardus Power Manager Service")

if os.fork():
    interval = int(get("update-interval",60, "service"))
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

while True:
    try:
        listen(main)
    except Exception as e:
        log(traceback.format_exc())
