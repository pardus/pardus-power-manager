import gi, os, time, subprocess
gi.require_version("Gtk","3.0")
gi.require_version("Notify", "0.7")

from gi.repository import Gtk
from gi.repository import Notify

import json

try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as appindicator
except:
    # fall back to Ayatana
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as appindicator

from util import send_server
from common import *

try:
    import locale
    from locale import gettext as _

    # Translation Constants:
    APPNAME = "pardus-power-manager"
    TRANSLATIONS_PATH = "/usr/share/locale"
    locale.bindtextdomain(APPNAME, TRANSLATIONS_PATH)
    locale.textdomain(APPNAME)
except:
    # locale load issue fix
    def _(msg):
        return msg
actions_file = os.path.dirname(os.path.abspath(__file__)) + "/actions.py"

# string for translation
_("powersave")
_("performance")

class MainWindow:

    def __init__(self):
        self.__is_init = False
        self.__window_status = False
        self.open_window = Gtk.MenuItem()
        self.power_mode = Gtk.MenuItem()
        self.quit = Gtk.MenuItem()
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../data/MainWindow.ui")
        self.window = self.builder.get_object("ui_window_main")
        data = {}
        data["update"]="client"
        send_server(data)

    def init(self):
        if self.__is_init:
            return
        self.indicator = appindicator.Indicator.new(
            "pardus-power-manager", "pardus-pm-performance-symbolic", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        Notify.init("Pardus Power Manager")

        self.menu = Gtk.Menu()
        self.current_mode = None

        if not self.__window_status:
             self.open_window.set_label(_("Show"))
        else:
             self.open_window.set_label(_("Hide"))
        self.open_window.connect('activate', self.open_window_event)
        self.menu.append(self.open_window)

        self.power_mode.connect('activate', self.power_mode_event)
        self.menu.append(self.power_mode)


        self.quit.set_label(_("Exit"))
        self.quit.connect('activate', self.quit_event)
        self.menu.append(self.quit)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        self.indicator.set_title(_("Pardus Power Manager"))

        # about dialog
        self.o("ui_about_dialog").set_program_name(_("Pardus Power Manager"))

        # settings page
        self.window.set_icon_name("pardus-power-manager")
        self.combobox_init()
        self.spinbutton_init()
        self.value_init()
        self.connect_signal()
        self.__is_init = True

    def connect_signal(self):
        self.window.connect("delete-event", self.window_delete_event)
        self.o("ui_button_powersave").connect("clicked",self.powersave_event)
        self.o("ui_button_performance").connect("clicked",self.performance_event)
        self.o("ui_combobox_acmode").connect("changed",self.save_settings)
        self.o("ui_combobox_batmode").connect("changed",self.save_settings)
        self.o("ui_checkbox_battery_treshold").connect("toggled",self.save_settings)
        self.o("ui_scale_brightness").connect("value-changed",self.set_brightness)
        self.o("ui_spinbutton_switch_to_performance").connect("value-changed",self.save_settings)
        self.o("ui_button_about").connect("clicked",self.__about_event)


    def __about_event(self, widget):
        self.o("ui_about_dialog").run()
        self.o("ui_about_dialog").hide()

###### widget init ######

    def combobox_init(self):
        store = Gtk.ListStore(str, str)
        store.append([_("Performance"),"performance"])
        store.append([_("Powersave"),"powersave"])
        store.append([_("Do Noting"),"ignore"])
        self.o("ui_combobox_acmode").set_model(store)
        self.o("ui_combobox_batmode").set_model(store)
        cellrenderertext = Gtk.CellRendererText()
        self.o("ui_combobox_acmode").pack_start(cellrenderertext, True)
        self.o("ui_combobox_acmode").add_attribute(cellrenderertext, "text", 0)
        self.o("ui_combobox_batmode").pack_start(cellrenderertext, True)
        self.o("ui_combobox_batmode").add_attribute(cellrenderertext, "text", 0)

    def spinbutton_init(self):
        self.o("ui_spinbutton_switch_to_performance").set_range(0,100)
        self.o("ui_spinbutton_switch_to_performance").set_increments(1,1)
        self.o("ui_spinbutton_switch_to_performance").set_digits(0)


    def value_init(self):
        self.o("ui_spinbutton_switch_to_performance").set_value(float(get("powersave_threshold","25","modes")))
        self.o("ui_checkbox_battery_treshold").set_active(get("charge_stop_enabled","False","modes").lower() == "true")
        l = ["performance", "powersave", "ignore"]
        self.o("ui_combobox_acmode").set_active(l.index(get("ac-mode","performance","modes")))
        self.o("ui_combobox_batmode").set_active(l.index(get("bat-mode","powersave","modes")))

###### mode functions ######

    def power_mode_event(self, widget):
        data = {}
        if self.current_mode == "performance":
            data["new-mode"] = "powersave"
        else:
            data["new-mode"] = "performance"
        send_server(data)

    def update(self,data):
        self.init()
        print(data)
        self.update_lock = True
        if "mode" in data:
            if self.current_mode != data["mode"]:
                if self.current_mode != None:
                    self.send_notification(_("Power profile changed: ") + _(data["mode"]))
                self.current_mode = data["mode"]
                if self.current_mode == "powersave":
                    self.power_mode.set_label(_("Disable Powersave"))
                    self.indicator.set_icon("pardus-pm-powersave-symbolic")
                else:
                    self.power_mode.set_label(_("Enable Powersave"))
                    self.indicator.set_icon("pardus-pm-performance-symbolic")
        if "backlight" in data:
            if len(data["backlight"]) > 0 :
                for dev in data["backlight"].keys():
                    max = data["backlight"][dev]["max"]
                    cur = data["backlight"][dev]["current"]
                    print(max, cur)
                    self.o("ui_scale_brightness").set_value((cur*100)/max)
            else:
                self.o("ui_box_brightness").hide()
        if "show" in data:
            self.open_window_event(None)
        if self.current_mode == "powersave":
            self.o("ui_button_powersave").set_sensitive(False)
            self.o("ui_button_performance").set_sensitive(True)
        else:
            self.o("ui_button_powersave").set_sensitive(True)
            self.o("ui_button_performance").set_sensitive(False)

        self.update_lock = False

    def set_brightness(self, widget):
        if self.update_lock:
            return
        value = widget.get_value()
        data = {}
        data["new-backlight"] = {}
        data["new-backlight"]["all"]="%"+str(int(value))
        send_server(data)

###### settings saver ######

    def save_settings(self, a=None, b=None):
        data = {}
        # service
        data["service"] = {}
        data["service"]["enabled"] = True
        # modes
        data["modes"] = {}
        ac_w = self.o("ui_combobox_acmode")
        bat_w = self.o("ui_combobox_batmode")
        t = ac_w.get_active_iter()
        if t:
            data["modes"]["ac-mode"] = ac_w.get_model()[t][1]
        t = bat_w.get_active_iter()
        if t:
            data["modes"]["bat-mode"] = bat_w.get_model()[t][1]
        data["modes"]["charge_stop_enabled"] = str(self.o("ui_checkbox_battery_treshold").get_active())
        # backlight
        data["modes"]["powersave_threshold"] = str(self.o("ui_spinbutton_switch_to_performance").get_value())
        self.write_settings(data)
        fdata = {}
        fdata["update"]="client"
        send_server(fdata)

    @asynchronous
    def write_settings(self, data):
        subprocess.run(["pkexec", actions_file, "save", json.dumps(data)])

###### utility functions ######

    def send_notification(self,msg):
        notification = Notify.Notification.new(msg)
        notification.show()

    def o(self,name):
        return self.builder.get_object(name)

###### buttons event ######

    def powersave_event(self,widget):
        self.o("ui_button_powersave").set_sensitive(False)
        self.o("ui_button_performance").set_sensitive(True)
        data = {}
        data["pid"] = os.getpid()
        data["new-mode"] = "powersave"
        send_server(data)

    def performance_event(self,widget):
        self.o("ui_button_powersave").set_sensitive(True)
        self.o("ui_button_performance").set_sensitive(False)
        data = {}
        data["pid"] = os.getpid()
        data["new-mode"] = "performance"
        send_server(data)

###### Window functions ######

    def window_delete_event(self, widget=None, event=None):
        self.window.hide()
        self.__window_status = False
        self.open_window.set_label(_("Show"))
        return True

    def open_window_event(self, widget):
        self.__window_status = not self.__window_status
        if self.__window_status:
            self.open_window.set_label(_("Hide"))
            self.window.show()
            self.window.present()
        else:
            self.open_window.set_label(_("Show"))
            self.window.hide()

    def quit_event(self, widget):
        os.unlink("/run/user/{}/ppm/{}".format(os.getuid(),os.getpid()))
        Gtk.main_quit()


