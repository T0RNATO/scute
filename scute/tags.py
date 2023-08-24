"""
Submodule for creating and managing tags - function tags, block tags, item tags, etc.
"""
import atexit

from scute import _function_namespaces, pack
from scute.internal.utils import create_json_file, format_text

_tags = {}


def _create_function_tag_files():
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
        raise Exception(f"Please put @{decoratorName} decorators above @func")


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
    def __init__(
        self, namespaceOrReference: str, name: str = None, entries: list[str] = None
    ):
        """
        Creates or references a block tag. When called with one argument, it references an existing tag. When called with all of them, it creates one with the given entries.
        Args:
            namespaceOrReference: The namespace of the tag to be created or a reference to one, like "minecraft:wool"
            name: The name of the tag
            entries: The block ids of the tag
        """
        if entries:
            create_json_file(
                namespaceOrReference, name, r"tags\blocks", {"values": entries}
            )
            self.reference = f"{namespaceOrReference}:{name}"
            return

        self.reference = namespaceOrReference


class ItemTag:
    def __init__(
        self, namespaceOrReference: str, name: str = None, entries: list[str] = None
    ):
        """
        Creates or references an item tag. When called with one argument, it references an existing tag. When called with all of them, it creates one with the given entries.
        Args:
            namespaceOrReference: The namespace of the tag to be created, like "mypack" or a reference to one, like "minecraft:wool"
            name: The name of the tag
            entries: The block ids of the tag
        """
        if entries:
            create_json_file(
                namespaceOrReference, name, r"tags\items", {"values": entries}
            )
            self.reference = f"{namespaceOrReference}:{name}"
            return

        self.reference = namespaceOrReference
