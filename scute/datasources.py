"""
Submodule for data sources, like block entities, entities, and storage - eventually to be used in /data etc
"""
from scute import pack

class DataSource:
    pass

class Storage(DataSource):
    def __init__(self, namespace: str):
        """
        Returns a reference to an nbt storage for passing into /data etc
        Args:
            namespace: The namespace for the storage, like pack:name, or just a name under the default namespace
        """
        if ":" in namespace:
            self.namespace = namespace
        else:
            self.namespace = f"{pack.namespace}:{namespace}"
        self.str = f"storage {self.namespace}"

class BlockData(DataSource):
    def __init__(self, x, y, z):
        """
        Returns a reference to a block entity's data for passing into /data etc
        Args:
            x: The x coordinate of the block
            y: The y coordinate of the block
            z: The z coordinate of the block
        """
        self.x = x
        self.y = y
        self.z = z
        self.str = f"block {x} {y} {z}"

class EntityData(DataSource):
    def __init__(self, selector):
        """
        Returns a reference to an entity's data for passing into /data etc
        Args:
            selector: The selector of the entity
        """
        self.selector = selector
        self.str = f"entity {selector}"
