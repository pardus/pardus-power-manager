#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:53:01 2024

@author: fatihaltun
"""

import os

import dbus
import dbus.mainloop.glib
import gi

gi.require_version("GLib", "2.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GLib, Gdk, Gio

try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as appindicator
except:
    # fall back to Ayatana
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as appindicator

# from UserSettings import UserSettings
from Utils import ErrorDialog

import locale
from locale import gettext as _

locale.bindtextdomain('pardus-power-manager', '/usr/share/locale')
locale.textdomain('pardus-power-manager')


def getenv(env_name):
    env = os.environ.get(env_name)
    return env if env else ""


gnome_desktop = False
if "gnome" in getenv("SESSION").lower() or "gnome" in getenv("XDG_CURRENT_DESKTOP").lower():
    gnome_desktop = True


class MainWindow(object):
    def __init__(self, application):
        self.Application = application

        self.main_window_ui_filename = os.path.dirname(os.path.abspath(__file__)) + "/../ui/MainWindow.glade"
        try:
            self.GtkBuilder = Gtk.Builder.new_from_file(self.main_window_ui_filename)
            self.GtkBuilder.connect_signals(self)
        except GObject.GError:
            print("Error reading GUI file: " + self.main_window_ui_filename)
            raise

        self.init_power_profiles_dbus()

        self.define_components()
        self.define_variables()

        self.main_window.set_application(application)

        # self.user_settings()
        # self.set_autostart()

        self.init_indicator()
        self.mark_current_profile()

        self.control_brightness()
        self.add_brightness_devices()

        self.monitor_brightness_devices()

        self.about_dialog.set_program_name(_("Pardus Power Manager"))
        if self.about_dialog.get_titlebar() is None:
            about_headerbar = Gtk.HeaderBar.new()
            about_headerbar.set_show_close_button(True)
            about_headerbar.set_title(_("About Pardus Power Manager"))
            about_headerbar.pack_start(Gtk.Image.new_from_icon_name("pardus-power-manager", Gtk.IconSize.LARGE_TOOLBAR))
            about_headerbar.show_all()
            self.about_dialog.set_titlebar(about_headerbar)

        # Set version
        # If not getted from __version__ file then accept version in MainWindow.glade file
        try:
            version = open(os.path.dirname(os.path.abspath(__file__)) + "/__version__").readline()
            self.about_dialog.set_version(version)
        except:
            pass

        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(os.path.dirname(os.path.abspath(__file__)) + "/../data/style.css")
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)

        if "tray" in self.Application.args.keys():
            self.main_window.set_visible(False)
        else:
            self.main_window.set_visible(True)
            self.main_window.show_all()

        self.set_indicator()

        self.hide_widgets()

    def init_power_profiles_dbus(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.ppd_bus = dbus.SystemBus()
        self.ppd_proxy = self.ppd_bus.get_object("net.hadess.PowerProfiles", "/net/hadess/PowerProfiles")
        self.ppd_interface = dbus.Interface(self.ppd_proxy, "net.hadess.PowerProfiles")

        self.ppd_bus.add_signal_receiver(
            self.on_profile_changed,
            dbus_interface="org.freedesktop.DBus.Properties",
            signal_name="PropertiesChanged",
            path="/net/hadess/PowerProfiles",
        )

    def on_profile_changed(self, interface_name, changed_properties, invalidated_properties):
        if "ActiveProfile" in changed_properties:
            new_profile = changed_properties["ActiveProfile"]
            print("signal: current_profile: {}".format(self.current_profile))
            print("signal: new_profile: {}".format(new_profile))
            if self.current_profile != new_profile:
                self.set_profile(new_profile)

    def define_components(self):
        self.main_window = self.GtkBuilder.get_object("ui_main_window")
        self.about_dialog = self.GtkBuilder.get_object("ui_about_dialog")

        self.ui_powersaver_button = self.GtkBuilder.get_object("ui_powersaver_button")
        self.ui_balanced_button = self.GtkBuilder.get_object("ui_balanced_button")
        self.ui_performance_button = self.GtkBuilder.get_object("ui_performance_button")

        self.ui_brightness_box = self.GtkBuilder.get_object("ui_brightness_box")

    def define_variables(self):
        self.dbus_power_profiles = self.ppd_interface.Get("net.hadess.PowerProfiles", "Profiles",
                                                          dbus_interface="org.freedesktop.DBus.Properties")
        self.power_profiles = ["{}".format(entry['Profile']) for entry in self.dbus_power_profiles]
        self.current_profile = self.ppd_interface.Get("net.hadess.PowerProfiles", "ActiveProfile",
                                                      dbus_interface="org.freedesktop.DBus.Properties")

        system_wide = "usr/share" in os.path.dirname(os.path.abspath(__file__))
        self.icon_powersaver = "pardus-pm-power-saver-symbolic" if system_wide else "power-profile-power-saver-symbolic"
        self.icon_balanced = "pardus-pm-balanced-symbolic" if system_wide else "spower-profile-balanced-symbolic"
        self.icon_performance = "pardus-pm-performance-symbolic" if system_wide else "power-profile-performance-symbolic"

        if gnome_desktop:
            self.icon_powersaver = "power-profile-power-saver-symbolic"
            self.icon_balanced = "power-profile-balanced-symbolic"
            self.icon_performance = "power-profile-performance-symbolic"

        self.brightness_available = False
        self.brightness_devices = {}

        self.brightness_error_message = ""

        self.device = ""
        self.value = ""

        print("Available profiles: {}".format(self.power_profiles))
        print("Current profile: {}".format(self.current_profile))

    # def user_settings(self):
    #     self.UserSettings = UserSettings()
    #     self.UserSettings.createDefaultConfig()
    #     self.UserSettings.readConfig()

    # def set_autostart(self):
    #     self.UserSettings.set_autostart(self.UserSettings.config_autostart)

    def init_indicator(self):
        self.indicator = appindicator.Indicator.new(
            "pardus-power-manager", "pardus-power-manager", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_title(_("Pardus Power Manager"))

        self.menu = Gtk.Menu()

        self.item_sh_app = Gtk.MenuItem()
        self.item_sh_app.connect("activate", self.on_menu_show_app)
        self.menu.append(self.item_sh_app)

        self.item_separator = Gtk.SeparatorMenuItem()
        self.menu.append(self.item_separator)

        self.item_powersaver = Gtk.MenuItem()
        if "power-saver" in self.power_profiles:
            self.item_powersaver.set_label(_("Power Saver"))
            self.item_powersaver.connect("activate", self.on_ui_powersaver_button_clicked)
            self.menu.append(self.item_powersaver)

        self.item_balanced = Gtk.MenuItem()
        if "balanced" in self.power_profiles:
            self.item_balanced.set_label(_("Balanced"))
            self.item_balanced.connect("activate", self.on_ui_balanced_button_clicked)
            self.menu.append(self.item_balanced)

            self.item_performance = Gtk.MenuItem()
            if "performance" in self.power_profiles:
                self.item_performance.set_label(_("Performance"))
                self.item_performance.connect("activate", self.on_ui_performance_button_clicked)
                self.menu.append(self.item_performance)

        self.item_separator1 = Gtk.SeparatorMenuItem()
        self.menu.append(self.item_separator1)

        self.item_quit = Gtk.MenuItem()
        self.item_quit.set_label(_("Quit"))
        self.item_quit.connect('activate', self.on_menu_quit_app)
        self.menu.append(self.item_quit)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    def set_indicator(self):

        if self.main_window.is_visible():
            self.item_sh_app.set_label(_("Hide App"))
        else:
            self.item_sh_app.set_label(_("Show App"))

    def hide_widgets(self):
        self.ui_powersaver_button.set_visible("power-saver" in self.power_profiles)
        self.ui_balanced_button.set_visible("balanced" in self.power_profiles)
        self.ui_performance_button.set_visible("performance" in self.power_profiles)
        self.ui_brightness_box.set_visible(self.brightness_available)

    def mark_current_profile(self):
        if self.current_profile == "power-saver":
            self.ui_powersaver_button.get_style_context().add_class("suggested-action")
            self.ui_balanced_button.get_style_context().remove_class("suggested-action")
            self.ui_performance_button.get_style_context().remove_class("suggested-action")
            if "[" not in self.item_powersaver.get_label():
                self.item_powersaver.set_label("[ {} ]".format(self.item_powersaver.get_label()))
            self.item_balanced.set_label("{}".format(
                self.item_balanced.get_label().replace("[", "").replace("]", "").strip()))
            self.item_performance.set_label("{}".format(
                self.item_performance.get_label().replace("[", "").replace("]", "").strip()))
            GLib.idle_add(self.indicator.set_icon, self.icon_powersaver)
        elif self.current_profile == "balanced":
            self.ui_balanced_button.get_style_context().add_class("suggested-action")
            self.ui_powersaver_button.get_style_context().remove_class("suggested-action")
            self.ui_performance_button.get_style_context().remove_class("suggested-action")
            if "[" not in self.item_balanced.get_label():
                self.item_balanced.set_label("[ {} ]".format(self.item_balanced.get_label()))
            self.item_powersaver.set_label("{}".format(
                self.item_powersaver.get_label().replace("[", "").replace("]", "").strip()))
            self.item_performance.set_label("{}".format(
                self.item_performance.get_label().replace("[", "").replace("]", "").strip()))
            GLib.idle_add(self.indicator.set_icon, self.icon_balanced)
        elif self.current_profile == "performance":
            self.ui_performance_button.get_style_context().add_class("suggested-action")
            self.ui_powersaver_button.get_style_context().remove_class("suggested-action")
            self.ui_balanced_button.get_style_context().remove_class("suggested-action")
            if "[" not in self.item_performance.get_label():
                self.item_performance.set_label("[ {} ]".format(self.item_performance.get_label()))
            self.item_powersaver.set_label("{}".format(
                self.item_powersaver.get_label().replace("[", "").replace("]", "").strip()))
            self.item_balanced.set_label("{}".format(
                self.item_balanced.get_label().replace("[", "").replace("]", "").strip()))
            GLib.idle_add(self.indicator.set_icon, self.icon_performance)

    def set_profile(self, profile_name):

        self.ppd_interface.Set("net.hadess.PowerProfiles", "ActiveProfile", profile_name,
                               dbus_interface="org.freedesktop.DBus.Properties")

        self.current_profile = self.ppd_interface.Get("net.hadess.PowerProfiles", "ActiveProfile",
                                                      dbus_interface="org.freedesktop.DBus.Properties")

        self.mark_current_profile()

        print("profile setted to: {}".format(profile_name))

    def monitor_brightness_devices(self):
        if self.brightness_available:
            self.mdir = {}
            for device, value in self.brightness_devices.items():
                self.mdir[device] = Gio.file_new_for_path("/sys/class/backlight/{}/brightness".format(
                    device)).monitor_file(0, None)
                self.mdir[device].connect('changed', self.on_brightness_changed_from_monitoring)

    def on_brightness_changed_from_monitoring(self, file_monitor, file, other_file, event_type):
        # print("on_brightness_changed_from_monitoring: {} {}".format(file.get_path(), event_type))
        if event_type in [Gio.FileMonitorEvent.CHANGES_DONE_HINT]:
            print("trigger: {} {}".format(file.get_path(), event_type))
            device = "{}".format(file.get_path()).split("/")[-2]
            brightness = self.get_current_brightness(device)
            print("trigger: device: {}, brightness: {}".format(device, brightness))
            self.set_brightness(device, brightness, from_monitoring=True)

    def control_brightness(self):
        if os.path.isdir("/sys/class/backlight") and os.listdir("/sys/class/backlight"):
            self.brightness_available = True
            backlight_devices = os.listdir("/sys/class/backlight")
            for dev in backlight_devices:
                self.brightness_devices[dev] = {"max_brightness": self.get_max_brightness(dev),
                                                "current_brightness": self.get_current_brightness(dev)}

            print("Brightness available. Devices: {}".format(self.brightness_devices))

    def get_max_brightness(self, device):
        max_brightness_file = "/sys/class/backlight/{}/max_brightness".format(device)
        if os.path.isfile(max_brightness_file):
            try:
                with open(max_brightness_file, "r") as f:
                    return int(f.read().strip())
            except Exception as e:
                print("Error in get_max_brightness. {}".format(e))
                return 0

    def get_current_brightness(self, device):
        current_brightness_file = "/sys/class/backlight/{}/brightness".format(device)
        if os.path.isfile(current_brightness_file):
            try:
                with open(current_brightness_file, "r") as f:
                    return int(f.read().strip())
            except Exception as e:
                print("Error in get_current_brightness. {}".format(e))
                return 0

    # def is_brightness_different(self, device, new_value):
    #     brightness_file = "/sys/class/backlight/{}/brightness".format(device)
    #     current_brightness_value = 0
    #     if os.path.isfile(brightness_file):
    #         try:
    #             with open(brightness_file, "r") as f:
    #                 current_brightness_value = int(f.read().strip())
    #         except Exception as e:
    #             print("Error in get_current_brightness. {}".format(e))
    #     return new_value != current_brightness_value

    def set_brightness(self, device, value, from_monitoring=False):
        self.brightness_error_message = ""
        self.device = device
        self.value = value

        # if self.is_brightness_different(device, value):
        #     print("brightness is changing.")
        #     if os.access("/sys/class/backlight/intel_backlight/brightness", os.W_OK):
        #         self.write_brightness(device, value)
        #     else:
        #         command = ["/usr/bin/pkexec", os.path.dirname(os.path.abspath(__file__)) + "/Brightness.py",
        #                    "{}".format(device), "{}".format(value)]
        #         self.start_brightness_process(command)
        # else:
        #     print("brightness same, controlling ui")
        #     ui_brightness_value = 0
        #     ui_brightness_adjustment = None
        #     for row in self.ui_brightness_box:
        #         if device == row.get_children()[1].get_adjustment().name:
        #             ui_brightness_adjustment = row.get_children()[1].get_adjustment()
        #             ui_brightness_value = int(ui_brightness_adjustment.get_value())
        #             break
        #     print("ui_brightness: {}, current_brightness:{}".format(ui_brightness_value, value))
        #     if ui_brightness_value != value and ui_brightness_adjustment is not None:
        #         ui_brightness_adjustment.set_value(value)
        #         print("ui_brightness_value changed to: {}".format(value))

        if not from_monitoring:
            if os.access("/sys/class/backlight/{}/brightness".format(device), os.W_OK):
                self.write_brightness(device, value)
            else:
                # command = ["/usr/bin/pkexec", os.path.dirname(os.path.abspath(__file__)) + "/Brightness.py",
                #            "{}".format(device), "{}".format(value)]
                # self.start_brightness_process(command)
                ErrorDialog(_("Error"), "{}:\n\n/sys/class/backlight/{}/brightness".format(
                    _("You don't have write permissions to file"), device))

        else:
            ui_brightness_value = 0
            ui_brightness_adjustment = None
            for row in self.ui_brightness_box:
                if device == row.get_children()[1].get_adjustment().name:
                    ui_brightness_adjustment = row.get_children()[1].get_adjustment()
                    ui_brightness_value = int(ui_brightness_adjustment.get_value())
                    break
            print("trigger control: ui_brightness: {}, current_brightness: {}".format(ui_brightness_value, value))
            if ui_brightness_value != value and ui_brightness_adjustment is not None:
                ui_brightness_adjustment.set_value(value)
                print("trigger: ui_brightness_value changed to: {}".format(value))

    def write_brightness(self, device, value):
        brightness_file = "/sys/class/backlight/{}/brightness".format(device)
        if os.path.isfile(brightness_file):
            fd = open("/sys/class/backlight/{}/brightness".format(device), "w")
            fd.write("{}".format(int(value)))
            fd.flush()
            fd.close()
            print("brightness changed to: {} {}".format(device, value))

    def add_brightness_devices(self):
        for row in self.ui_brightness_box:
            self.ui_brightness_box.remove(row)
        for device, value in self.brightness_devices.items():
            label = Gtk.Label.new()
            label.set_text(_("Screen Brightness:"))

            adjustment = Gtk.Adjustment.new(value=value["current_brightness"],
                                            lower=0,
                                            upper=value["max_brightness"],
                                            step_increment=value["max_brightness"] / 100,
                                            page_increment=value["max_brightness"] / 100,
                                            page_size=0)
            adjustment.name = device
            adjustment.connect("value-changed", self.on_brightness_changed)

            scale = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, adjustment)
            scale.set_draw_value(False)
            scale.set_inverted(False)
            scale.set_show_fill_level(False)
            scale.set_restrict_to_fill_level(True)

            box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 3)
            box.pack_start(label, True, True, 0)
            box.pack_start(scale, True, True, 0)

            self.ui_brightness_box.pack_start(box, True, True, 0)

    def on_brightness_changed(self, adjustment):
        print("on_brightness_changed: {} {}".format(adjustment.name, int(adjustment.get_value())))
        self.set_brightness(adjustment.name, int(adjustment.get_value()), from_monitoring=False)

    def on_ui_powersaver_button_clicked(self, button):
        self.set_profile("power-saver")

    def on_ui_balanced_button_clicked(self, button):
        self.set_profile("balanced")

    def on_ui_performance_button_clicked(self, button):
        self.set_profile("performance")

    def on_menu_show_app(self, *args):
        window_state = self.main_window.is_visible()
        if window_state:
            self.main_window.set_visible(False)
            self.item_sh_app.set_label(_("Show App"))
        else:
            self.main_window.set_visible(True)
            self.item_sh_app.set_label(_("Hide App"))
            self.main_window.present()

    def on_menu_quit_app(self, *args):
        if self.about_dialog.is_visible():
            self.about_dialog.hide()
        self.main_window.get_application().quit()

    def on_ui_about_button_clicked(self, button):
        self.about_dialog.run()
        self.about_dialog.hide()

    def on_ui_main_window_delete_event(self, widget, event):
        self.main_window.hide()
        self.item_sh_app.set_label(_("Show App"))
        return True

    def on_ui_main_window_destroy(self, widget, event):
        if self.about_dialog.is_visible():
            self.about_dialog.hide()
        self.main_window.get_application().quit()

    def start_brightness_process(self, params):
        pid, stdin, stdout, stderr = GLib.spawn_async(params, flags=GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                                      standard_output=True, standard_error=True)
        GLib.io_add_watch(GLib.IOChannel(stdout), GLib.IO_IN | GLib.IO_HUP, self.on_brightness_process_stdout)
        GLib.io_add_watch(GLib.IOChannel(stderr), GLib.IO_IN | GLib.IO_HUP, self.on_brightness_process_stderr)
        GLib.child_watch_add(GLib.PRIORITY_DEFAULT, pid, self.on_brightness_process_exit)

        return pid

    def on_brightness_process_stdout(self, source, condition):
        if condition == GLib.IO_HUP:
            return False
        line = source.readline()
        print("on_brightness_process_stdout - line: {}".format(line))
        return True

    def on_brightness_process_stderr(self, source, condition):
        if condition == GLib.IO_HUP:
            return False
        line = source.readline()
        print("on_brightness_process_stderr - line: {}".format(line))
        self.brightness_error_message = line
        return True

    def on_brightness_process_exit(self, pid, status):
        print("on_brightness_process_exit - status: {}".format(status))
        if status == 32256:  # operation cancelled | Request dismissed
            print("operation cancelled | Request dismissed")
        else:
            if self.brightness_error_message != "":
                ErrorDialog(_("Error"), "{}".format(self.brightness_error_message))
            else:
                if self.device != "" and self.value != "":
                    self.write_brightness(self.device, self.value)
