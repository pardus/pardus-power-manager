import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk
print(os.getpid())
from util import send_server
from indicator import Indicator

class MainWindow:
    def __init__(self):
        self.indicator = Indicator()
        self.init()
        send_server()

    def init(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../data/MainWindow.ui")
        self.window = self.builder.get_object("ui_window_main")
        self.indicator.set_window(self.window)
        self.connect_signals()
        self.update_lock = False
        

    def powersave_button_event(self,widget=None):
        if self.update_lock:
            return
        data = {}
        data["new-mode"] = "powersave"
        send_server(data)

    def performance_button_event(self,widget=None):
        if self.update_lock:
            return
        data = {}
        data["new-mode"] = "performance"
        send_server(data)


    def destroy_signal(self,widget=None):
        self.window.hide()
        self.init()


    def connect_signals(self):
        self.window.connect("destroy",self.destroy_signal)
        self.builder.get_object("ui_button_powersave").connect("clicked",self.powersave_button_event)
        self.builder.get_object("ui_button_performance").connect("clicked",self.performance_button_event)


    def update(self,data):
        print(data)
        self.update_lock = True
        if "show" in data:
            self.window.show()
        if "mode" in data:
            cur_mode = data["mode"]
            self.builder.get_object("ui_button_performance").set_active(cur_mode == "performance")
            self.builder.get_object("ui_button_powersave").set_active(cur_mode == "powersave")
        self.update_lock = False
