from __future__ import annotations

from os import makedirs
from os.path import join

from scute.blocks import Block
from scute.items import Item
from scute.function import func
from scute.internal_utils.dictToNBT import dictToNBT
from scute import command_stack, pack, function_namespaces
from types import FunctionType
from typing import Callable

from uuid import uuid4

def command(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, str):
            command_stack[-1].append(result + "\n")
        elif isinstance(result, execute):
            command_stack[-1][-1] = result.com + "\n"
        return result

    return wrapper


@command
def give(player, item: Item):
    """
    Gives a player an item
    Parameters:
        player (str): A selector like @a[distance=..5]
        item (Item): The item to give the player, like Item.stone
    """
    com = f"give {player} {item.id}"
    if item.nbt is not None:
        com += dictToNBT(item.nbt)

    if item.count != 1:
        com += " " + str(item.count)

    return com


@command
def setblock(x, y, z, block: Block):
    """
    Places a block at some coordinates
    :param x: X coord of block
    :param y: Y coord of block
    :param z: Z coord of block
    :param block: Block to place
    """
    com = f"setblock {x} {y} {z} {block.id}"
    if block.nbt is not None:
        com += dictToNBT(block.nbt)

    return com


@command
def function(funct: Callable | str):
    """
    Runs another function
    :param funct: A function reference, or a resource location for a function, like mypack:func1
    """
    if isinstance(funct, FunctionType):
        return f"function {function_namespaces[funct]}"
    elif isinstance(funct, str):
        return f"function {funct}"


