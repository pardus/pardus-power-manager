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

def get(variable, default=None, section="pardus"):
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