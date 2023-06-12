#!/usr/bin/env python3
from util import *
from service import main
from backends.battery import battery_init, battery_main
from gi.repository import GLib


if not get("enabled",True,"service"):
    exit(0)

import traceback
singleinstance()

# set initial mode state
mode = get("ac-mode","performance","modes")
if not get_ac_online():
    mode = get("bat-mode","powersave","modes")
set_mode(mode)

if os.fork():
    if not get("battery-events",True,"service"):
        exit(0)
    battery_init()
    while True:
        battery_main()
        time.sleep(int(get("battery-check-interval",60,"service")))
else:
    while True:
        try:
            listen(main)
        except Exception as e:
            log(traceback.format_exc())
