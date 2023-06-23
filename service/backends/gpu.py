import os, subprocess
from common import *

def pci_remove(id):
    if os.path.isdir("/sys/bus/pci/devices/0000:{}/driver".format(id)):
        module = os.readlink("/sys/bus/pci/devices/0000:/driver/module".format(id))
        module = os.basename(module)
        subprocess.run(["rmmod", "-f", module])

    with open("/sys/bus/pci/devices/0000:{}/remove".format(id), "w") as f:
        f.write("1")

def disable_3d_controller():
    with open("/sys/bus/pci/rescan", "w") as f:
        f.write("1")
        for pci in list_3d_controller():
            pci_remove(pci)
    subprocess.run(["udevadm", "control", "--reload"])

