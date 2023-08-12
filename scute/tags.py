"""
Submodule for creating and managing tags - function tags, block tags, item tags, etc.
"""

import atexit
import json
import os
from os.path import join

from scute import _function_namespaces, pack
from scute.internal.utils import _createJsonFile

_tags = {}

def _createFunctionTagFiles():
    for tag, functions in _tags.items():
        namespace, name = tag.split(":")
        _createJsonFile(namespace, name, r"tags\functions", {
                "values": [
                    func for func in functions
                ]
            })
        print(f"Successfully created function tag {namespace}:{name}")

    print("Built!")


atexit.register(_createFunctionTagFiles)

def _addFuncToTag(func, tag, decoratorName):
    try:
        name = _function_namespaces[func.unwrapped]
        if tag in _tags:
            _tags[tag].append(name)
        else:
            _tags[tag] = [name]
    except:
        raise Exception(f"Please put @{decoratorName} decorators above @func")

def load(func):
    """
    Adds your function to load.json when used as a decorator
    """
    _addFuncToTag(func, "minecraft:load", "load")
    return func

def tick(func):
    """
    Adds your function to tick.json when used as a decorator
    """
    _addFuncToTag(func, "minecraft:tick", "tick")
    return func

def functionTag(namespace, name):
    """
    Adds your function to a function tag of your choosing when used as a decorator
    """
    def decorator(func):
        _addFuncToTag(func, f"{namespace}:{name}", "tag")
        return func
    return decorator

def createBlockTag(namespace: str, name: str, entries: list[str]):
    """
    Creates a block tag with the given entries
    Args:
        namespace: The namespace of the tag
        name: The name of the tag
        entries: The block ids of the tag
    """
    path = join(pack.path, pack.name)
    path = join(path, rf"data\{namespace}\tags\blocks")

    os.makedirs(path, exist_ok=True)

    with open(join(path, rf"{name}.json"), "w") as f:
        json.dump({
            "values": entries
        }, f, indent=4)

class BlockTag:
    def __init__(self, namespaceOrReference: str, name: str = None, entries: list[str] = None):
        """
        Creates or references a block tag. When called with one argument, it references an existing tag. When called with all of them, it creates one with the given entries.
        Args:
            namespaceOrReference: The namespace of the tag to be created or a reference to one, like "minecraft:wool"
            name: The name of the tag
            entries: The block ids of the tag
        """
        if entries is not None:
            path = join(pack.path, pack.name)
            path = join(path, rf"data\{namespaceOrReference}\tags\blocks")

            os.makedirs(path, exist_ok=True)

            with open(join(path, rf"{name}.json"), "w") as f:
                json.dump({
                    "values": entries
                }, f, indent=4)

            self.reference = f"{namespaceOrReference}:{name}"
            return

        self.reference = namespaceOrReference

class ItemTag:
    def __init__(self, namespaceOrReference: str, name: str = None, entries: list[str] = None):
        """
        Creates or references an item tag. When called with one argument, it references an existing tag. When called with all of them, it creates one with the given entries.
        Args:
            namespaceOrReference: The namespace of the tag to be created, like "mypack" or a reference to one, like "minecraft:wool"
            name: The name of the tag
            entries: The block ids of the tag
        """
        if entries:
            _createJsonFile(namespaceOrReference, name, r"tags\items", {
                "values": entries
            })
            self.reference = f"{namespaceOrReference}:{name}"
            return

        self.reference = namespaceOrReference

