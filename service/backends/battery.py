import gi
from gi.repository import GLib
from util import *

class battery:

    def __init__(self,name):
        self.name = name
        self.level = 100
        self.status = "unknown"
        self.health = 100
        self.update()

    def update(self):
        path="/sys/class/power_supply/{}/".format(self.name)
        # battery level
        if os.path.exists("{}/energy_now".format(path)):
            now= readfile("{}/energy_now".format(path))
            max= readfile("{}/energy_full".format(path))
            self.level = int(now)/int(max) * 100
        elif os.path.exists("{}/capacity".format(path)):
            self.level = int(readfile("{}/capacity".format(path)))
        elif os.path.exists("{}/capacity_level".format(path)):
            level = readfile("{}/capacity_level".format(path)).lower()
            if level == "unknown" or level == "high":
                self.level = 100
            elif level == "normal":
                self.level = 80
            elif level == "low":
                self.level = 40
            elif self.level == "clitical":
                self.level = 20
        else:
            self.level = 100
        # stat us
        if os.path.exists("{}/status".format(path)):
            self.status = readfile("{}/status".format(path)).lower()
        # battery health
        if os.path.exists("{}/energy_full_design".format(path)):
            max= readfile("{}/energy_full".format(path))
            hmax= readfile("{}/energy_full_design".format(path))
            self.health = int(max) * 100 / int(hmax)


acpi_battery = []
def battery_init():
    global acpi_battery
    for dev in get_acpi_power_devices():
        path="/sys/class/power_supply/{}/".format(dev)
        devtype = readfile("{}/type".format(path)).lower()
        if  devtype == "battery":
            b = battery(dev)
            acpi_battery.append(b)

def battery_main():
    for b in acpi_battery:
        b.update()
        print(b.name,b.level,b.health)
