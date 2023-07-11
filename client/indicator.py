import gi, os, time, subprocess
gi.require_version("Gtk","3.0")
gi.require_version("Notify", "0.7")

from gi.repository import Gtk
from gi.repository import Notify

from util import send_server
from common import *

class Indicator:

    def __init__(self):
        self.indicator = Gtk.StatusIcon()
        self.indicator.connect("activate", self.open_window_event)
        self.indicator.connect("popup-menu", self.menu_popup_event)
        self.indicator.set_from_icon_name("pardus-pm")

        Notify.init("Pardus Power Manager")

        self.menu = Gtk.Menu()
        self.current_mode = None
        
        self.menu.connect("popped-up",self.menu_popup_event)

        self.open_window = Gtk.MenuItem()
        self.open_window.set_label("Settings")
        self.open_window.connect('activate', self.open_window_event)
        self.menu.append(self.open_window)

        self.power_mode = Gtk.MenuItem()
        self.power_mode.set_label("Disable Powersave")
        self.power_mode.connect('activate', self.power_mode_event)
        self.menu.append(self.power_mode)

        self.quit = Gtk.MenuItem()
        self.quit.set_label("Exit")
        self.quit.connect('activate', self.quit_event)
        self.menu.append(self.quit)

        self.menu.show_all()

    def power_mode_event(self, widget):
        data = {}
        if self.current_mode == "performance":
            data["new-mode"] = "powersave"
        else:
            data["new-mode"] = "performance"
        send_server(data)

    def menu_popup_event(self, icon = None, button = 3, time = 0):
        data = {}
        data["update"] = "indicator"
        send_server(data)
        self.menu.popup(None, None, None, self.indicator, button, time)

    def update(self,data):
        print(data)
        self.update_lock = True
        if "mode" in data:
            if self.current_mode != data["mode"]:
                if self.current_mode != None:
                    self.send_notification("Power profile changed: " + data["mode"])
                self.current_mode = data["mode"]
                if self.current_mode == "powersave":
                    self.power_mode.set_label("Disable Powersave")
                else:
                    self.power_mode.set_label("Enable Powersave")
        if "show" in data:
            self.open_window_event(None)
        self.update_lock = False

    def send_notification(self,msg):
        notification = Notify.Notification.new(msg)
        notification.show()


    @asynchronous
    def open_window_event(self, widget):
        subprocess.run(["pkexec", "/usr/share/pardus/power-manager/settings/main.py"])

    def quit_event(self, widget):
        os.unlink("/run/user/{}/ppm/{}".format(os.getuid(),os.getpid()))
        Gtk.main_quit()


