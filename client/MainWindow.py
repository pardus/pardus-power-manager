import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk
print(os.getpid())
from util import send_server

class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/MainWindow.ui")
        self.window = self.builder.get_object("ui_window_main")
        self.window.show_all()
        self.connect_signals()
        send_server()


    def destroy_signal(self,widget=None):
        os.unlink("/run/user/{}/ppm/{}".format(os.getuid(),os.getpid()))
        Gtk.main_quit()


    def connect_signals(self):
        self.window.connect("destroy",self.destroy_signal)

    def update(self,data):
        print(data)
