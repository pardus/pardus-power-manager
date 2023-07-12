#!/usr/bin/env python3
from util import *
from indicator import *

import os, sys

if not os.path.exists("/run/ppm"):
    if "--autostart" in sys.argv:
        print("Failed to connect ppm service")
        exit(127)
    else:
        subprocess.run(["pkexec", "/usr/share/pardus/power-manager/settings/main.py"])
        exit(0)

client_dir = "/run/user/{}/ppm/".format(os.getuid())
no_show = False
if os.path.exists(client_dir):
    data = {}
    data["pid"] = os.getpid()
    data["show"] = "1"
    for fifo in listdir(client_dir):
        if os.path.exists("/proc/{}".format(fifo)):
            writefile(client_dir + fifo, json.dumps(data))
            no_show = True
        else:
            os.unlink(client_dir + fifo)

if no_show:
    exit(0)
main = Indicator()
listen(main)
Gtk.main()
