#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 00:03:13 2024

@author: fatih
"""

import subprocess
import sys


def main():
    def add_to_group(user, group):
        subprocess.call(["adduser", user, group])

    if len(sys.argv) > 1:
        add_to_group(sys.argv[1], sys.argv[2])
    else:
        print("no argument passed")


if __name__ == "__main__":
    main()
