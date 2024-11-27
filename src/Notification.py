#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:53:01 2024

@author: fatih
"""

import gi

gi.require_version("Notify", "0.7")
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Notify

import locale
from locale import gettext as _

locale.bindtextdomain('pardus-power-manager', '/usr/share/locale')
locale.textdomain('pardus-power-manager')


class Notification(GObject.GObject):
    __gsignals__ = {
        'notify-action': (GObject.SIGNAL_RUN_FIRST, None,
                          (str,))
    }

    def __init__(self, summary="", body="", icon="pardus-power-manager", app_id="tr.org.pardus-power-manager"):
        GObject.GObject.__init__(self)
        if Notify.is_initted():
            Notify.uninit()
        Notify.init(app_id)
        self.notification = Notify.Notification.new(summary, body, icon)
        self.notification.set_app_name(_("Pardus Power Manager"))
        self.notification.add_action('close', _('Close'), self.close_callback)
        self.notification.connect('closed', self.on_closed)

    def show(self):
        self.notification.show()

    def close_callback(self, widget, action):
        self.emit('notify-action', 'closed')

    def on_closed(self, widget):
        self.emit('notify-action', 'closed')
