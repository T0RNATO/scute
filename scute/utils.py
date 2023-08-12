from uuid import uuid4

from scute.items import Item
from scute.recipes import ShapedCraftingLayout, registerRecipe, RecipeType
from scute import pack


def knowledgeBookCraft(outputItem: Item, recipe: ShapedCraftingLayout, dummyItem: str = "minecraft:knowledge_book"):
    """
    Creates a "crafting recipe" that results in an item with nbt, using the knowledge book trick.
    Args:
        outputItem: The output of the recipe
        recipe: The ingredients and layout of the recipe
        dummyItem: Optional. The item to use instead of the knowledge book.
    """
    rec = RecipeType.crafting_shaped(recipe, dummyItem)
    recipe_name = str(uuid4())
    registerRecipe(rec, pack.namespace, recipe_name)
    # Todo
