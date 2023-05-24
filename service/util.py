import os
import sys
import json
import grp
def listen(main):
    if not os.path.exists("/run/ppm"):
        os.mkfifo("/run/ppm")
        os.chmod("/run/ppm", 0o775)
        os.chown("/run/ppm", 0, get_gid_by_name("ppm"))
    while True:
        with open("/run/ppm","r") as f:
            try:
                data = json.loads(f.read())
                if "pid" in data:
                    main(data)
            except Exception as e:
                sys.stderr.write("Json error: {}\n".format(str(e)))
                continue

def get_gid_by_name(name):
    try:
        grpinfo = grp.getgrnam(name)
        return grpinfo.gr_gid
    except:
        return 0

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

def readfile(path):
    if not os.path.exists(path):
        return ""
    with open(path,"r") as f:
        return f.read()
