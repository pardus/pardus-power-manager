#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:53:01 2024

@author: fatihaltun
"""

import os
import signal
import subprocess

import gi

gi.require_version("GLib", "2.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

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

        self.define_components()
        self.define_variables()
        self.main_window.set_application(application)

        self.user_settings()

        self.set_autostart()
        self.init_indicator()

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

        def sighandler(signum, frame):
            if self.about_dialog.is_visible():
                self.about_dialog.hide()
            self.main_window.get_application().quit()

        signal.signal(signal.SIGINT, sighandler)
        signal.signal(signal.SIGTERM, sighandler)

        if "tray" in self.Application.args.keys():
            self.main_window.set_visible(False)
        else:
            self.main_window.set_visible(True)
            self.main_window.show_all()

        self.set_indicator()

    def define_components(self):
        self.main_window = self.GtkBuilder.get_object("ui_main_window")
        self.about_dialog = self.GtkBuilder.get_object("ui_about_dialog")

    def define_variables(self):
        pass

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
        self.item_separator = Gtk.SeparatorMenuItem()
        self.item_quit = Gtk.MenuItem()
        self.item_quit.set_label(_("Quit"))
        self.item_quit.connect('activate', self.on_menu_quit_app)
        self.menu.append(self.item_sh_app)
        self.menu.append(self.item_separator)
        self.menu.append(self.item_quit)
        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    def set_indicator(self):

        if self.main_window.is_visible():
            self.item_sh_app.set_label(_("Hide App"))
        else:
            self.item_sh_app.set_label(_("Show App"))

    def set_autostart(self):
        self.UserSettings.set_autostart(self.UserSettings.config_autostart)

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
