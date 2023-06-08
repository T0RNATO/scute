from scute import command_stack, pack
from os.path import join
import os

def function(function_namespace, function_name):
    def decorator(func):
        func()

        bp = join(os.path.expandvars(pack.path), pack.name)
        bp = join(bp, fr"data\{function_namespace}\functions")

        os.makedirs(bp)

        with open(join(bp, fr"{function_name}.mcfunction"), "w") as f:
           f.writelines(command_stack)
        return func
    return decorator