class execute:
    def __init__(self):
        self.com = "execute"
        command_stack[-1].append(self.com)

    @command
    def at(self, selector):
        """
        Sets the execution position to a entity.
        :param selector: Selector to set position to
        """
        self.com += f" at {selector}"
        return self

    @command
    def as_(self, selector):
        """
        Sets the execution context to a selector. (Note: `as` is reserved in python)
        :param selector: Selector to set context to
        """
        self.com += f" as {selector}"
        return self

    @command
    def anchored(self, pos):
        """
        Sets the execution anchor to the eyes or feet.
        :param pos: "eyes" or "feet" - the anchor to set to.
        """
        self.com += f" anchored {pos}"
        return self

    @command
    def align(self, axes):
        """
        Aligns the current execution position to the grid in the axes provided.
        :param axes: A swizzle of "xyz" - like "x" or "yz"
        """
        self.com += f" align {axes}"
        return self

    @command
    def facing(self, x, y, z):
        """
        Sets the execution context's rotation to look towards a certain point
        :param x: X coord of position to look towards
        :param y: Y coord of position to look towards
        :param z: Z coord of position to look towards
        """
        self.com += f" facing {x} {y} {z}"
        return self

    @command
    def facing_entity(self, selector, anchor):
        """
        Sets the execution context's rotation to look towards an entity
        :param selector: The entity to look towards
        :param anchor: "feet" or "eyes" - the point to look towards
        """
        self.com += f" facing entity {selector} {anchor}"
        return self

    @command
    def in_(self, dimension):
        """
        Sets the execution context's dimension (Note: `in` is reserved in python)
        :param dimension: The resource location of a dimension, like Dimension.overworld
        """
        self.com += f" in {dimension}"
        return self

    @command
    def on(self, relation):
        """
        Sets the executor to an entity based on relation to the current executor entity
        :param relation: A relation like Relation.passengers
        """
        self.com += f" on {relation}"
        return self

    @command
    def positioned(self, x, y, z):
        """
        Sets the execution context to some coordinates
        :param x: The x coordinate to set the position to
        :param y: The y coordinate to set the position to
        :param z: The z coordinate to set the position to
        """
        self.com += f" positioned {x} {y} {z}"
        return self

    @command
    def positioned_as(self, selector):
        """
        Sets the execution context to an entity's position
        :param selector: The entity to set the position to
        """
        self.com += f" positioned as {selector}"
        return self

    @command
    def positioned_over(self, heightmap):
        """
        Sets the execution context to one block above the value of a heightmap at this location
        :param heightmap: The heightmap to use, like Heightmap.world_surface
        """
        self.com += f" positioned over {heightmap}"
        return self

    @command
    def rotated(self, yaw, pitch):
        """
        Sets the execution context's rotation to a certain angle
        :param yaw: The angle around the y-axis - 0 is south, ±180 is north.
        :param pitch: The up-and-down angle - 0 is straight ahead
        """
        self.com += f" rotated {yaw} {pitch}"
        return self

    @command
    def rotated_as(self, selector):
        """
        Sets the execution context's rotation to the same as another entity's
        :param selector: The entity to rotate as
        """
        self.com += f" rotated as {selector}"
        return self

    @command
    def run(self, cmd: str | list | FunctionType):
        """
        Runs a command or function with the current execution context
        :param cmd: The command to run - can be a single command like give(), a list of commands, or a (non-wrapped!) function to run.
        """

        # If the command is a string, meaning the return value from a command
        if isinstance(cmd, str):
            # Add it to the end of the execute command, and remove it from the owner function
            self.com += f" run {cmd}"
            command_stack[-1].pop()

        # Or, if it's a function reference
        elif isinstance(cmd, FunctionType):
            if cmd not in function_namespaces:
                # Generate a name for the function
                name = uuid4()
                self.com += f" run function scute:{name}"
                # Run the function as if it was decorated with @function, generating a file
                command_stack.append([])
                func("scute", name)(cmd)
                # Delete that output
                del command_stack[-1]
            else:
                self.com += f" run function scute:{function_namespaces[cmd]}"

        # Or, if it's a list of commands
        elif isinstance(cmd, list):
            name = uuid4()
            self.com += f" run function scute:{name}"

            # Create a file
            bp = join(pack.path, pack.name)
            bp = join(bp, rf"data\scute\functions")
            makedirs(bp, exist_ok=True)

            function_namespaces[function] = f"scute:{name}"

            with open(join(bp, rf"{name}.mcfunction"), "w") as f:
                # And add the last n values from the command stack to the file, where n is len(cmd)
                f.writelines(command_stack[-1][-len(cmd):])
            # Then remove those values from the stack
            del command_stack[-1][-len(cmd):]

        command_stack[-1].pop()
        return self.com

    class _if_clause:
        def __init__(self, ex):
            self.ex = ex
            ex.com += " if"

        class if_data:
            def __init__(self, ex):
                self.ex = ex
                ex.com += " data"

            @command
            def block(self, x, y, z, path):
                """
                Checks if a certain nbt path exists in a block entity
                :param x: The x position of the block to test
                :param y: The y position of the block to test
                :param z: The z position of the block to test
                :param path: The nbt path, like `Items[{id:"minecraft:diamond"}]`
                """
                self.ex.com += f" block {x} {y} {z} {path}"
                return self.ex

            @command
            def entity(self, selector, path):
                """
                Checks if a certain nbt path exists on an entity
                :param selector: The entity to test
                :param path: The nbt path, like `Invulnerable`
                """
                self.ex.com += f" entity {selector} {path}"
                return self.ex

            @command
            def storage(self, storage, path):
                """
                Checks if a certain nbt path exists in a storage
                :param storage: The resource location of the storage for data testing, like `namespace:storage`
                :param path: The nbt path, like `myTag`
                """
                self.ex.com += f" storage {storage} {path}"
                return self.ex

        @property
        def data(self):
            return execute._if_clause.if_data(self.ex)

        @command
        def biome(self, x: int, y: int, z: int, biome: str):
            """
            Checks if the block at xyz is of a certain biome
            :param x: The x coord of the block
            :param y: The y coord of the block
            :param z: The z coord of the block
            :param biome: The biome to check for, like Biome.beach
            """
            self.ex.com += f" biome {x} {y} {z} {biome}"
            return self.ex

        @command
        def block(self, x, y, z, block: Block):
            """
            Checks if a certain block is at a certain set of coordinates
            :param x: The x position of the block
            :param y: The y position of the block
            :param z: The z position of the block
            :param block: The block, like `Block(Block.dirt)`
            """
            self.ex.com += f" block {x} {y} {z} {block.id}"
            return self.ex

        @command
        def blocks(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, x3: int, y3: int, z3: int, scanmode: str):
            """
            Checks if the blocks in two regions match
            :param x1: The x-coord of the first corner of the first region
            :param y1: The y-coord of the first corner of the first region
            :param z1: The z-coord of the first corner of the first region
            :param x2: The x-coord of the second corner of the first region
            :param y2: The y-coord of the second corner of the first region
            :param z2: The z-coord of the second corner of the first region
            :param x3: The x-coord of the origin of the second region
            :param y3: The y-coord of the origin of the second region
            :param z3: The z-coord of the origin of the second region
            :param scanmode: Whether or not air blocks should also be compared - "all" if yes, "masked" if no
            :return:
            """
            self.ex.com += f" blocks {x1} {y1} {z1} {x2} {y2} {z2} {x3} {y3} {z3} {scanmode}"
            return self.ex

        @command
        def dimension(self, dimension: str):
            """
            Checks if the execution context is in a certain dimension
            :param dimension: The dimension to check for, like Dimension.overworld
            """
            self.ex.com += f" dimension {dimension}"
            return self.ex

        @command
        def entity(self, selector: str):
            """
            Checks if at least one entity matches the selector
            :param selector: A selector
            """
            self.ex.com += f" entity {selector}"
            return self.ex

        @command
        def loaded(self, x: int, y: int, z: int):
            """
            Checks if a certain chunk containing the coordinate is fully loaded
            :param x: The x-coord of a block in the chunk
            :param y: The y-coord of a block in the chunk
            :param z: The z-coord of a block in the chunk
            """
            self.ex.com += f" loaded {x} {y} {z}"
            return self.ex

        @command
        def predicate(self, predicate: str):
            """
            Checks if a predicate is true, with the current execution context
            :param predicate: A resource location of a predicate, like namespace:my_pred
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