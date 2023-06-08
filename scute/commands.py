from scute.gen.blocks import Block
from scute.items import Item
from scute.internal_utils.dictToNBT import dictToNBT

command_stack = []

def command(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, str):
            command_stack.append(result)
        elif isinstance(result, execute):
            command_stack[-1] = result.com
        return result
    return wrapper

@command
def give(player, item : Item):
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

class execute:
    def __init__(self):
        self.com = "execute"
        command_stack.append(self.com)

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