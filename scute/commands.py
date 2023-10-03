"""
Submodule containing commands and command-related functions
"""
from functools import wraps

from scute.blocks import Block
from scute.internal.utils import create_function
from scute.items import Item
from scute.function import func, _MacroArg
from scute.internal.dict_to_NBT import dict_to_NBT
from scute.tags import _scute_init
from scute import pack, _function_namespaces
from types import FunctionType
from scute.data_sources import _NbtSource, EntityData, Storage, BlockData
from scute.data_types import _NbtValue

from uuid import uuid4

# A single command, a function reference, or a list of commands
functionArg = str | list | FunctionType


def _functionArgument(
    cmd: functionArg, single_command_allowed: bool, delete: bool = True
):
    result = ""

    # If the command is a string, meaning the return value from a command
    if isinstance(cmd, str):
        if single_command_allowed:
            if delete:
                del pack._command_stack[-1]
            result = cmd
        else:
            cmd = [cmd]

    # Or, if it's a function reference
    elif isinstance(cmd, FunctionType):
        if cmd not in _function_namespaces:
            # Run the function as if it was decorated with @function, generating a file
            func()(cmd)

        result = f"function {pack.namespace}:{_function_namespaces[cmd]}"

    # Or, if it's a list of commands
    if isinstance(cmd, list):
        # Delete the commands that were added to the stack
        if delete:
            del pack._command_stack[-len(cmd) :]

        for i in range(len(cmd)):
            cmd[i] += "\n"

        name = uuid4()
        result = f"function {pack.namespace}:{name}"

        create_function(pack.namespace, name, cmd)

    return result


def _command(funct):
    @wraps(funct)
    def wrapper(*args):
        is_macro: bool = any(isinstance(arg, _MacroArg) for arg in args)
        result = funct(*args)

        if isinstance(result, str):
            command = result + "\n"
            if is_macro:
                command = "$" + command
            pack._command_stack.append(command)

        elif isinstance(result, execute):
            command = result.com + "\n"
            if is_macro:
                command = "$" + command
            # Overwrite command written by previous subcommand with new value
            pack._command_stack[-1] = command

        return result

    return wrapper


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

    com = f"give {player} {item.commandFormat}"

    if item.count != 1:
        com += " " + str(item.count)

    return com


@_command
def run_raw(command: _MacroArg | str):
    """
    Runs a command from a string - useful for macros or unimplemented commands.
    Args:
        command: A string or macro argument
    """
    return command.arg if isinstance(command, _MacroArg) else command


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

    return f"setblock {x} {y} {z} {block.id}{{dict_to_NBT(block.nbt)}}"


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
        cmd: The function or list of commands to run
        time: The time until it's run
        units: "t", "d", or "s", ticks, days, or seconds respectively until the function runs (defaults to ticks)
    """
    return f"schedule function {_functionArgument(cmd, False)} {time}{units}"


class execute:
    def __init__(self):
        self.com = "execute"
        pack._command_stack.append(self.com)

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
            dimension: The resource location of a dimension, like `scute.dimensions.Dimension.overworld`
        """
        self.com += f" in {dimension}"
        return self

    @_command
    def on(self, relation):
        """
        Sets the executor to an entity based on relation to the current executor entity
        Args:
            relation: A relation like `scute.relations.Relation.passengers`
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
            heightmap: The heightmap to use, like `scute.heightmaps.Heightmap.world_surface`
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
        self.com += " run " + _functionArgument(cmd, True)
        del pack._command_stack[-1]
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
                block: The block, like `scute.blocks.Block.dirt`
            """
            self.ex.com += f" block {x} {y} {z} {block.id + dict_to_NBT(block.nbt) if isinstance(block, Block) else block}"
            return self.ex

        @_command
        def blocks(
            self,
            x1: int,
            y1: int,
            z1: int,
            x2: int,
            y2: int,
            z2: int,
            x3: int,
            y3: int,
            z3: int,
            scanmode: str,
        ):
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
            self.ex.com += (
                f" blocks {x1} {y1} {z1} {x2} {y2} {z2} {x3} {y3} {z3} {scanmode}"
            )
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


