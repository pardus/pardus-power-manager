#!/usr/bin/env python3
import gi
import os
gi.require_version('Gtk', '3.0')

from gi.repository import GLib, Gtk
from util import get

class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../data/MainWindow.ui")
        self.window = self.builder.get_object("ui_window_main")
        self.connect_signals()

    def connect_signals(self):
        self.window.connect("destroy",Gtk.main_quit)

if __name__ == "__main__":
    main = MainWindow()
    main.window.show()
    Gtk.main()
