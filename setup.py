#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:53:01 2024

@author: fatihaltun
"""

import os
import subprocess

from setuptools import setup, find_packages


def create_mo_files():
    podir = "po"
    mo = []
    for po in os.listdir(podir):
        if po.endswith(".po"):
            os.makedirs("{}/{}/LC_MESSAGES".format(podir, po.split(".po")[0]), exist_ok=True)
            mo_file = "{}/{}/LC_MESSAGES/{}".format(podir, po.split(".po")[0], "pardus-power-manager.mo")
            msgfmt_cmd = 'msgfmt {} -o {}'.format(podir + "/" + po, mo_file)
            subprocess.call(msgfmt_cmd, shell=True)
            mo.append(("/usr/share/locale/" + po.split(".po")[0] + "/LC_MESSAGES",
                       ["po/" + po.split(".po")[0] + "/LC_MESSAGES/pardus-power-manager.mo"]))
    return mo


changelog = "debian/changelog"
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = "0.0.0"
    f = open("src/__version__", "w")
    f.write(version)
    f.close()

data_files = [
                 ("/usr/bin", ["pardus-power-manager"]),
                 ("/usr/share/applications",
                  ["data/tr.org.pardus.power-manager.desktop"]),
                 ("/usr/share/pardus/pardus-power-manager/ui",
                  ["ui/MainWindow.glade"]),
                 ("/usr/share/pardus/pardus-power-manager/src",
                  ["src/Main.py",
                   "src/MainWindow.py",
                   "src/Brightness.py",
                   "src/Notification.py",
                   "src/UserSettings.py",
                   "src/Utils.py",
                   "src/__version__"]),
                 ("/usr/share/pardus/pardus-power-manager/data",
                  ["data/style.css",
                   "data/tr.org.pardus.power-manager.desktop",
                   "data/tr.org.pardus.power-manager-autostart.desktop"]),
                 ("/usr/share/polkit-1/actions",
                  ["data/tr.org.pardus.pkexec.pardus-power-manager.policy"]),
                 ("/lib/udev",
                  ["data/ppm-bright-helper"]),
                 ("/lib/udev/rules.d",
                  ["data/90-ppm-brightness.rules"]),
                 ("/etc/xdg/autostart",
                  ["data/tr.org.pardus.power-manager-autostart.desktop"]),
                 ("/usr/share/icons/hicolor/scalable/apps/",
                  ["data/pardus-power-manager.svg",
                   "data/pardus-power-manager-power-saver.svg",
                   "data/pardus-power-manager-balanced.svg",
                   "data/pardus-power-manager-performance.svg",
                   "data/pardus-power-manager-power-saver-symbolic.svg",
                   "data/pardus-power-manager-balanced-symbolic.svg",
                   "data/pardus-power-manager-performance-symbolic.svg",
                   ])
             ] + create_mo_files()

setup(
    name="pardus-power-manager",
    version=version,
    packages=find_packages(),
    scripts=["pardus-power-manager"],
    install_requires=["PyGObject"],
    data_files=data_files,
    author="Fatih Altun",
    author_email="fatih.altun@pardus.org.tr",
    description="Pardus Power Manager application.",
    license="GPLv3",
    keywords="pardus-power-manager",
    url="https://github.com/pardus/pardus-power-manager",
)
