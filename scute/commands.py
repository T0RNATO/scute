"""
Submodule containing commands and command-related functions
"""
from os import makedirs
from os.path import join

from scute.blocks import Block
from scute.items import Item
from scute.function import func, _MacroArg
from scute.internal.dictToNBT import dictToNBT
from scute import _command_stack, pack, _function_namespaces
from types import FunctionType

from uuid import uuid4
from functools import wraps

functionArg = str | list | FunctionType


def _command(funct):
    @wraps(funct)
    def wrapper(*args):
        # TODO: pass macro args to commands somehow as strings/obj when needed
        macro = any(isinstance(arg, _MacroArg) for arg in args)
        result = funct(*args)
        if isinstance(result, str):
            c = result + "\n"
            if macro:
                c = "$" + c
            _command_stack[-1].append(c)
        elif isinstance(result, execute):
            c = result.com + "\n"
            if macro:
                c = "$" + c
            _command_stack[-1][-1] = c
        return result

    return wrapper


def _functionArgument(cmd: functionArg, single_command_allowed: bool):
    _command_stack.append([])

    result = "" if single_command_allowed else "function "

    # If the command is a string, meaning the return value from a command
    if isinstance(cmd, str):
        result = cmd

    # Or, if it's a function reference
    elif isinstance(cmd, FunctionType):
        if cmd not in _function_namespaces:
            # Run the function as if it was decorated with @function, generating a file
            func()(cmd)

        result = f"function {pack.namespace}:{_function_namespaces[cmd]}"

    # Or, if it's a list of commands
    elif isinstance(cmd, list):
        name = uuid4()

        result = f"function {pack.namespace}:{name}"

        # Create a file
        bp = join(pack.path, pack.name)
        bp = join(bp, rf"data\{pack.namespace}\functions")
        makedirs(bp, exist_ok=True)

        _function_namespaces[function] = f"{pack.namespace}:{name}"

        with open(join(bp, rf"{name}.mcfunction"), "w") as f:
            # Write the commands to the file
            f.writelines(_command_stack[-1])

    del _command_stack[-1]

    return result


@_command
def give(player, item: Item | str):
    """
    Gives a player an item
    Args:
        player: A selector like @a[distance=..5]
        item: The item to give the player, - an instance of the Item() class or a string id like Item.egg
    """
    if isinstance(item, _MacroArg):
        return f"give {player} {item.arg}"
    elif isinstance(item, str):
        return f"give {player} {item}"

    com = f"give {player} {item.id}"
    if item.nbt is not None:
        com += dictToNBT(item.nbt)

    if item.count != 1:
        com += " " + str(item.count)

    return com


@_command
def setblock(x, y, z, block: Block | str):
    """
    Places a block at some coordinates
    Args:
        x: X coord of block
        y: Y coord of block
        z: Z coord of block
        block: Block to place
    """
    if isinstance(block, _MacroArg):
        return f"setblock {x} {y} {z} {block.arg}"
    elif isinstance(block, str):
        return f"setblock {x} {y} {z} {block}"

    com = f"setblock {x} {y} {z} {block.id}"
    if block.nbt is not None:
        com += dictToNBT(block.nbt)

    return com


@_command
def function(funct: str):
    """
    Calls another function from another pack. To call your own function, just call it like myFunc()
    Args:
        funct: A resource location for a function, like mypack:func1
    """
    return f"function {funct}"


@_command
def schedule(cmd: functionArg, time: int, units: str = "t"):
    """
    Schedules a function to run at a point in the future
    Args:
        cmd: The function, command, or list of commands to run
        time: The time until it's run
        units: "t", "d", or "s", ticks, days, or seconds respectively until the function runs (defaults to ticks)
    """
    return f"schedule function {_functionArgument(cmd, False)} {time}{units}"


