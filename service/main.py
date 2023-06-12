#!/usr/bin/env python3
from util import *
from service import main
from backends.battery import battery_init, battery_main
from gi.repository import GLib

import traceback

if not get("enabled",True,"service"):
    exit(0)
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
