#!/usr/bin/env python3
from util import *
from indicator import *

import os, sys

if not os.path.exists("/run/ppm"):
    print("Failed to connect ppm service")
    exit(127)

client_dir = "/run/user/{}/ppm/".format(os.getuid())
if os.path.exists(client_dir):
    data = {}
    data["pid"] = os.getpid()
    data["show"] = "1"
    no_show = False
    for fifo in listdir(client_dir):
        if os.path.exists("/proc/{}".format(fifo)):
            writefile(client_dir + fifo, json.dumps(data))
            no_show = True
        else:
            os.unlink(client_dir + fifo)

main = Indicator()
listen(main)
Gtk.main()
