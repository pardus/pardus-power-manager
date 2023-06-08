import os
import sys
import json
sys.path.insert(0, os.path.dirname( os.path.realpath(__file__) )+"/../common")
from common import *

def listen(main):
    if not os.path.exists("/run/ppm"):
        os.mkfifo("/run/ppm")
        os.chmod("/run/ppm", 0o777)
        os.chown("/run/ppm", 0, 0)
        os.system("chattr -R -a /run/ppm")
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



def send_client(data):
    data["pid"] = str(os.getpid())
    for dir in listdir("/run/user"):
        if os.path.exists("/run/user/{}/ppm/".format(dir)):
            for fifo in listdir("/run/user/{}/ppm/".format(dir)):
                debug("Send data to client: {} {}".format(dir, fifo))
                if not os.path.isdir("/proc/{}".format(fifo)):
                    os.unlink("/run/user/{}/ppm/{}".format(dir,fifo))
                else:
                    with open("/run/user/{}/ppm/{}".format(dir,fifo), "w") as f:
                        f.write(json.dumps(data))
                        f.flush()
