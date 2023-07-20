import os
import sys
import json
sys.path.insert(0, os.path.dirname( os.path.realpath(__file__) )+"/../common")
from common import *

@asynchronous
def listen(main):
    ppm = "/run/user/{}/ppm".format(os.getuid())
    if not os.path.exists(ppm):
        os.makedirs(ppm)
    ppm = ppm+"/"+str(os.getpid())
    if not os.path.exists(ppm):
        os.mkfifo(ppm)
    while True:
        with open(ppm,"r") as f:
            try:
                data = json.loads(f.read())
                main.update(data)
            except Exception as e:
                sys.stderr.write("Json error: {}\n".format(str(e)))
                continue

last_data = None
@asynchronous
def send_server(data={}):
    global last_data
    if last_data == data and last_data != None:
        return
    last_data = data
    print(data)
    try:
        data["pid"] = str(os.getpid())
        if os.path.exists("/run/ppm"):
            with open("/run/ppm", "w") as f:
                f.write(json.dumps(data))
    except Exception as e:
        print(str(e))

