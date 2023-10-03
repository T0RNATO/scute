class Advancement:
    def add_condition(self, condition):
        pass


class AdvancementCriteria:
    class allay_drop_item_on_block(Advancement):
        def __init__(self):
            self.type = "allay_drop_item_on_block"

    class avoid_vibration(Advancement):
        def __init__(self):
            self.type = "avoid_vibration"

    class bee_nest_destroyed(Advancement):
        def __init__(self):
            self.type = "bee_nest_destroyed"

    class bred_animals(Advancement):
        def __init__(self):
            self.type = "bred_animals"

    class brewed_potion(Advancement):
        def __init__(self):
            self.type = "brewed_potion"

    class changed_dimension(Advancement):
        def __init__(self):
            self.type = "changed_dimension"

    class channeled_lightning(Advancement):
        def __init__(self):
            self.type = "channeled_lightning"

    class construct_beacon(Advancement):
        def __init__(self):
            self.type = "construct_beacon"

    class consume_item(Advancement):
        def __init__(self):
            self.type = "consume_item"

    class cured_zombie_villager(Advancement):
        def __init__(self):
            self.type = "cured_zombie_villager"

    class effects_changed(Advancement):
        def __init__(self):
            self.type = "effects_changed"

    class enchanted_item(Advancement):
        def __init__(self):
            self.type = "enchanted_item"

    class enter_block(Advancement):
        def __init__(self):
            self.type = "enter_block"

    class entity_hurt_player(Advancement):
        def __init__(self):
            self.type = "entity_hurt_player"

    class entity_killed_player(Advancement):
        def __init__(self):
            self.type = "entity_killed_player"

    class fall_from_height(Advancement):
        def __init__(self):
            self.type = "fall_from_height"

    class filled_bucket(Advancement):
        def __init__(self):
            self.type = "filled_bucket"

    class fishing_rod_hooked(Advancement):
        def __init__(self):
            self.type = "fishing_rod_hooked"

    class hero_of_the_village(Advancement):
        def __init__(self):
            self.type = "hero_of_the_village"

    class impossible(Advancement):
        def __init__(self):
            self.type = "impossible"

    class inventory_changed(Advancement):
        def __init__(self):
            self.type = "inventory_changed"

    class item_durability_changed(Advancement):
        def __init__(self):
            self.type = "item_durability_changed"

    class item_used_on_block(Advancement):
        def __init__(self):
            self.type = "item_used_on_block"

    class kill_mob_near_sculk_catalyst(Advancement):
        def __init__(self):
            self.type = "kill_mob_near_sculk_catalyst"

    class killed_by_crossbow(Advancement):
        def __init__(self):
            self.type = "killed_by_crossbow"

    class levitation(Advancement):
        def __init__(self):
            self.type = "levitation"

    class lightning_strike(Advancement):
        def __init__(self):
            self.type = "lightning_strike"

    class location(Advancement):
        def __init__(self):
            self.type = "location"

    class nether_travel(Advancement):
        def __init__(self):
            self.type = "nether_travel"

    class placed_block(Advancement):
        def __init__(self):
            self.type = "placed_block"

    class player_generates_container_loot(Advancement):
        def __init__(self):
            self.type = "player_generates_container_loot"

    class player_hurt_entity(Advancement):
        def __init__(self):
            self.type = "player_hurt_entity"

    class player_interacted_with_entity(Advancement):
        def __init__(self):
            self.type = "player_interacted_with_entity"

    class player_killed_entity(Advancement):
        def __init__(self):
            self.type = "player_killed_entity"

    class recipe_crafted(Advancement):
        def __init__(self):
            self.type = "recipe_crafted"

    class recipe_unlocked(Advancement):
        def __init__(self):
            self.type = "recipe_unlocked"

    class ride_entity_in_lava(Advancement):
        def __init__(self):
            self.type = "ride_entity_in_lava"

    class shot_crossbow(Advancement):
        def __init__(self):
            self.type = "shot_crossbow"

    class slept_in_bed(Advancement):
        def __init__(self):
            self.type = "slept_in_bed"

    class slide_down_block(Advancement):
        def __init__(self):
            self.type = "slide_down_block"

    class started_riding(Advancement):
        def __init__(self):
            self.type = "started_riding"

    class summoned_entity(Advancement):
        def __init__(self):
            self.type = "summoned_entity"

    class tame_animal(Advancement):
        def __init__(self):
            self.type = "tame_animal"

    class target_hit(Advancement):
        def __init__(self):
            self.type = "target_hit"

    class thrown_item_picked_up_by_entity(Advancement):
        def __init__(self):
            self.type = "thrown_item_picked_up_by_entity"

    class thrown_item_picked_up_by_player(Advancement):
        def __init__(self):
            self.type = "thrown_item_picked_up_by_player"

    class tick(Advancement):
        def __init__(self):
            self.type = "tick"

    class used_ender_eye(Advancement):
        def __init__(self):
            self.type = "used_ender_eye"

    class used_totem(Advancement):
        def __init__(self):
            self.type = "used_totem"

    class using_item(Advancement):
        def __init__(self):
            self.type = "using_item"

    class villager_trade(Advancement):
        def __init__(self):
            self.type = "villager_trade"

    class voluntary_exile(Advancement):
        def __init__(self):
            self.type = "voluntary_exile"


class ConditionType:
    class Entity:
        pass

    class Item:
        pass

    class NumberObject:
        pass

    class Location:
        pass


