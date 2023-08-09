from uuid import uuid4

from scute import command_stack, pack, function_namespaces
from scute.internal_utils.dictToNBT import dictToNBT
from scute.datasources import DataSource
from os.path import join
from inspect import signature
from typing import TypeVar
import os

NbtSource = TypeVar('NbtSource', bound=DataSource)

class MacroArguments:
    def __getattr__(self, item):
        return MacroArg(item)

class MacroArg:
    def __init__(self, item):
        self.item = f"$({item})"

def func(function_namespace=None, function_name=None):
    """
    Creates a function in your datapack. You can provide an optional namespace and name, or it will default to your main namespace and a randomised name.
    Args:
        function_namespace: The namespace your function should go under
        function_name: The name of your function
    """
    def decorator(function):
        sig = signature(function)
        if len(sig.parameters) > 0:
            function(MacroArguments())
        else:
            function()
        name = function_name or uuid4()
        space = function_namespace or pack.namespace

        function_namespaces[function] = f"{space}:{name}"

        bp = join(pack.path, pack.name)
        bp = join(bp, rf"data\{space}\functions")

        os.makedirs(bp, exist_ok=True)

        with open(join(bp, rf"{name}.mcfunction"), "w") as f:
            f.writelines(command_stack[-1])

        command_stack[-1] = []

        def wrapper(args: dict | NbtSource = None, path=None):
            command = f"function {function_namespaces[function]}"
            if isinstance(args, dict):
                command += " " + dictToNBT(args)
                if path is not None:
                    print("Macro argument path does not need to be specified when using hardcoded nbt.")
            elif issubclass(type(args), DataSource):
                if path is None:
                    raise Exception("Macro arguments using external nbt requires a path.")
                else:
                    command += f" with {args.str} {path}"
            command_stack[-1].append(command + "\n")

        wrapper.unwrapped = function

        return wrapper

    return decorator
