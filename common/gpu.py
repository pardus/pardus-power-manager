import os
def list_3d_controller():
    ret = []
    for dev in os.listdir("/sys/class/drm/"):
        if dev.startswith("card") and dev[4:].isnumeric():
            # 03 Display Controller
            # 02 3D Controller
            dclass = open("/sys/class/drm/{}/device/class".format(dev),"r").read()
            if dclass.startswith("0x0302"):
                pci = os.readlink("/sys/class/drm/{}/device".format(dev))
                pci = os.path.basename(pci)[5:]
                ret.append(pci)
    return ret
