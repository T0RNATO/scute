"""
Submodule for creating and managing tags - function tags, block tags, item tags, etc.
"""
import atexit

from scute import _function_namespaces, pack
from scute.internal.utils import create_json_file, format_text, create_function

# Dict of function tags, {"namespace:mytag": ["namespace:function", ...]}
_tags = {}
_scute_init = {"commands": [], "scoreboard_needed": False}


def _create_function_tag_files():
    if _scute_init["commands"]:
        namespace = pack.namespace + ":scute_init"

        if "minecraft:load" in _tags:
            _tags["minecraft:load"].append(namespace)
        else:
            _tags["minecraft:load"] = [namespace]

        if _scute_init["scoreboard_needed"]:
            _scute_init["commands"].append("scoreboard objectives add scute dummy")

        create_function(pack.namespace, "scute_init", _scute_init["commands"])

    for tag, functions in _tags.items():
        namespace, name = tag.split(":")
        create_json_file(
            namespace, name, r"tags\functions", {"values": [func for func in functions]}
        )
        print(format_text(f"Successfully created function tag {namespace}:{name}", 32))

    print(format_text("Built!", 42, 30))


atexit.register(_create_function_tag_files)


def _add_func_to_tag(func, tag, decoratorName):
    try:
        name = _function_namespaces[func.unwrapped]
        if tag in _tags:
            _tags[tag].append(name)
        else:
            _tags[tag] = [name]
    except KeyError:
        raise RuntimeError(f"@{decoratorName} decorators must be put above @func")


def load(func):
    """
    Adds your function to load.json when used as a decorator
    """
    _add_func_to_tag(func, "minecraft:load", "load")
    return func


def tick(func):
    """
    Adds your function to tick.json when used as a decorator
    """
    _add_func_to_tag(func, "minecraft:tick", "tick")
    return func


def functionTag(namespace, name):
    """
    Adds your function to a function tag of your choosing when used as a decorator
    """

    def decorator(func):
        _add_func_to_tag(func, f"{namespace}:{name}", "tag")
        return func

    return decorator


class BlockTag:
    def __init__(self, namespace: str, name: str, entries: list[str] = None):
        """
        Creates or references a block tag. When called with two arguments, it references an existing tag. When called with three, it creates one with the given entries.
        Args:
            namespace: The namespace of the tag being created or referenced
            name: The name of the tag
            entries: The item ids of the tag if it's being created
        """
        self.reference = f"{namespace}:{name}"
        if entries:
            create_json_file(namespace, name, r"tags\blocks", {"values": entries})


class ItemTag:
    def __init__(self, namespace: str, name: str, entries: list[str] = None):
        """
        Creates or references an item tag. When called with two arguments, it references an existing tag. When called with three, it creates one with the given entries.
        Args:
            namespace: The namespace of the tag being created or referenced
            name: The name of the tag
            entries: The item ids of the tag if it's being created
        """
        self.reference = f"{namespace}:{name}"
        if entries:
            create_json_file(namespace, name, r"tags\items", {"values": entries})
