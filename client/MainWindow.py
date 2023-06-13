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
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.create_widgets()
        self.create_window()
        self.window.add(self.main_box)
        self.connect_signals()
        self.window.show_all()
        send_server()


    def create_widgets(self):
        self.but_powersave = Gtk.Button()
        self.but_performance = Gtk.Button()
        self.img_powersave = Gtk.Image.new_from_file("powersave.png")
        self.img_performance = Gtk.Image.new_from_file("performance.png")
        self.cm_mode_ac = Gtk.ComboBox(halign=Gtk.Align.CENTER)
        self.cm_mode_bat = Gtk.ComboBox(halign=Gtk.Align.CENTER)


    def create_window(self):
        # Service on off switch
        sbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        switch = Gtk.Switch(halign=Gtk.Align.CENTER)
        sbox.pack_start(switch, False, False, 13)
        sbox.pack_start(Gtk.Label("Service"), True, True, 0)
        self.main_box.pack_start(sbox, False, False, 13)
        # big mode buttons
        mbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        mbox.set_homogeneous(True)
        mbox.pack_start(self.but_powersave, True, True, 0)
        mbox.pack_start(self.but_performance, True, True, 0)
        self.main_box.pack_start(mbox, False, False, 13)
        # powersave button image
        self.but_powersave.set_always_show_image(True)
        ps_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        ps_box.pack_start(self.img_powersave, False, False, 0)
        ps_box.pack_start(Gtk.Label("Powersave"),False,False, 0)
        ps_box.show_all()
        self.but_powersave.set_image(ps_box)
        self.but_powersave.set_relief(Gtk.ReliefStyle.NONE)
        # performance button image
        self.but_performance.set_always_show_image(True)
        pm_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        pm_box.pack_start(self.img_performance, False, False, 0)
        pm_box.pack_start(Gtk.Label("Performance"),False,False, 0)
        pm_box.show_all()
        self.but_performance.set_image(pm_box)
        self.but_performance.set_relief(Gtk.ReliefStyle.NONE)
        # power settings combo
        cbox =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        cbox.pack_start(Gtk.Label("On Power"),False,False,0)
        self.cm_mode_ac.set_size_request(200, -1)
        cbox.pack_start(self.cm_mode_ac,False,False,0)
        cbox.pack_start(Gtk.Label("On Battery"),False,False,0)
        self.cm_mode_bat.set_size_request(200, -1)
        cbox.pack_start(self.cm_mode_bat,False,False,0)
        self.main_box.pack_start(cbox, False, False, 13)


    def destroy_signal(self,widget=None):
        os.unlink("/run/user/{}/ppm/{}".format(os.getuid(),os.getpid()))
        Gtk.main_quit()


    def connect_signals(self):
        self.window.connect("destroy",self.destroy_signal)

    def update(self,data):
        self.label.set_label(str(data))
