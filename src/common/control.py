import os
def service_stop():
    if os.path.exists("/run/ppm"):
        os.unlink("/run/ppm")
    if os.path.exists("/lib/systemd/systemd"):
        os.system("systemctl stop ppm")

def service_start():
    if os.path.exists("/run/ppm"):
        os.unlink("/run/ppm")
    if os.path.exists("/lib/systemd/systemd"):
        os.system("systemctl start ppm")
