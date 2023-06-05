from util import send_client
import backends.power as power
import backends.backlight as backlight
def main(data):
    print(data)
    if "new-mode" in data:
        power.set_mode(data["new-mode"])
    if "new-backlight" in data:
        for dev in data[new-backlight]:
             backlight.set_brightness(dev, data[new-backlight][dev])
    udata = {}
    udata["current-mode"] = power.get_mode()
    udata["current-backlight"] = {}
    udata["max-backlight"] = {}
    for dev in backlight.get_devices():
        udata["current-backlight"][dev] = backlight.get_brightness(dev)
        udata["max-backlight"][dev] = backlight.get_max_brightness(dev)
    print(udata)
    send_client(udata)
