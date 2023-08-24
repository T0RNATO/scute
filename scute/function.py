from uuid import uuid4

from scute import pack, _function_namespaces
from scute.internal.dict_to_NBT import dict_to_NBT
from scute.datasources import DataSource
from os.path import join
from inspect import signature
from typing import TypeVar
import os

from scute.internal.utils import format_text, create_function

_NbtSource = TypeVar("_NbtSource", bound=DataSource)


class _MacroArguments:
    """
    The class instance passed to a function that has been declared with arguments (a macro). Accessing any property will return a `_MacroArg` instance which can be passed into any command
    """

    def __getattr__(self, item):
        return _MacroArg(item)


class _MacroArg:
    def __init__(self, item):
        """
        An internal class returned from `_MacroArguments` which can be passed into any command
        """
        self.arg: str = f"$({item})"

    def __str__(self):
        return self.arg


def func(function_namespace=None, function_name=None):
    """
    A decorator that creates a function in your datapack. You can provide an optional namespace and name,
    or it will default to your main namespace and a randomised name.
    Args:
        function_namespace: The namespace your function should go under
        function_name: The name of your function

    .. include:: ../pdoc/documentation/functions.md
    """

    def decorator(function):
        if function not in _function_namespaces:
            sig = signature(function)
            if len(sig.parameters) > 0:
                function(_MacroArguments())
            else:
                function()
            name = function_name or uuid4()
            space = function_namespace or pack.namespace

            _function_namespaces[function] = f"{space}:{name}"

            create_function(space, name, pack._command_stack)

            pack._command_stack = []

            print(format_text(f"Created function {space}:{name}", 32))

        # Code run if the function is called
        def wrapper(args: dict | _NbtSource = None, path=None):
            command = f"function {_function_namespaces[function]}"
            if isinstance(args, dict):
                command += " " + dict_to_NBT(args)
                if path is not None:
                    print(
                        "Warning: Macro argument path should not be specified when using hardcoded nbt."
                    )
            elif issubclass(type(args), DataSource):
                command += f" with {args.str} {path}"
            pack._command_stack.append(command + "\n")

        wrapper.unwrapped = function

        return wrapper

    return decorator
