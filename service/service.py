from util import send_client
import power
import backlight
def main(data):
    print(data)
    if "new-mode" in data:
        power.set_mode(data["new-mode"])
    udata = {}
    udata["current-mode"] = power.get_mode()
    udata["current-backlight"] = {}
    for dev in backlightd.get_devices():
        udata["current-backlight"][dev] = backlight.get_brightness(dev)
    send_client(udata)
