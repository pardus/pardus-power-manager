import gi, os, time
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from util import send_server

class Indicator:

    def __init__(self):
        self.indicator = Gtk.StatusIcon()
        self.indicator.connect("activate", self.open_window_event)
        self.indicator.connect("popup-menu", self.menu_popup_event)


        self.menu = Gtk.Menu()
        
        self.menu.connect("popped-up",self.menu_popup_event)

        self.status = Gtk.MenuItem()
        self.status.set_label("")
        self.menu.append(self.status)
        self.status.set_sensitive(False)

        self.open_window = Gtk.MenuItem()
        self.open_window.set_label("Open")
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
        if self.client.current_mode == "performance":
            self.client.powersave_button_event(widget)
        else:
            self.client.performance_button_event(widget)

    def menu_popup_event(self, icon = None, button = 3, time = 0):
        data = {}
        data["update"] = "indicator"
        send_server(data)
        self.menu.popup(None, None, None, self.indicator, button, time)


    def set_client(self, client):
        self.client = client

    def set_status(self, message):
        self.status.set_label(message)

    def open_window_event(self, widget):
        self.client.window.show()

    def quit_event(self, widget):
        os.unlink("/run/user/{}/ppm/{}".format(os.getuid(),os.getpid()))
        Gtk.main_quit()


