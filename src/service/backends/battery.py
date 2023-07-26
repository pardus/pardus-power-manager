import gi
from gi.repository import GLib
from util import *
import time


class battery:

    def __init__(self,name):
        self.__last_update = 0
        self.__last_energy = 0
        self.name = name
        self.level = 100
        self.status = "unknown"
        self.health = 100
        self.update()
        path="/sys/class/power_supply/{}/".format(self.name)
        self.real_name = readfile("{}/manufacturer".format(path))
        self.real_name += " " +readfile("{}/model_name".format(path))

    def set_stop_threshold(self,enabled=False):
        path="/sys/class/power_supply/{}/".format(self.name)
        for f in ["charge_control_end_threshold", "charge_stop_threshold"]:
            if os.path.exists(path+f):
                if enabled:
                    writefile(path+f, "80")
                else:
                    writefile(path+f, "100")

    def update(self):
        debug("Update battery information for: {}".format(self.name))
        path="/sys/class/power_supply/{}/".format(self.name)
        # battery level
        if os.path.exists("{}/energy_now".format(path)):
            now= readfile("{}/energy_now".format(path))
            max= readfile("{}/energy_full".format(path))
            self.level = int(now)/int(max) * 100
        elif os.path.exists("{}/capacity".format(path)):
            self.level = int(readfile("{}/capacity".format(path)))
        elif os.path.exists("{}/capacity_level".format(path)):
            level = readfile("{}/capacity_level".format(path)).lower()
            if level == "unknown" or level == "high":
                self.level = 100
            elif level == "normal":
                self.level = 80
            elif level == "low":
                self.level = 40
            elif self.level == "clitical":
                self.level = 20
        else:
            self.level = 100
        # stat us
        if os.path.exists("{}/status".format(path)):
            self.status = readfile("{}/status".format(path)).lower()
        # battery health
        if os.path.exists("{}/energy_full_design".format(path)):
            max= readfile("{}/energy_full".format(path))
            hmax= readfile("{}/energy_full_design".format(path))
            self.health = int(max) * 100 / int(hmax)