@_command
def else_(cmd: functionArg):
    """
    Runs a command if the immediately previous `execute if` command did not pass
    Args:
        cmd: The function, command, or list of commands to run
    """
    _scute_init["scoreboard_needed"] = True
    if isinstance(cmd, str):
        del pack._command_stack[-1]

    p = pack._command_stack[-1]
    if "execute" not in p or "run" not in p or "if" not in p:
        raise RuntimeError(
            "else_ must be directly preceded by an `execute ... if ... run` command"
        )

    previous = p.split("run ")
    base: str = previous[0]
    run_command: str = previous[1]

    if run_command.startswith("function"):
        args = run_command.split(" ")
        namespace, name = args[1].split(":")
        # This function will append to an existing file if it already exists (which it does)
        # Sets the score to 1 if the function runs, so that the next command knows if it succeeded
        create_function(
            namespace, name.rstrip(), ["\nscoreboard players set $success scute 1\n"]
        )
        # Make sure that the value isn't 1 due to meddling
        pack._command_stack.insert(-1, "scoreboard players set $success scute 0\n")
    else:
        name = uuid4()
        create_function(
            pack.namespace,
            name,
            [run_command + "\n", "scoreboard players set $success scute 1\n"],
        )
        pack._command_stack[-1] = base + f"run function {pack.namespace}:{name}"
    return (
        f"execute unless score $success scute matches 1 run {_functionArgument(cmd, True, False)}\n"
        "scoreboard players set $success scute 0"
    )


@_command
def data_get(data_source: _NbtSource, path: str = None, scale: float = None):
    """
    Gets NBT data from an entity, block, or storage
    Args:
        data_source: Any child of `scute.datasources.DataSource`, Storage, BlockData, or EntityData
        path: An optional NBT path to get data from
        scale: An optional scale value to multiply the retrieved value by (if it is a number)
    """
    return f"data get {data_source.str} {path} {scale}"


@_command
def data_merge(data_source: _NbtSource, nbt: dict):
    """
    Merges NBT data into an entity, block, or storage
    Args:
        data_source: Any child of `scute.datasources.DataSource`, Storage, BlockData, or EntityData
        nbt: NBT to merge (a dict, or nbt())
    """
    return f"data merge {data_source.str} {dict_to_NBT(nbt)}"


@_command
def data_remove(data_source: _NbtSource, path: str):
    """
    Removes an NBT compound or value from an entity, block, or storage
    Args:
        data_source: Any child of `scute.datasources.DataSource`, Storage, BlockData, or EntityData
        path: The path to the NBT value or compound to remove
    """
    return f"data remove {data_source.str} {path}"


class DataModification:
    append = "append "
    """Append the source data or direct value data onto the end of the pointed-to list."""
    prepend = "prepend "
    """Prepend the source data or direct value data onto the beginning of the pointed-to list."""
    merge = "merge "
    """Merge the source data or direct value data into the pointed-to object."""
    set = "set "
    """Set the specified tag to a data value."""

    @staticmethod
    def insert(i) -> str:
        """
        Insert the value into the pointed-to list as element `i`, then shift higher elements one position upward.
        Args:
            i: The index of the inserted element
        """
        return f"insert {i} "


@_command
def data_modify_from(
    target: _NbtSource,
    path: str,
    modification: str,
    source: _NbtSource,
    source_path: str = None,
):
    """
    Copies source nbt using an operation to the target
    Args:
        target: The nbt being modified
        path: The nbt path of the source being modified
        modification: The modification, like "set" or `scute.commands.DataModification.set`
        source: The source which nbt is being copied from
        source_path: Optional path for source
    """
    return f"data modify {target.str} {path} {modification} from {source.str} {source_path}"


@_command
def data_modify_string(
    target: _NbtSource,
    path: str,
    modification: str,
    source: _NbtSource,
    source_path: str = None,
    start: int = None,
    end: int = None,
):
    """
    Copies a string or a section of a string using an operation from the source to the target
    Args:
        target: The nbt being modified
        path: The nbt path of the source being modified
        modification: The modification, like "set" or `scute.commands.DataModification.set`
        source: The source which nbt is being copied from
        source_path: Optional path for source
        start: Optional index of first character to include at the start of the string. Negative values are counted from the end of the string.
        end: Optional index of the first character to exclude at the end of the string. Negative values are counted from the end of the string.
    """
    return f"data modify {target.str} {path} {modification} string {source.str} {source_path} {start} {end}"


@_command
def data_modify_value(
    target: _NbtSource, path: str, modification: str, value: _NbtValue
):
    """
    Uses an operation to modify the target with a fixed value
    Args:
        target: The nbt being modified
        path: The nbt path of the source being modified
        modification: The modification, like "set" or `scute.commands.DataModification.set`
        value: The nbt value used, like Byte(1) or "hello" or an nbt compound
    """
    val = value
    if isinstance(value, dict):
        val = dict_to_NBT(value)
    return f"data modify {target.str} {path} {modification} value {val}"
