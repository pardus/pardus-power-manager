import gi
from gi.repository import GLib
from util import *

class battery:

    def __init__(self,name):
        self.name = name
        self.level=100
        self.status="unknown"
        self.update()

    def update(self):
        path="/sys/class/power_supply/{}/".format(self.name)
        # battery level
        if os.path.exists("{}/energy_now".format(path)):
            now= readfile("{}/energy_now".format(path))
            max= readfile("{}/energy_full".format(path))
            self.level = int(max)/int(now)
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


acpi_battery = []
def battery_init():
    global acpi_battery
    for dev in get_acpi_power_devices():
        b = battery(dev)
        acpi_battery.append(b)
    while True:
        battery_main()
        time.sleep(1)

def battery_main():
    for b in acpi_battery:
        b.update()
        print(b.level)
    print("loop")
