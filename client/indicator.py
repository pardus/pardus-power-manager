import gi, os
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as appindicator
except:
    # fall back to Ayatana
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as appindicator

class Indicator:

    def __init__(self):
        self.indicator = appindicator.Indicator.new(
            "appindicator", "system-upgrade", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

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

        self.quit = Gtk.MenuItem()
        self.quit.set_label("Exit")
        self.quit.connect('activate', self.quit_event)
        self.menu.append(self.quit)
        
        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    def menu_popup_event(self):
        print("aaaa")

    def set_window(self, window):
        self.window = window

    def set_status(self, message):
        self.status.set_label(message)

    def open_window_event(self, widget):
        self.window.show()

    def quit_event(self, widget):
        os.unlink("/run/user/{}/ppm/{}".format(os.getuid(),os.getpid()))
        Gtk.main_quit()


