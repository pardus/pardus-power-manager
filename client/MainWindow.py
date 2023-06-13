import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk
print(os.getpid())
from util import send_server

class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../data/MainWindow.ui")
        self.window = self.builder.get_object("ui_window_main")
        self.window.show_all()
        self.connect_signals()
        self.update_lock = False
        send_server()

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
        os.unlink("/run/user/{}/ppm/{}".format(os.getuid(),os.getpid()))
        Gtk.main_quit()


    def connect_signals(self):
        self.window.connect("destroy",self.destroy_signal)
        self.builder.get_object("ui_button_powersave").connect("clicked",self.powersave_button_event)
        self.builder.get_object("ui_button_performance").connect("clicked",self.performance_button_event)


    def update(self,data):
        print(data)
        self.update_lock = True
        if "mode" in data:
            cur_mode = data["mode"]
            self.builder.get_object("ui_button_performance").set_active(cur_mode == "performance")
            self.builder.get_object("ui_button_powersave").set_active(cur_mode == "powersave")
        self.update_lock = False
