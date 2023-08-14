import json
import os
from os.path import join

from scute import pack

def _createJsonFile(namespace, name, p, data):
    path = join(pack.path, pack.name)
    path = join(path, rf"data\{namespace}\{p}")

    os.makedirs(path, exist_ok=True)

    with open(join(path, name + ".json"), "w") as f:
        json.dump(data, f, indent=4)

def formatText(text, *codes):
    out = ""
    for code in codes:
        out += f"\033[{code}m"
    out += text
    return out + "\033[0m"