class Condition:
    @staticmethod
    def location(condition: ConditionType.Location):
        """
        Predicates applied to the location relevant to the advancement.
        Applies to `allay_drop_item_on_block`, `item_used_on_block`, and `placed_block`
        """
        pass

    @staticmethod
    def block(block: str):
        """
        The ID of the relevant block
        Applies to `bee_nest_destroyed`, `enter_block`, and `slide_down_block`
        """
        pass

    @staticmethod
    def item(condition: ConditionType.Item):
        """
        The relevant item that was used, consumed, attained, etc.
        Applies to `bee_nest_destroyed`, `consume_item`, `consume_item`, `filled_bucket`, `fishing_rod_hooked`, `item_durability_changed`, `player_interacted_with_entity`, `shot_crossbow`, `thrown_item_picked_up_by_entity`, `thrown_item_picked_up_by_player`, `used_totem`, `using_item`, and `villager_trade`
        """
        pass

    @staticmethod
    def num_bees_inside(bees: int):
        """
        The number of bees inside the broken hive.
        Applies to `bee_nest_destroyed`
        """
        pass

    @staticmethod
    def child(condition: ConditionType.Entity):
        """
        The entity that was created
        Applies to `bred_animals`
        """
        pass

    @staticmethod
    def parent(condition: ConditionType.Entity):
        """
        The entity that was bred
        Applies to `bred_animals`
        """
        pass

    @staticmethod
    def partner(condition: ConditionType.Entity):
        """
        The entity that was bred
        Applies to `bred_animals`
        """
        pass

    @staticmethod
    def potion(potion: str):
        """
        The string ID of the potion that was brewed.
        Applies to `brewed_potion`
        """
        pass

    @staticmethod
    def from_dimension(dimension: str):
        """
        The dimension travelled from
        Applies to `changed_dimension`
        """
        pass

    @staticmethod
    def to_dimension(dimension: str):
        """
        The dimension travelled to
        Applies to `changed_dimension`
        """
        pass

    @staticmethod
    def victims(condition: ConditionType):
        """TODO"""
        pass

    @staticmethod
    def beacon_level(condition: ConditionType.NumberObject):
        """
        The level of the beacon constructed, 1, 2, 3, or 4
        Applies to `construct_beacon`
        """
        pass

    @staticmethod
    def villager(condition: ConditionType.Entity):
        """
        The relevant villager
        Applies to `cured_zombie_villager` and `villager_trade`
        """
        pass

    @staticmethod
    def zombie(condition: ConditionType.Entity):
        """
        The zombie villager that the villager was right before it was converted
        Applies to `cured_zombie_villager`
        """
        pass

    @staticmethod
    def source(condition: ConditionType.Entity):
        pass

    @staticmethod
    def effects(condition: ConditionType):
        """TODO"""
        pass

    @staticmethod
    def levels(condition: ConditionType.NumberObject):
        """
        The levels spend by the player on the enchantment
        Applies to `enchanted_item`
        """
        pass

    @staticmethod
    def state(condition: ConditionType):
        """TODO"""
        pass

    @staticmethod
    def damage(condition: ConditionType):
        """TODO"""
        pass

    @staticmethod
    def killing_blow(condition: ConditionType):
        """TODO"""
        pass

    @staticmethod
    def start_position(condition: ConditionType.Location):
        """
        The last position of the player before the advancement was begun
        Applies to `fall_from_height`, `nether_travel`, and `ride_entity_in_lava`
        """
        pass

    @staticmethod
    def distance(condition: ConditionType):
        """TODO"""
        pass

    @staticmethod
    def entity(condition: ConditionType.Entity):
        pass

    @staticmethod
    def rod(condition: ConditionType.Item):
        """
        The fishing rod that was used
        Applies to `fishing_rod_hooked`
        """
        pass

    @staticmethod
    def items(condition: ConditionType):
        """TODO"""
        pass

    @staticmethod
    def slots(condition: ConditionType):
        """TODO"""
        pass

    @staticmethod
    def delta(condition: ConditionType.NumberObject):
        """
        The change in the durability of the item
        Applies to `item_durability_changed`
        """
        pass

    @staticmethod
    def durability(condition: ConditionType.NumberObject):
        """
        The remaining durability of the item
        Applies to `item_durability_changed`
        """
        pass

    @staticmethod
    def unique_entity_types(condition: ConditionType.NumberObject):
        """
        The number of unique entities killed
        Applies to `killed_by_crossbow`
        """
        pass

    @staticmethod
    def duration(condition: ConditionType.NumberObject):
        """
        The duration of the effect in ticks
        Applies to `levitation`
        """
        pass

    @staticmethod
    def lightning(condition: ConditionType.Entity):
        """
        The lightning entity
        Applies to `lightning_strike`
        """
        pass

    @staticmethod
    def bystander(condition: ConditionType.Entity):
        """
        An entity not hurt by the lightning but in a certain radius around it.
        Applies to `lightning_strike`
        """
        pass

    @staticmethod
    def loot_table(table: str):
        """
        The resource location of the loot table generated
        Applies to `player_generates_container_loot`
        """
        pass

    @staticmethod
    def recipe(recipe: str):
        """
        The resoure location of the recipe that was unlocked.
        Applies to `recipe_unlocked`
        """
        pass

    @staticmethod
    def recipe_id(recipe: str):
        """
        The resoure location of the recipe that was crafted.
        Applies to `recipe_crafted`
        """
        pass

    @staticmethod
    def ingredients(condition: ConditionType):
        """TODO"""
        pass

    @staticmethod
    def signal_strength(condition: ConditionType.NumberObject):
        """
        The signal strength outputted from the hit target
        Applies to`target_hit`
        """
        pass

    @staticmethod
    def projectile(condition: ConditionType.Entity):
        """
        The projectile that hit the target
        Applies to`target_hit`
        """
        pass

    @staticmethod
    def stronghold_distance(condition: ConditionType.NumberObject):
        """
        The horizontal distance between the player and the stronghold.
        Applies to`used_ender_eye`
        """
        pass
