## Usage
Define a function, and wrap it with @func().
```python
from scute.function import func
from scute.commands import give
from scute.items import Item

@func()
def myFunction():
    give("@s", Item.egg)
```
This function will be created with a uuid as its name, under the namespace specified in `scute.pack.setMainNamespace`

Alternatively, specify a namespace and function name.
```python
@func("my_datapack", "function1")
def myFunction():
    give("@s", Item.egg)
```

To reference this function from other functions in your project, call it like you would any other function.
```python
@func()
def myOtherFunction():
    myFunction()
```

## Macros
To define a macro function (1.20.2+), give your function an argument. This represents the nbt compound that is passed in.
```python
@func()
def myFunction(args):
    give("@s", args.item)
```

To call this function, just pass in some arguments.

```python
from scute.items import nbt, Item
from scute.data_sources import Storage

myStorage = Storage("my_namespace")


@func()
def myOtherFunction():
    myFunction(nbt(item="minecraft:egg"))
    # or
    myFunction({"item": "minecraft:egg"})
    # or
    myFunction(nbt(item=Item.egg))
    # or
    myFunction(myStorage)
    # or
    myFunction(myStorage, "path.to.the.compound.i.want.to.use")
```
