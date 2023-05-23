import os
from util import writefile
_cur_mode = None
def set_mode(mode):
    global _cur_mode
    if mode == _cur_mode:
        return
    if mode == "performance":
        _performance()
    elif mode == "powersave":
        _powersave()
    else:
        return
    _cur_mode = mode
    print("New mode: {}".format(mode))

def get_mode():
    return _cur_mode


# https://wiki.debian.org/SimplePowerSave
def _powersave():
    # laptop mode
    writefile("/proc/sys/vm/laptop_mode",1)

    # sata channel
    scsi_host_path="/sys/class/scsi_host/"
    for dir in os.listdir(scsi_host_path):
        if dir.startswith("host"):
            writefile("{}/{}/link_power_management_policy".format(scsi_host_path,dir),"min_power")
    # cpu governor
    cpu_path="/sys/devices/system/cpu/"
    for dir in os.listdir(cpu_path):
        if dir.startswith("cpu"):
            writefile("{}/{}/cpufreq/scaling_governor".format(cpu_path,dir),"powersave")
    # usb auto suspend
    usb_path="/sys/bus/usb/devices/"
    for dir in os.listdir(usb_path):
        writefile("{}/{}/power/control".format(usb_path,dir),"on")

    # pci auto suspend
    pci_path="/sys/bus/pci/devices/"
    for dir in os.listdir(pci_path):
        writefile("{}/{}/power/control".format(pci_path,dir),"on")

    # i2c auto suspend
    i2c_path="/sys/bus/i2c/devices/"
    for dir in os.listdir(i2c_path):
        writefile("{}/{}/power/control".format(i2c_path,dir),"on")


    # audio card
    writefile("/sys/module/snd_hda_intel/parameters/power_save",5)
    writefile("/sys/module/snd_hda_intel/parameters/power_save_controller","Y")

    # turbo boost
    writefile("/sys/devices/system/cpu/intel_pstate/no_turbo",1)
    writefile("/sys/devices/system/cpu/cpufreq/boost",0)

    # network
    net_path="/sys/class/net/"
    for dir in os.listdir(net_path):
        writefile("{}/{}/device/power/control".format(net_path,dir),"auto")


def _performance():
    # laptop mode
    writefile("/proc/sys/vm/laptop_mode",0)

    # sata channel
    scsi_host_path="/sys/class/scsi_host/"
    for dir in os.listdir(scsi_host_path):
        if dir.startswith("host"):
            writefile("{}/{}/link_power_management_policy".format(scsi_host_path,dir),"max_performance")
    # cpu governor
    cpu_path="/sys/devices/system/cpu/"
    for dir in os.listdir(cpu_path):
        if dir.startswith("cpu"):
            writefile("{}/{}/cpufreq/scaling_governor".format(cpu_path,dir),"performance")

    # usb auto suspend
    usb_path="/sys/bus/usb/devices/"
    for dir in os.listdir(usb_path):
        writefile("{}/{}/power/control".format(usb_path,dir),"on")

    # pci auto suspend
    pci_path="/sys/bus/pci/devices/"
    for dir in os.listdir(pci_path):
        writefile("{}/{}/power/control".format(pci_path,dir),"on")

    # i2c auto suspend
    i2c_path="/sys/bus/i2c/devices/"
    for dir in os.listdir(i2c_path):
        writefile("{}/{}/power/control".format(i2c_path,dir),"on")

    # audio card
    writefile("/sys/module/snd_hda_intel/parameters/power_save",0)
    writefile("/sys/module/snd_hda_intel/parameters/power_save_controller","N")

    # turbo boost
    writefile("/sys/devices/system/cpu/intel_pstate/no_turbo",0)
    writefile("/sys/devices/system/cpu/cpufreq/boost",1)

    # network
    net_path="/sys/class/net/"
    for dir in os.listdir(net_path):
        writefile("{}/{}/device/power/control".format(net_path,dir),"on")

