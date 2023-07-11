from util import *
import backends.power as power
import backends.backlight as backlight
import backends.battery as battery

def main(data):
    debug("Reading /run/ppm fifo")
    # mode switch
    if "new-mode" in data:
        if data["new-mode"] in ["powersave", "performance"]:
            power.set_mode(data["new-mode"])
    if "new-backlight" in data:
        for dev in data["new-backlight"]:
             backlight.set_brightness(dev, data["new-backlight"][dev])
    # battery events
    if acpi_battery == None:
        battery_init()
    for b in acpi_battery:
        b.update()
        if "update" in data and data["update"] == "service":
            reload_config()
            if b.level <= int(get("powersave_threshold","25","modes")):
                power.set_mode("powersave")
    # client update
    udata = {}
    udata["mode"] = power.get_mode()
    udata["backlight"] = {}
    for dev in backlight.get_devices():
        udata["backlight"][dev] = {}
        udata["backlight"][dev]["current"] = backlight.get_brightness(dev)
        udata["backlight"][dev]["max"] = backlight.get_max_brightness(dev)
    udata["battery"] = {}
    for dev in acpi_battery:
        udata["battery"][dev.name] = {}
        udata["battery"][dev.name]["level"] = dev.level
        udata["battery"][dev.name]["real_name"] = dev.real_name
        udata["battery"][dev.name]["status"] = dev.status
        udata["battery"][dev.name]["health"] = dev.health
        udata["battery"][dev.name]["power_usage"] = dev.power_usage
    send_client(udata)


acpi_battery = None
def battery_init():
    global acpi_battery
    acpi_battery = []
    for dev in get_acpi_power_devices():
        path="/sys/class/power_supply/{}/".format(dev)
        devtype = readfile("{}/type".format(path)).lower()
        if  devtype == "battery":
            b = battery.battery(dev)
            acpi_battery.append(b)
