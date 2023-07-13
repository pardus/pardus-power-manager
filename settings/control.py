import os
import subprocess
def service_stop():
    os.unlink("/run/ppm")
    if os.path.exists("/lib/systemd/systemd"):
        subprocess.run(["systemctl", "stop", "ppm"])
    elif os.path.exists("/sbin/rc-service"):
        subprocess.run(["rc-service", "ppm", "stop"])

def service_start():
    if os.path.exists("/lib/systemd/systemd"):
        subprocess.run(["systemctl", "start", "ppm"])
    elif os.path.exists("/sbin/rc-service"):
        subprocess.run(["rc-service", "ppm", "start"])
