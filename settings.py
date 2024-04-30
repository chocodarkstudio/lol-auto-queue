from __future__ import annotations
import json

class Resolutions:
    availible_res = ["1366x768"]
    img_path = "imgs_" + availible_res[0]

class Config:
    global DATA
    DATA = None

    @staticmethod
    def load(path="config.json"):
        global DATA
        print("loading data")

        file = open(path, "r")
        DATA = json.loads(file.read())
        file.close()
    
    @staticmethod
    def get(key: str):
        global DATA

        # no loaded data
        if DATA is None:
            raise(BaseException("No loaded data"))

        return DATA[key]

Config.load()