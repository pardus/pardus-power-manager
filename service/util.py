import os
import sys
import json
import grp
import time

from config import *

start_time = time.time()

def listen(main):
    if not os.path.exists("/run/ppm"):
        os.mkfifo("/run/ppm")
        os.chmod("/run/ppm", 0o775)
        os.chown("/run/ppm", 0, get_gid_by_name("ppm"))
    while True:
        with open("/run/ppm","r") as f:
            try:
                data = f.read()
                if len(data.strip()) == 0:
                    continue
                debug(data)
                data = json.loads(data)
            except Exception as e:
                log("Json error: {}\n{}".format(str(e),str(f.read()) ))
                continue
        if "pid" in data:
            main(data)

def get_gid_by_name(name):
    try:
        grpinfo = grp.getgrnam(name)
        return grpinfo.gr_gid
    except:
        return 0

def send_client(data):
    data["pid"] = str(os.getpid())
    for dir in os.listdir("/run/user"):
        if os.path.exists("/run/user/{}/ppm/".format(dir)):
            for fifo in os.listdir("/run/user/{}/ppm/".format(dir)):
                debug("Send data to client: {} {}".format(dir, fifo))
                if not os.path.isdir("/proc/{}".format(fifo)):
                    os.unlink("/run/user/{}/ppm/{}".format(dir,fifo))
                else:
                    with open("/run/user/{}/ppm/{}".format(dir,fifo), "w") as f:
                        f.write(json.dumps(data))
                        f.flush()

def writefile(path,data):
    debug("Write file: "+ path)
    try:
        with open(path,"w") as f:
            f.write(str(data))
            f.flush()
    except:
        return False
    return True

def readfile(path):
    debug("Read file: "+ path)
    if not os.path.exists(path):
        return ""
    try:
        with open(path,"r") as f:
            return f.read()
    except Exception as e:
        print(e)
        return ""


logfile = open("/var/log/ppm.log","a")

def log(msg):
    ftime = time.time() - start_time
    ftime = float(int(10000*ftime))/10000
    logfile.write("[{}]: {}\n".format(ftime, msg))
    logfile.flush()

if get("debug",False):
    debug = log
else:
    def debug(msg):
        return

def listdir(path):
    if os.path.isdir(path):
        return os.listdir(path)
    return []
