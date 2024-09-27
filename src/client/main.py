#!/usr/bin/env python3
from util import *
from MainWindow import *
import os, sys

import gi, json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

client_dir = "/run/user/{}/ppm/".format(os.getuid())
no_show = False
if os.path.exists(client_dir):
    if len(os.listdir(client_dir)) > 0:
        data = {}
        data["pid"] = os.getpid()
        data["show"] = str(os.getuid())
        no_show = True
        with open("/run/ppm","w") as f:
            f.write(json.dumps(data))
if no_show:
    exit(0)

class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="tr.org.pardus.power-manager",
                         flags=Gio.ApplicationFlags(8), **kwargs)
        self.main = None
        GLib.set_prgname("tr.org.pardus.power-manager")

        self.add_main_option(
            "test",
            ord("t"),
            GLib.OptionFlags(0),
            GLib.OptionArg(0),
            "Start application on test mode",
            None,
        )
        self.add_main_option(
            "autostart",
            ord("a"),
            GLib.OptionFlags(0),
            GLib.OptionArg(0),
            "Start application on autostart mode",
            None,
        )

    def do_activate(self):
        print("Client started")
        self.main = MainWindow()
        listen(self.main)
        if "--autostart" not in sys.argv:
            self.main.open_window_event(None)
        data = {}
        data["update"]="client"
        data["pid"] = os.getpid()
        send_server(data)


    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()
        self.args = options
        self.activate()
        return 0


app = Application()
app.run(sys.argv)
Gtk.main()

