#!/usr/bin/env python3
import gi, os, sys, subprocess, json
gi.require_version('Gtk', '3.0')

# FIXME: remove this
def _(msg):
    return msg

from gi.repository import GLib, Gtk
sys.path.insert(0, os.path.dirname( os.path.realpath(__file__) )+"/../common")
from common import *
from control import *

def fint(ctx):
    ret = ""
    for c in ctx:
        if c in "0123456789":
            ret += c
    return int(ret)



class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../data/MainWindow.ui")
        self.window = self.builder.get_object("ui_window_main")
        self.combobox_init()
        self.spinbutton_init()
        self.value_init()
        self.power_buttons_init()
        self.widget_changes_event_init()
        self.window.connect("destroy",Gtk.main_quit)

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
        self.o("ui_switch_service").set_state(get("enabled",True,"service"))
        self.o("ui_spinbutton_switch_to_performance").set_value(fint(get("powersave_threshold","25","modes")))
        l = ["performance", "powersave", "ignore"]
        self.o("ui_combobox_acmode").set_active(l.index(get("ac-mode","performance","modes")))
        self.o("ui_combobox_batmode").set_active(l.index(get("bat-mode","powersave","modes")))
        self.o("ui_box_main").set_sensitive(get("enabled",True,"service"))

    def widget_changes_event_init(self):
        self.o("ui_switch_service").connect("notify::active",self.save_settings)
        self.o("ui_combobox_acmode").connect("changed",self.save_settings)
        self.o("ui_combobox_batmode").connect("changed",self.save_settings)
        self.o("ui_spinbutton_switch_to_performance").connect("value-changed",self.save_settings)

    def o(self,name):
        return self.builder.get_object(name)


    def power_buttons_init(self):
        @asynchronous
        def powersave_event(widget):
            data = {}
            data["pid"] = os.getpid()
            data["new-mode"] = "powersave"
            if os.path.exists("/run/ppm"):
                with open("/run/ppm","w") as f:
                    f.write(json.dumps(data))
        @asynchronous
        def performance_event(widget):
            data = {}
            data["pid"] = os.getpid()
            data["new-mode"] = "performance"
            if os.path.exists("/run/ppm"):
                with open("/run/ppm","w") as f:
                    f.write(json.dumps(data))
        self.o("ui_button_powersave").connect("clicked",powersave_event)
        self.o("ui_button_performance").connect("clicked",performance_event)


    def save_settings(self, a=None, b=None):
        data = {}
        # service
        data["service"] = {}
        data["service"]["enabled"] = self.o("ui_switch_service").get_state()
        self.o("ui_box_main").set_sensitive(data["service"]["enabled"])
        if data["service"]["enabled"]:
            service_start()
        else:
            service_stop()
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
        # backlight
        data["modes"]["powersave_threshold"] = str(self.o("ui_spinbutton_switch_to_performance").get_value())
        self.write_settings(data)

    def write_settings(self,data):
        ctx = ""
        for section in data:
            ctx += "[" + section + "]\n"
            for var in data[section]:
                ctx += str(var) + "=" + str(data[section][var]) +"\n"
            ctx += "\n"
        writefile("/etc/pardus/ppm.conf.d/99-ppm-settings.conf",ctx)

if __name__ == "__main__":
    if os.getuid() != 0 and "--test" not in sys.argv:
        subprocess.run(["pkexec", "/usr/share/pardus/power-manager/settings/main.py"])
        exit(0)
    try:
        import socket
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind('\0ppm_settings_lock')
    except socket.error as e:
        sys.exit (0)

    main = MainWindow()
    main.window.show()
    Gtk.main()
