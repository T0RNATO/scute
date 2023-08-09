# from scute import pack
from scute.commands import *
from scute.function import func
from scute.blocks import Block
from scute.items import nbt, Item
from scute.datasources import Storage
from scute.tags import load, tag, tick

pack.setName("myDatapack")
pack.setVersion("1.19.4")
pack.setDescription("A small pack")
pack.setBuildPath(r"./output")

namespace = "myFirstDatapack"

pack.setMainNamespace(namespace)

pack.build()

myStorage = Storage("myData")

# A macro function
@func(namespace, "func2")
def my_macro(args):
    give(args.x, Item(Item.diamond))

# Will be assigned a randomly-generated name under the namespace set in pack.setMainNamespace, and added to tick.json
@tick
@func()
def my_anonymous_function():
    give("@a", Item(Item.apple))

@func(namespace, "myFunction")
def my_function():
    my_macro(nbt(x="@s"))
    my_macro(myStorage, "optional.path.to.my.data")
    my_anonymous_function()

    execute().if_.block(1, 2, 3, Block(Block.gold_block)).run([
        give("@s", Item(Item.acacia_boat)),
        setblock("~", "~", "~", Block(Block.diamond_block))
    ])
