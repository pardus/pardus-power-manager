#!/usr/bin/env python3
import gi, os, sys, subprocess
gi.require_version('Gtk', '3.0')

from gi.repository import GLib, Gtk
sys.path.insert(0, os.path.dirname( os.path.realpath(__file__) )+"/../common")
from common import *

class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../data/MainWindow.ui")
        self.window = self.builder.get_object("ui_window_main")
        self.connect_signals()

    def connect_signals(self):
        self.window.connect("destroy",Gtk.main_quit)

if __name__ == "__main__":
    if os.getuid() != 0:
        subprocess.run(["pkexec", "/usr/share/pardus/power-manager/settings/main.py"])
        exit(0)
    main = MainWindow()
    main.window.show()
    Gtk.main()
