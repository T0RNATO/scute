import atexit
from scute import function_namespaces

# tags = {tag_namespace: [function_namespace, ...]}
tags = {}

def createTagFiles():
    print(tags)


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
