import os
import sys
import json
def listen(main):
    if not os.path.exists("/run/ppm"):
        os.mkfifo("/run/ppm")
    while True:
        with open("/run/ppm","r") as f:
            try:
                data = json.loads(f.read())
                main(data)
            except Exception as e:
                sys.stderr.write("Json error: {}\n".format(str(e)))
                continue

def send_client(data):
    data["pid"] = str(os.getpid())
    for dir in os.listdir("/run/user"):
        if os.path.exists("/run/user/{}/ppm".format(dir)):
            with open("/run/user/{}/ppm".format(dir), "w") as f:
                f.write(json.dumps(data))

def writefile(path,data):
    try:
        with open(path,"w") as f:
            f.write(str(data))
            f.flush()
    except:
        return False
    return True
