#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 00:03:13 2024

@author: fatih
"""

import os
import sys


def main():
    def set_brightness(device, value):
        brightness_file = "/sys/class/backlight/{}/brightness".format(device)
        if os.path.isfile(brightness_file):
            fd = open("/sys/class/backlight/{}/brightness".format(device), "w")
            fd.write("{}".format(int(value)))
            fd.flush()
            fd.close()

    if len(sys.argv) > 1:
        set_brightness(sys.argv[1], sys.argv[2])
    else:
        print("no argument passed")


if __name__ == "__main__":
    main()
