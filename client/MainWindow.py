import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk
print(os.getpid())
from util import send_server

class MainWindow:
    def __init__(self):
        self.window = Gtk.Window()
        self.label = Gtk.Label()
        self.window.add(self.label)
        self.connect_signals()
        self.window.show_all()
        #data = {'main': {'name': 'test', 'num': 0}}
        #send_server(data)

    def connect_signals(self):
        self.window.connect("destroy",Gtk.main_quit)

    def update(self,data):
        self.label.set_label(str(data))
