import os
from file import readfile

def get_device_type():
    chassis_names = [
        "Other",
	"Unknown",
	"Desktop",
	"Low Profile Desktop",
	"Pizza Box",
	"Mini Tower",
	"Tower",
	"Portable",
	"Laptop",
	"Notebook",
	"Hand Held",
	"Docking Station",
	"All in One",
	"Sub Notebook",
	"Space-saving",
	"Lunch Box",
	"Main Server Chassis",
	"Expansion Chassis",
	"SubChassis",
	"Bus Expansion Chassis",
	"Peripheral Chassis",
	"RAID Chassis",
	"Rack Mount Chassis",
	"Sealed-case PC",
	"Multi-system chassis",
	"Compact PCI",
	"Advanced TCA",
	"Blade",
	"Tablet",
	"Convertible",
	"Detachable",
	"IoT Gateway",
	"Embedded PC",
	"Mini PC",
	"Stick PC"
    ]
    type = int(readfile("/sys/devices/virtual/dmi/id/chassis_type"))
    print(chassis_names[type])
    if type < len(chassis_names):
        return chassis_names[type]
    return chassis_names[1]

def is_laptop():
    if os.path.isdir("/proc/pmu"):
        return "Battery" in open("/proc/pmu/info","r").read()
    if os.path.exists("/sys/devices/virtual/dmi/id/chassis_type"):
        type = readfile("/sys/devices/virtual/dmi/id/chassis_type")
        return type in ["8", "9", "10", "11"]
    for dev in os.listdir("/sys/class/power_supply"):
        if "BAT" in dev:
            return True
    if which("dmidecode"):
        chassis_type = subprocess.getoutput("dmidecode --string chassis-type").strip()
        if chassis_type in ["Notebook", "Portable", "Laptop", "Hand Held"]:
            return True
    if os.path.exists("/proc/acpi/battery"):
        return True
    if os.path.isfile("/proc/apm"):
        type = open("/proc/apm","r").read().split(" ")[5]
        return type in ["0xff", "0x80"]
    if os.system("laptop-detect") == 0:
        return True
    return False


def which(command):
    for dir in os.environ["PATH"].split(":"):
        if os.path.isfile("{}/{}".format(dir,command)):
            return "{}/{}".format(dir,command)
    return None

def is_live():
    return "boot=live" in readfile("/proc/cmdline")

def is_virtual_machine():
    cpuinfo = readfile("/proc/cpuinfo").split("\n")
    for line in cpuinfo:
        if line.startswith("flags"):
            return "hypervisor" in line
    return False

def is_chroot():
    return readfile("/proc/1/mountinfo") != readfile("/proc/self/mountinfo")

def is_docker():
    return "docker" in readfile("/proc/1/cgroup")

def is_root():
    return os.getuid() == 0

acpi_support = None
def is_acpi_supported():
    global acpi_support
    if acpi_support == None:
        if is_root():
            with open("/sys/firmware/acpi/tables/DSDT","rb") as f:
                acpi_support = ("linux" in str(f.read()).lower() )
        else:
            acpi_support = False
    return acpi_support

def is_oem_available():
    return os.path.exists("/sys/firmware/acpi/MSDM")
