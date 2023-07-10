import gi
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class RebootDialog(Gtk.Dialog):
    def __init__(self):
        super().__init__(title="Reboot required", transient_for=None, flags=0)
        self.add_buttons("Quit", Gtk.ResponseType.CLOSE)
        self.add_buttons("Reboot now", Gtk.ResponseType.OK)
        label = Gtk.Label(label="Settings will take effect after reboot. Do you want to restart now?")

        box = self.get_content_area()
        box.add(label)
        self.show_all()
        response = self.run()
        if response == Gtk.ResponseType.OK:
            subprocess.run(["reboot"])
        elif response == Gtk.ResponseType.CANCEL:
            Gtk.main_quit()

        self.destroy()
