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

        self.status = Gtk.MenuItem()
        self.status.set_label("")
        self.menu.append(self.status)
        self.status.set_sensitive(False)

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
        self.set_status(self.data_to_msg(data))
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
            elif int(usage) < 0:
                ret += "Charge = {}W\n".format(int((-1*usage)/1000))
        ret += "\n"
        for d in data["backlight"].keys():
            max = data["backlight"][d]["max"]
            cur = data["backlight"][d]["current"]
            percent = cur * 100 / max
            ret += "[Backlight:{}]\n".format(d)
            ret += "Level = {}%\n".format(int(percent))
        return ret[:-1]


    def set_status(self, message):
        if message.strip() == "":
            self.status.hide()
        else:
            self.status.show()
        self.status.set_label(message.strip())

    def send_notification(self,msg):
        notification = Notify.Notification.new(msg)
        notification.show()


    @asynchronous
    def open_window_event(self, widget):
        subprocess.run(["pkexec", "/usr/share/pardus/power-manager/settings/main.py"])

    def quit_event(self, widget):
        os.unlink("/run/user/{}/ppm/{}".format(os.getuid(),os.getpid()))
        Gtk.main_quit()


