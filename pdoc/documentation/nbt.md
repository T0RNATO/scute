## NBT Handling
NBT is used in lots of places, and there's a couple ways to input it.
```python
from scute.items import Item, nbt
from scute.datatypes import Byte

Item(Item.apple, nbt(mytag=Byte(1)))
Item(Item.apple, {"mytag": Byte(1)})
```
There is no functional difference between these two, and they can be used interchangably.

Datatypes of nbt tags from the vanilla game (like CustomModelData) are assumed, meaning you can just pass in an int or a float,
but for your own tags you shold specify a type like `scute.datasources.Byte` or it will be assumed to be an int/float.

Some things have utilities to save you writing nbt, like this:
```python
from scute.items import Item
from scute.jsontext import JSONText, Colour

Item(Item.apple, name=JSONText("my apple", colour=Colour.red))
```
This also allows you to use JSONText() and not write it out yourself.