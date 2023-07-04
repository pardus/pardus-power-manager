import os
import sys
from file import *
def get_ac_online():
    if not os.path.exists("/sys/class/power_supply/"):
        return True
    if len(os.listdir("/sys/class/power_supply/")) == 0:
        return True
    for device in get_acpi_power_devices():
        if os.path.exists("/sys/class/power_supply/{}/status".format(device)):
            status = readfile("/sys/class/power_supply/{}/status".format(device)).lower().strip()
            if "discharging" in status:
                return False
            elif "not charging" in status:
                return True
            elif "charging" in status:
                return True
            elif "full" in status:
                return True
            elif "empty" in status:
                return False
            elif "unknown" in status:
                return True
    return True

def get_acpi_power_devices():
    devices = []
    for interface in os.listdir("/sys/bus/acpi/devices/"):
        acpi_device = "/sys/bus/acpi/devices/{}/power_supply".format(interface)
        if os.path.exists(acpi_device):
            for device in os.listdir(acpi_device):
                devices.append(device)
    return devices


def get_3d_controller_pci():
    for fdir in os.listdir("/sys/class/drm/"):
        if fdir.startswith("card") and fdir[4:].isnumeric():
            ctx = readfile("/sys/class/drm//{}/device/class".format(fdir))
            if ctx.startswith("0x0302"):
                return os.readlink("/sys/class/drm//{}/device".format(fdir))[-12:]
    return None

def remove_pci(id):
    if os.path.exits("/sys/bus/pci/devices/{}/driver".format(id)):
        module = os.readlink("/sys/bus/pci/devices/{}/driver/module".format(id))
        module = os.part.basename(module)
        os.system("rmmod -f '{}'"/format(module))
    writefile("/sys/bus/pci/devices/{}/remove".format(id))
    os.system("udevadm control --reload")
