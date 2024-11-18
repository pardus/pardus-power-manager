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
from gi.repository import Gtk, GObject, GLib

try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as appindicator
except:
    # fall back to Ayatana
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as appindicator

from UserSettings import UserSettings

import locale
from locale import gettext as _

locale.bindtextdomain('pardus-power-manager', '/usr/share/locale')
locale.textdomain('pardus-power-manager')


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

        self.user_settings()

        self.set_autostart()

        self.init_indicator()
        self.mark_current_profile()

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

    def define_variables(self):
        self.dbus_power_profiles = self.ppd_interface.Get("net.hadess.PowerProfiles", "Profiles",
                                                          dbus_interface="org.freedesktop.DBus.Properties")
        self.power_profiles = ["{}".format(entry['Profile']) for entry in self.dbus_power_profiles]
        self.current_profile = self.ppd_interface.Get("net.hadess.PowerProfiles", "ActiveProfile",
                                                      dbus_interface="org.freedesktop.DBus.Properties")

        print("Available profiles: {}".format(self.power_profiles))
        print("Current profile: {}".format(self.current_profile))

    def user_settings(self):
        self.UserSettings = UserSettings()
        self.UserSettings.createDefaultConfig()
        self.UserSettings.readConfig()

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

    def set_profile(self, profile_name):

        self.ppd_interface.Set("net.hadess.PowerProfiles", "ActiveProfile", profile_name,
                               dbus_interface="org.freedesktop.DBus.Properties")

        self.current_profile = self.ppd_interface.Get("net.hadess.PowerProfiles", "ActiveProfile",
                                                      dbus_interface="org.freedesktop.DBus.Properties")

        self.mark_current_profile()

        print("profile setted to: {}".format(profile_name))

    def set_autostart(self):
        self.UserSettings.set_autostart(self.UserSettings.config_autostart)

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
