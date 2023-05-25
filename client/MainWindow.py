import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk
print(os.getpid())
from util import send_server

class MainWindow:
    def __init__(self):
        self.window = Gtk.Window()
        self.label = Gtk.Label()
        self.main_box = Gtk.Box()
        self.window.add(self.main_box)
        # TODO: Remove this test buttons
        self.test()

        self.main_box.pack_start(self.label,False,False,0)
        self.connect_signals()
        self.window.show_all()
        send_server({})

    def destroy_signal(self,widget=None):
        os.unlink("{}/ppm/{}".format(os.environ["XDG_RUNTIME_DIR"],os.getpid()))
        Gtk.main_quit()

    def test(self):
        self.a = Gtk.Button("performance")
        self.b = Gtk.Button("powersave")
        self.main_box.pack_start(self.a,False,False,0)
        self.main_box.pack_start(self.b,False,False,0)
        def aaa(widget=None):
            data = {'new-mode': "performance"}
            send_server(data)
        def bbb(widget=None):
            data = {'new-mode': "powersave"}
            send_server(data)
        self.a.connect("clicked",aaa)
        self.b.connect("clicked",bbb)

    def connect_signals(self):
        self.window.connect("destroy",self.destroy_signal)

    def update(self,data):
        self.label.set_label(str(data))
