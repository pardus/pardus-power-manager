from util import send_client
from power import *
def main(data):
    print(data)
    if "new-mode" in data:
        set_mode(data["new-mode"])
    send_client(data)
