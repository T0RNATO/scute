from scute import command_stack, pack
from os.path import join
import os


def function(function_namespace, function_name):
    def decorator(func):
        func()

        bp = join(pack.path, pack.name)
        bp = join(bp, rf"data\{function_namespace}\functions")

        os.makedirs(bp)

        with open(join(bp, rf"{function_name}.mcfunction"), "w") as f:
            f.writelines(command_stack[-1])
        return func

    return decorator
