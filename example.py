from scute.commands import *
from scute.function import func
from scute.blocks import Block
from scute.items import nbt, Item
from scute.tags import ItemTag, tick
from scute.json_text import JSONText, Colour
from scute.recipes import ShapedCraftingLayout, RecipeType

pack.set_name("myDatapack")
pack.set_version("1.19.4")
pack.set_description("A small pack")
pack.set_build_path(r"./output")

namespace = "my_first_datapack"

pack.set_main_namespace(namespace)

pack.check_valid()

myItem = Item(Item.diamond, name=JSONText("My special diamond", colour=Colour.red))
hi = give("@a", myItem)


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
    my_anonymous_function()

    execute().if_.block(1, 2, 3, Block.gold_block).run(
        [
            give("@s", Item.acacia_boat),
            setblock("~", "~", "~", Block.diamond_block),
        ]
    )
    else_(give("@s", Item.diamond))


mytag = ItemTag("minecraft", "wool")

# layout = ShapedCraftingLayout("AAA", "AAA", "BBB", {"A": Item.diamond, "B": mytag})
#
# myrecipe = RecipeType.crafting_shaped(layout, Item.dirt)
#
# registerRecipe(myrecipe, namespace, "my_recipe")

# sonar.ignore
