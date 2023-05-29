import os
import sys
import json
import threading


def asynchronous(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper


@asynchronous
def listen(main):
    ppm = "/run/user/{}/ppm/{}".format(os.getuid(),os.getpid())
    if not os.path.exists(ppm):
        os.mkdir(ppm)
    ppm = ppm+str(os.getpid())
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


def send_server(data):
    data["pid"] = str(os.getpid())
    if os.path.exists("/run/ppm"):
        with open("/run/ppm", "w") as f:
            f.write(json.dumps(data))

