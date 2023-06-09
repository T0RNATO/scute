from uuid import uuid4

from scute import command_stack, pack, function_namespaces
from os.path import join
import os


def func(function_namespace = None, function_name = None):
    def decorator(function):
        function()
        name = function_name or uuid4()
        space = function_namespace or pack.namespace

        function_namespaces[function] = f"{space}:{name}"

        bp = join(pack.path, pack.name)
        bp = join(bp, rf"data\{space}\functions")

        os.makedirs(bp, exist_ok=True)

        with open(join(bp, rf"{name}.mcfunction"), "w") as f:
            f.writelines(command_stack[-1])
        return function

    return decorator
