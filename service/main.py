#!/usr/bin/env python3
from util import *
from service import main
from backends.battery import battery_init
from gi.repository import GLib
if os.fork():
    battery_init()
while True:
    try:
        listen(main)
    except Exception as e:
        log(str(e))
