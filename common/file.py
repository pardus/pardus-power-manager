import os
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
    try:
        with open(path,"r") as f:
            return f.read().strip()
    except Exception as e:
        print(e)
        return ""

def listdir(path):
    if os.path.isdir(path):
        return os.listdir(path)
    return []


def singleinstance():
    try:
        import socket
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind('\0ppm_notify_lock')
    except socket.error as e:
        sys.exit (0)
