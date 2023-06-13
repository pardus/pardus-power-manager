#!/usr/bin/env python3
from util import *
from service import main
from backends.power import set_mode
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
while True:
    try:
        listen(main)
    except Exception as e:
        log(traceback.format_exc())
