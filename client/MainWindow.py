import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk
print(os.getpid())
from util import send_server, get
from indicator import Indicator

class MainWindow:
    def __init__(self):
        self.indicator = Indicator()
        self.init()
        self.current_mode = "performance"
        send_server()

    def init(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../data/MainWindow.ui")
        self.window = self.builder.get_object("ui_window_main")
        self.indicator.set_client(self)
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
            self.current_mode = data["mode"]
            self.builder.get_object("ui_button_performance").set_active(self.current_mode == "performance")
            self.builder.get_object("ui_button_powersave").set_active(self.current_mode == "powersave")
            if self.current_mode == "powersave":
                self.indicator.power_mode.set_label("Disable Powersave")
            else:
                self.indicator.power_mode.set_label("Enable Powersave")
        self.indicator.set_status(self.data_to_msg(data))
        self.update_lock = False

    def data_to_msg(self, data):
        ret = ""
        for d in data["battery"].keys():
            real_name = data["battery"][d]["real_name"]
            level = data["battery"][d]["level"]
            health = data["battery"][d]["health"]
            usage = data["battery"][d]["power_usage"]
            ret += "[Battery:{}]\n".format(real_name)
            ret += "Level = {}%\n".format(int(level))
            ret += "Health = {}%\n".format(int(health))
            if int(usage) > 0:
                ret += "Usage = {}W\n".format(int(usage/1000))
        ret += "\n"
        for d in data["backlight"].keys():
            max = data["backlight"][d]["max"]
            cur = data["backlight"][d]["current"]
            percent = cur * 100 / max
            ret += "[Backlight:{}]\n".format(d)
            ret += "Level = {}%\n".format(int(percent))
        return ret[:-1]
