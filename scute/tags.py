import atexit
import json
import os
from os.path import join

from scute import function_namespaces, pack

# tags = {tag_namespace: [function_namespace, ...]}
tags = {}

def createTagFiles():
    for tag, functions in tags.items():
        namespace, name = tag.split(":")
        path = join(pack.path, pack.name)
        path = join(path, rf"data\{namespace}\tags\functions")

        os.makedirs(path, exist_ok=True)

        with open(join(path, rf"{name}.json"), "w") as f:
            json.dump({
                "values": [
                    func for func in functions
                ]
            }, f, indent=4)


atexit.register(createTagFiles)

def addFuncToTag(func, tag, decoratorName):
    try:
        name = function_namespaces[func.unwrapped]
        if tag in tags:
            tags[tag].append(name)
        else:
            tags[tag] = [name]
    except:
        raise Exception(f"Please put @{decoratorName} decorators above @func")

def load(func):
    """
    Adds your function to load.json
    """
    addFuncToTag(func, "minecraft:load", "load")
    return func

def tick(func):
    """
    Adds your function to tick.json
    """
    addFuncToTag(func, "minecraft:tick", "tick")
    return func

def tag(namespace, name):
    """
    Adds your function to a function tag of your choosing
    """
    def decorator(func):
        addFuncToTag(func, f"{namespace}:{name}", "tag")
        return func
    return decorator
