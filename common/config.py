import os
import configparser
try:
    cfgs = ["/etc/pardus/ppm.conf"]
    if os.path.isdir("/etc/pardus/ppm.conf.d"):
        for cdir in os.listdir("/etc/pardus/ppm.conf.d/"):
            cfgs.append("/etc/pardus/ppm.conf.d/"+cdir)

    config = configparser.RawConfigParser()
    config.read(cfgs)
except Exception as e:
    print(str(e))
    config = []

cmdargs = {}
with open("/proc/cmdline") as f:
    for word in f.read().split(" "):
        if word.startswith("ppm.") and "=" in word:
            v = variable.split(".")
            if len(v) >= 3:
                variable = v[0]
                value = v[1]
                sec = [1]
                var = v[2]
                if sec not in cmdargs:
                    cmdargs[sec] = {}
                cmdargs[sec][var] = value

print(cmdargs)

def get(variable, default=None, section="pardus"):
    ret = default
    if section in cmdargs:
        if variable in cmdargs[section]:
            ret = cmdargs[section][variable]
    else:
        if section not in config:
            return default
        if variable not in config[section]:
            return default
        ret = config[section][variable]
    if default == True or default == False:
        if str(ret).lower() == "true":
            return True
        else:
            return False
    return str(ret)