class execute:
    def __init__(self):
        self.com = "execute"
        _command_stack[-1].append(self.com)

    @_command
    def at(self, selector):
        """
        Sets the execution position to a entity.
        Args:
            selector: Selector to set position to
        """
        self.com += f" at {selector}"
        return self

    @_command
    def as_(self, selector):
        """
        Sets the execution context to a selector. (Note: `as` is reserved in python)
        Args:
            selector: Selector to set context to
        """
        self.com += f" as {selector}"
        return self

    @_command
    def anchored(self, pos):
        """
        Sets the execution anchor to the eyes or feet.
        Args:
            pos: "eyes" or "feet" - the anchor to set to.
        """
        self.com += f" anchored {pos}"
        return self

    @_command
    def align(self, axes):
        """
        Aligns the current execution position to the grid in the axes provided.
        Args:
            axes: A swizzle of "xyz" - like "x" or "yz"
        """
        self.com += f" align {axes}"
        return self

    @_command
    def facing(self, x, y, z):
        """
        Sets the execution context's rotation to look towards a certain point
        Args:
            x: X coord of position to look towards
            y: Y coord of position to look towards
            z: Z coord of position to look towards
        """
        self.com += f" facing {x} {y} {z}"
        return self

    @_command
    def facing_entity(self, selector, anchor):
        """
        Sets the execution context's rotation to look towards an entity
        Args:
            selector: The entity to look towards
            anchor: "feet" or "eyes" - the point to look towards
        """
        self.com += f" facing entity {selector} {anchor}"
        return self

    @_command
    def in_(self, dimension):
        """
        Sets the execution context's dimension (Note: `in` is reserved in python)
        Args:
            dimension: The resource location of a dimension, like Dimension.overworld
        """
        self.com += f" in {dimension}"
        return self

    @_command
    def on(self, relation):
        """
        Sets the executor to an entity based on relation to the current executor entity
        Args:
            relation: A relation like Relation.passengers
        """
        self.com += f" on {relation}"
        return self

    @_command
    def positioned(self, x, y, z):
        """
        Sets the execution context to some coordinates
        Args:
            x: The x coordinate to set the position to
            y: The y coordinate to set the position to
            z: The z coordinate to set the position to
        """
        self.com += f" positioned {x} {y} {z}"
        return self

    @_command
    def positioned_as(self, selector):
        """
        Sets the execution context to an entity's position
        Args:
            selector: The entity to set the position to
        """
        self.com += f" positioned as {selector}"
        return self

    @_command
    def positioned_over(self, heightmap):
        """
        Sets the execution context to one block above the value of a heightmap at this location
        Args:
            heightmap: The heightmap to use, like Heightmap.world_surface
        """
        self.com += f" positioned over {heightmap}"
        return self

    @_command
    def rotated(self, yaw, pitch):
        """
        Sets the execution context's rotation to a certain angle
        Args:
            yaw: The angle around the y-axis - 0 is south, ±180 is north.
            pitch: The up-and-down angle - 0 is straight ahead
        """
        self.com += f" rotated {yaw} {pitch}"
        return self

    @_command
    def rotated_as(self, selector):
        """
        Sets the execution context's rotation to the same as another entity's
        Args:
            selector: The entity to rotate as
        """
        self.com += f" rotated as {selector}"
        return self

    @_command
    def run(self, cmd: functionArg):
        """
        Runs a command or function with the current execution context
        Args:
            cmd: The command to run - can be a single command like give(), a list of commands, or a (non-wrapped!) function to run.
        """
        self.com += " run "
        self.com += _functionArgument(cmd, True)
        return self.com

    class _if_clause:
        def __init__(self, ex):
            self.ex = ex
            ex.com += " if"

        class _if_data:
            def __init__(self, ex):
                self.ex = ex
                ex.com += " data"

            @_command
            def block(self, x, y, z, path):
                """
                Checks if a certain nbt path exists in a block entity
                Args:
                    x: The x position of the block to test
                    y: The y position of the block to test
                    z: The z position of the block to test
                    path: The nbt path, like `Items[{id:"minecraft:diamond"}]`
                """
                self.ex.com += f" block {x} {y} {z} {path}"
                return self.ex

            @_command
            def entity(self, selector, path):
                """
                Checks if a certain nbt path exists on an entity
                Args:
                    selector: The entity to test
                    path: The nbt path, like `Invulnerable`
                """
                self.ex.com += f" entity {selector} {path}"
                return self.ex

            @_command
            def storage(self, storage, path):
                """
                Checks if a certain nbt path exists in a storage
                Args:
                    storage: The resource location of the storage for data testing, like `namespace:storage`
                    path: The nbt path, like `myTag`
                """
                self.ex.com += f" storage {storage} {path}"
                return self.ex

        @property
        def data(self):
            return execute._if_clause._if_data(self.ex)

        @_command
        def biome(self, x: int, y: int, z: int, biome: str):
            """
            Checks if the block at xyz is of a certain biome
            Args:
                x: The x coord of the block
                y: The y coord of the block
                z: The z coord of the block
                biome: The biome to check for, like Biome.beach
            """
            self.ex.com += f" biome {x} {y} {z} {biome}"
            return self.ex

        @_command
        def block(self, x, y, z, block: Block):
            """
            Checks if a certain block is at a certain set of coordinates
            Args:
                x: The x position of the block
                y: The y position of the block
                z: The z position of the block
                block: The block, like `Block(Block.dirt)`
            """
            self.ex.com += f" block {x} {y} {z} {block.id}"
            return self.ex

        @_command
        def blocks(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, x3: int, y3: int, z3: int,
                   scanmode: str):
            """
            Checks if the blocks in two regions match
            Args:
                x1: The x-coord of the first corner of the first region
                y1: The y-coord of the first corner of the first region
                z1: The z-coord of the first corner of the first region
                x2: The x-coord of the second corner of the first region
                y2: The y-coord of the second corner of the first region
                z2: The z-coord of the second corner of the first region
                x3: The x-coord of the origin of the second region
                y3: The y-coord of the origin of the second region
                z3: The z-coord of the origin of the second region
                scanmode: Whether air blocks should also be compared - "all" if yes, "masked" if no
            :return:
            """
            self.ex.com += f" blocks {x1} {y1} {z1} {x2} {y2} {z2} {x3} {y3} {z3} {scanmode}"
            return self.ex

        @_command
        def dimension(self, dimension: str):
            """
            Checks if the execution context is in a certain dimension
            Args:
                dimension: The dimension to check for, like Dimension.overworld
            """
            self.ex.com += f" dimension {dimension}"
            return self.ex

        @_command
        def entity(self, selector: str):
            """
            Checks if at least one entity matches the selector
            Args:
                selector: A selector
            """
            self.ex.com += f" entity {selector}"
            return self.ex

        @_command
        def loaded(self, x: int, y: int, z: int):
            """
            Checks if a certain chunk containing the coordinate is fully loaded
            Args:
                x: The x-coord of a block in the chunk
                y: The y-coord of a block in the chunk
                z: The z-coord of a block in the chunk
            """
            self.ex.com += f" loaded {x} {y} {z}"
            return self.ex

        @_command
        def predicate(self, predicate: str):
            """
            Checks if a predicate is true, with the current execution context
            Args:
                 predicate: A resource location of a predicate, like namespace:my_pred
            """
            self.ex.com += f" predicate {predicate}"
            return self.ex

    class _unless_clause(_if_clause):
        def __init__(self, ex):
            self.ex = ex
            ex.com += " unless"

    @property
    def if_(self):
        return execute._if_clause(self)

    @property
    def unless(self):
        return execute._unless_clause(self)
