from scute.commands import *
from scute.function import func
from scute.blocks import Block
from scute.items import nbt, Item
from scute.tags import ItemTag
from scute.jsontext import JSONText, Colour
from scute.recipes import ShapedCraftingLayout, RecipeType, registerRecipe

pack.setName("myDatapack")
pack.setVersion("1.19.4")
pack.setDescription("A small pack")
pack.setBuildPath(r"./output")

namespace = "my_first_datapack"

pack.setMainNamespace(namespace)

pack.build()

myItem = Item(Item.diamond, name=JSONText("My special diamond", colour=Colour.red))

# A macro function
@func(namespace, "func2")
def my_macro(args):
    give(args.x, Item(Item.diamond))

# Will be assigned a randomly-generated name under the namespace set in pack.setMainNamespace, and added to tick.json
@func()
def my_anonymous_function():
    give("@a", myItem)

@func(namespace, "my_function")
def my_function():
    # my_macro(nbt(x="@s"))
    my_anonymous_function()

    execute().if_.block(1, 2, 3, Block(Block.gold_block)).run([
        give("@s", Item.acacia_boat),
        setblock("~", "~", "~", Block(Block.diamond_block))
    ])


mytag = ItemTag("minecraft:wool")

layout = ShapedCraftingLayout("AAA", "AAA", "BBB", {
    "A": Item.diamond,
    "B": mytag
})

myrecipe = RecipeType.crafting_shaped(layout, Item.dirt)

registerRecipe(myrecipe, namespace, "my_recipe")
