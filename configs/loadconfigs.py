import json
import os


def read_config():
    with open(f"{os.getcwd()}/configs/config.json", "r") as f:
        return json.load(f)
