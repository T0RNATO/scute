from scute import pack
from scute.commands import *
from scute.datatypes import Byte
from scute.enchantments import Enchantment
from scute.function import function
from scute.gen.blocks import Block
from scute.items import nbt, Item

pack.setName("myDatapack")
pack.setVersion("1.19.4")
pack.setDescription("A small pack")
pack.setBuildPath(r"./output")

pack.build()

namespace = "myFirstDatapack"


@function(namespace, "myFunction")
def my_function():
    give(
        "@s",
        Item(
            Item.stone,
            count=5,
            nbt=nbt(
                # Data type of default tags is assumed
                CustomModelData=3,
                Enchantments=[nbt(id=Enchantment.mending, lvl=1)],
                # Custom tags must be assigned a data type - defaults to int if not specified
                myCustomTag=Byte(3),
            ),
        ),
    )

    setblock(69, 33, -100, Block(Block.stone))
