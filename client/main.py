#!/usr/bin/env python3
from util import *
from MainWindow import *

if not os.path.exists("/run/ppm"):
    print("Failed to connect ppm service")
    exit(127)

main = MainWindow()

listen(main)
Gtk.main()
