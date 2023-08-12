import json
import os
from os.path import join

from scute import pack

def _createJsonFile(namespace, name, p, data):
    path = join(pack.path, pack.name)
    path = join(path, rf"data\{namespace}\{p}")

    os.makedirs(path, exist_ok=True)

    print(path)

    with open(join(path, name + ".json"), "w") as f:
        json.dump(data, f, indent=4)
