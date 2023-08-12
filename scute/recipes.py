"""
Submodule for creating and managing recipes - shaped crafting, smelting, etc.
"""
from typing import TypeVar

from scute.internal.utils import _createJsonFile
from scute.tags import ItemTag

class Recipe:
    pass

class ShapedCraftingLayout:
    def __init__(self, row1: str, row2: str, row3: str, key: dict[str, str | ItemTag]):
        """
        A layout for a shaped crafting recipe
        Args:
            row1: A two or three letter string representing the first row of the grid
            row2: A two or three letter string representing the second row of the grid
            row3: A three letter string representing the third row of the grid - can be None for 2x2 grids
            key: A dictionary mapping the letters or symbols used in the rows to the items they represent. e.g. {"a": Item.cobblestone, "b": Item.dirt}
        """
        if row3 is not None:
            self.rows = [row1, row2, row3]
        else:
            self.rows = [row1, row2]
        self.key = key

class RecipeType:
    class blasting(Recipe):
        def __init__(self, input: str | ItemTag, output: str):
            """
            A blasting recipe, with one input and one output that accept no nbt
            Args:
                input: The input item, like Item.cobblestone
                output: The output item
            """
            self.input = input
            self.output = output
            self.json = _singleInOutRecipe("blasting", input, output)

    class campfire_cooking(Recipe):
        def __init__(self, input: str | ItemTag, output: str):
            """
            A campfire cooking recipe, with one input and one output that accept no nbt
            Args:
                input: The input item, like Item.cobblestone
                output: The output item
            """
            self.input = input
            self.output = output
            self.json = _singleInOutRecipe("campfire_cooking", input, output)

    class crafting_shaped(Recipe):
        def __init__(self, layout: ShapedCraftingLayout, output: str, count: int = 1):
            """
            A shaped crafting recipe in a crafting table, with a layout and an output that accept no nbt
            Args:
                layout: The items that need to be placed in the grid, and their locations
                output: The output item of the recipe
            """
            self.layout = layout
            self.output = output

            self.json = {
                "type": "minecraft:crafting_shaped",
                "pattern": layout.rows,
                "key": {
                    i: ({"tag": j.reference} if isinstance(j, ItemTag) else {"item": j})
                    for i, j in layout.key.items()
                },
                "result": {
                    "item": output,
                    "count": count
                }
            }

    class crafting_shapeless(Recipe):
        def __init__(self, ingredients: list[str | ItemTag], output: str, count: int = 1):
            """
            A shapeless crafting recipe in a crafting table, with a list of ingredients and an output that accept no nbt
            Args:
                ingredients: The items that need to be placed in the grid, and their locations
                output: The output item of the recipe
                count: The amount of output items
            """
            self.ingredients = ingredients
            self.output = output

            self.json = {
                "type": "minecraft:crafting_shapeless",
                "ingredients": [
                    {"tag": i.reference} if isinstance(i, ItemTag) else {"item": i}
                    for i in ingredients
                ],
                "result": {
                    "item": output,
                    "count": count
                }
            }

    class smelting(Recipe):
        def __init__(self, input: str | ItemTag, output: str):
            """
            A smelting recipe, with one input and one output that accept no nbt
            Args:
                input: The input item, like Item.cobblestone
                output: The output item
            """
            self.input = input
            self.output = output
            self.json = _singleInOutRecipe("smelting", input, output)

    class smithing(Recipe):
        """Unimplemented"""
        pass

    class smoking(Recipe):
        def __init__(self, input: str | ItemTag, output: str):
            """
            A smoking recipe, with one input and one output that accept no nbt
            Args:
                input: The input item, like Item.cobblestone
                output: The output item
            """
            self.input = input
            self.output = output
            self.json = _singleInOutRecipe("smoking", input, output)

    class stonecutting(Recipe):
        def __init__(self, input: str | ItemTag, output: str, count: int = 1):
            """
            A stonecutting recipe, with one input and an output that accept no nbt
            Args:
                input: The input item, like Item.cobblestone
                output: The output item
                count: The amount of output items
            """
            self.input = input
            self.output = output
            self.count = count
            self.json = _singleInOutRecipe("smoking", input, output, count=count)

def _singleInOutRecipe(id, input, output, count=None):
    out = \
        {
            "type": f"minecraft:{id}",
            "ingredient": {
                "item": input
            },
            "result": output
        }\
        if isinstance(input, str) else\
        {
            "type": f"minecraft:{id}",
            "ingredient": {
                "tag": input.reference
            },
            "result": output
        }
    if count is not None and count != 1:
        out["count"] = count

    return out


_Recipe = TypeVar('_Recipe', bound=Recipe)

def registerRecipe(recipe: _Recipe, namespace: str, name: str):
    _createJsonFile(namespace, name, r"recipes", recipe.json)
    print(f"Successfully registered recipe {namespace}:{name}")
