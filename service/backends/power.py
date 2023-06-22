import os
from util import writefile, readfile, listdir
from backends.cpu import list_cpu, change_cpu_status
from common import *


_cur_mode = None

def set_mode(mode):
    global _cur_mode
    if mode == "performance":
        _performance()
    elif mode == "powersave":
        _powersave()
    _cur_mode = mode
    log("New mode: {}".format(mode))

def get_mode():
    return _cur_mode


# https://wiki.debian.org/SimplePowerSave
@asynchronous
def _powersave():
    # laptop mode
    writefile("/proc/sys/vm/laptop_mode",1)

    # platform profile
    writefile("/sys/firmware/acpi/platform_profile","low-power")

    # less disk activity
    writefile("/proc/sys/vm/dirty_writeback_centisecs",1500)

    if get("scsi",True,"powersave"):
        # sata channel
        scsi_host_path="/sys/class/scsi_host/"
        for dir in listdir(scsi_host_path):
            if dir.startswith("host"):
                writefile("{}/{}/link_power_management_policy".format(scsi_host_path,dir),"min_power")

    if get("governor",True,"powersave"):
        # cpu governor
        cpu_path="/sys/devices/system/cpu/"
        for dir in listdir(cpu_path):
            if dir.startswith("cpu"):
                writefile("{}/{}/cpufreq/scaling_governor".format(cpu_path,dir),"powersave")
    if get("usb-suspend",True,"powersave"):
        # usb auto suspend
        usb_path="/sys/bus/usb/devices/"
        for dir in listdir(usb_path):
            writefile("{}/{}/power/control".format(usb_path,dir),"on")

    if get("pci-suspend",True,"powersave"):
        # pci auto suspend
        pci_path="/sys/bus/pci/devices/"
        for dir in listdir(pci_path):
            writefile("{}/{}/power/control".format(pci_path,dir),"on")

    if get("i2c-suspend",True,"powersave"):
        # i2c auto suspend
        i2c_path="/sys/bus/i2c/devices/"
        for dir in listdir(i2c_path):
            writefile("{}/{}/power/control".format(i2c_path,dir),"on")

    if get("audio",True,"powersave"):
        # audio card
        writefile("/sys/module/snd_hda_intel/parameters/power_save",5)
        writefile("/sys/module/snd_hda_intel/parameters/power_save_controller","Y")


    if get("turbo",True,"powersave"):
        # turbo boost
        writefile("/sys/devices/system/cpu/intel_pstate/no_turbo",1)
        writefile("/sys/devices/system/cpu/cpufreq/boost",0)

    if get("network",True,"powersave"):
        # network
        net_path="/sys/class/net/"
        for dir in listdir(net_path):
            writefile("{}/{}/device/power/control".format(net_path,dir),"auto")

    if get("cpufreq",True,"powersave"):
        # decrease max cpu freq
        ratio = float(get("freq-ratio",0.5,"powersave"))
        if ratio > 1.0:
            ratio = 1.0
        cpu_path="/sys/devices/system/cpu/"
        for dir in listdir(cpu_path):
            if not dir.startswith("cpu"):
                continue
            freq_file = "{}/{}/cpufreq/scaling_available_frequencies".format(cpu_path,dir)
            if os.path.exists(freq_file):
                freqs = readfile(freq_file).split(" ")
                if len(freqs) > 0 and freqs[0] != '':
                    new_freq = freqs[int((len(freqs) -1) * ratio)]
                    writefile("{}/{}/cpufreq/scaling_max_freq".format(cpu_path,dir),int(new_freq))
            else:
                min_freq=readfile("{}/{}/cpufreq/cpuinfo_min_freq".format(cpu_path,dir))
                max_freq=readfile("{}/{}/cpufreq/cpuinfo_max_freq".format(cpu_path,dir))
                if min_freq != "" and max_freq != "":
                    new_freq = int(max_freq) * ratio
                    writefile("{}/{}/cpufreq/scaling_max_freq".format(cpu_path,dir),int(new_freq))

    if get("core",True,"powersave"):
        # disable cpu core
        cpus = list_cpu()
        dnum = len(cpus) * float(get("core-ratio",0.5,"powersave"))
        if len(cpus) <= 4:
            dnum = len(cpus)
        elif len(cpus) - dnum < 4:
            dnum = 4
        for cpu in range(len(cpus) - int(dnum), len(cpus)):
            change_cpu_status(cpu,False)

@asynchronous
def _performance():
    # laptop mode
    writefile("/proc/sys/vm/laptop_mode",0)

    # platform profile
    writefile("/sys/firmware/acpi/platform_profile","performance")


    # more disk activity
    writefile("/proc/sys/vm/dirty_writeback_centisecs",500)

    if get("scsi",True,"performance"):
        # sata channel
        scsi_host_path="/sys/class/scsi_host/"
        for dir in listdir(scsi_host_path):
            if dir.startswith("host"):
                writefile("{}/{}/link_power_management_policy".format(scsi_host_path,dir),"max_performance")

    if get("governor",True,"performance"):
        # cpu governor
        cpu_path="/sys/devices/system/cpu/"
        for dir in listdir(cpu_path):
            if dir.startswith("cpu"):
                writefile("{}/{}/cpufreq/scaling_governor".format(cpu_path,dir),"performance")

    if get("usb",True,"performance"):
        # usb auto suspend
        usb_path="/sys/bus/usb/devices/"
        for dir in listdir(usb_path):
            writefile("{}/{}/power/control".format(usb_path,dir),"on")

    if get("pci",True,"performance"):
        # pci auto suspend
        pci_path="/sys/bus/pci/devices/"
        for dir in listdir(pci_path):
            writefile("{}/{}/power/control".format(pci_path,dir),"on")

    if get("i2c",True,"performance"):
        # i2c auto suspend
        i2c_path="/sys/bus/i2c/devices/"
        for dir in listdir(i2c_path):
            writefile("{}/{}/power/control".format(i2c_path,dir),"on")

    if get("audio",True,"performance"):
        # audio card
        writefile("/sys/module/snd_hda_intel/parameters/power_save",0)
        writefile("/sys/module/snd_hda_intel/parameters/power_save_controller","N")

    if get("turbo",True,"performance"):
        # turbo boost
        writefile("/sys/devices/system/cpu/intel_pstate/no_turbo",0)
        writefile("/sys/devices/system/cpu/cpufreq/boost",1)

    if get("network",True,"performance"):
        # network
        net_path="/sys/class/net/"
        for dir in listdir(net_path):
            writefile("{}/{}/device/power/control".format(net_path,dir),"on")

    if get("core",True,"performance"):
        # enable cpu core
        cpus = list_cpu()
        print(cpus)
        for cpu in range(0, len(cpus)):
            change_cpu_status(cpu,True)

    if get("cpufreq",True,"performance"):
        # increase max cpu freq
        cpu_path="/sys/devices/system/cpu/"
        for dir in listdir(cpu_path):
            if not dir.startswith("cpu"):
                continue
            max_freq=readfile("{}/{}/cpufreq/cpuinfo_max_freq".format(cpu_path,dir))
            if max_freq != "":
                writefile("{}/{}/cpufreq/scaling_max_freq".format(cpu_path,dir),max_freq)
