"""
Submodule for scoreboards and criteria
"""
from scute.tags import _tags
from scute import pack
from scute.commands import _command
from scute.json_text import _JsonText
from scute.internal.utils import create_function
import atexit

_scoreboard_list = []


class Scoreboard:
    def __init__(
        self,
        name: str,
        criteria: str,
        displayName: _JsonText = None,
        displaySlot: str = None,
    ):
        """
        Creates and initialises a scoreboard - this will be put in load.json. This object should be stored for doing operations on the scoreboard later.
        Args:
            name: Unique id of the scoreboard
            criteria: The criteria of the scoreboard, like `scute.scoreboards.Criteria.dummy` or `scute.scoreboards.Criteria.mined`(`scute.blocks.Block.stone`)
            displayName: Optional display name
            displaySlot: Optional display slot, like `scute.scoreboards.DisplaySlots.sidebar` or `scute.scoreboards.DisplaySlots.sidebar_team`(`scute.json_text.Colour.red`) to be set in load.json
        """
        self.name = name
        self.criteria = criteria
        self.display = displayName
        self.slot = displaySlot

        _scoreboard_list.append(self)

        load = "minecraft:load"
        init = pack.namespace + ":scute_init"

        if load not in _tags:
            _tags[load] = [init]
        elif init not in _tags[load]:
            _tags[load].append(init)

    @_command
    def delete(self):
        """
        Deletes the scoreboard and all its data
        """
        return f"scoreboard objectives remove {self.name}"

    @_command
    def set_display(self, slot: str):
        """
        Sets the display slot of the scoreboard
        Args:
            slot: The display slot, like `scute.scoreboards.DisplaySlots.sidebar`
        """
        return f"scoreboard objectives setdisplay {slot} {self.name}"

    @_command
    def get(self, target: str):
        """
        Gets the score of a target in the scoreboard
        Args:
            target: The target(s), like "@s"
        """
        return f"scoreboard players get {target} {self.name}"

    @_command
    def set(self, target: str, value: int):
        """
        Sets the score of a target in the scoreboard
        Args:
            target: The target(s), like "@s"
            value: The new value
        """
        return f"scoreboard players set {target} {self.name} {value}"

    @_command
    def add(self, target: str, value: int):
        """
        Adds a value to the score of a target in the scoreboard
        Args:
            target: The target(s), like "@s"
            value: The value for the score to be incremented by
        """
        return f"scoreboard players add {target} {self.name} {value}"

    @_command
    def remove(self, target: str, value: int):
        """
        Removes a value from the score of a target in the scoreboard
        Args:
            target: The target(s), like "@s"
            value: The value for the score to be decremented by
        """
        return f"scoreboard players remove {target} {self.name} {value}"

    @_command
    def reset(self, target: str):
        """
        Removes a target's score from the scoreboard
        Args:
            target: The target(s), like "@s"
        """
        return f"scoreboard players reset {target} {self.name}"

    @_command
    def enable(self, target: str):
        """
        Enables this scoreboard to be used in /trigger one time by the targets specified
        Args:
            target: The target(s), like "@s"
        """
        return f"scoreboard players enable {target} {self.name}"

    @_command
    def operation_as_source(
        self, source_target, operation, target_scoreboard: "Scoreboard", target_target
    ):
        """
        Runs an operation on a scoreboard value of a target of this scoreboard, and puts it into target_scoreboard under target_target
        Args:
            source_target: The target from this scoreboard to get the value from
            operation: The operation, like TODO
            target_scoreboard: The scoreboard which the value is put into
            target_target: The target from the source scoreboard to put the value into
        """
        return f"scoreboard players operation {target_target} {target_scoreboard.name} {operation} {self.name} {source_target}"

    @_command
    def operation_as_target(
        self, source_target, source_scoreboard: "Scoreboard", operation, target_target
    ):
        """
        Runs an operation on a scoreboard value of a target of this scoreboard, and puts it into target_scoreboard under target_target
        Args:
            source_target: The target from source_scoreboard to get the value from
            source_scoreboard: The scoreboard to get the value from
            operation: The operation, like TODO
            target_target: The target from this scoreboard that the value is put into
        """
        return f"scoreboard players operation {target_target} {self.name} {operation} {source_scoreboard.name} {source_target}"


def _register_scoreboards():
    function = [
        f"scoreboard objectives add {scoreboard.name} {scoreboard.criteria} {scoreboard.display}"
        for scoreboard in _scoreboard_list
    ]
    function += [
        f"scoreboard objectives setdisplay {scoreboard.slot} {scoreboard.name}"
        for scoreboard in _scoreboard_list
        if scoreboard.slot
    ]
    create_function(pack.namespace, "scute_init", function)


atexit.register(_register_scoreboards)


class Criteria:
    """
    Enum for scoreboard criteria
    """

    # Inbuilt criteria
    dummy = "dummy"
    trigger = "trigger"
    deathCount = "deathCount"
    playerKillCount = "playerKillCount"
    totalKillCount = "totalKillCount"
    health = "health"
    xp = "xp"
    level = "level"
    food = "food"
    air = "air"
    armor = "armor"

    # Custom statistic criteria
    animals_bred = "minecraft:animals_bred"
    clean_armor = "minecraft:clean_armor"
    clean_banner = "minecraft:clean_banner"
    open_barrel = "minecraft:open_barrel"
    bell_ring = "minecraft:bell_ring"
    eat_cake_slice = "minecraft:eat_cake_slice"
    fill_cauldron = "minecraft:fill_cauldron"
    open_chest = "minecraft:open_chest"
    damage_absorbed = "minecraft:damage_absorbed"
    damage_blocked_by_shield = "minecraft:damage_blocked_by_shield"
    damage_dealt = "minecraft:damage_dealt"
    damage_dealt_absorbed = "minecraft:damage_dealt_absorbed"
    damage_dealt_resisted = "minecraft:damage_dealt_resisted"
    damage_resisted = "minecraft:damage_resisted"
    damage_taken = "minecraft:damage_taken"
    inspect_dispenser = "minecraft:inspect_dispenser"
    climb_one_cm = "minecraft:climb_one_cm"
    crouch_one_cm = "minecraft:crouch_one_cm"
    fall_one_cm = "minecraft:fall_one_cm"
    fly_one_cm = "minecraft:fly_one_cm"
    sprint_one_cm = "minecraft:sprint_one_cm"
    swim_one_cm = "minecraft:swim_one_cm"
    walk_one_cm = "minecraft:walk_one_cm"
    walk_on_water_one_cm = "minecraft:walk_on_water_one_cm"
    walk_under_water_one_cm = "minecraft:walk_under_water_one_cm"
    boat_one_cm = "minecraft:boat_one_cm"
    aviate_one_cm = "minecraft:aviate_one_cm"
    horse_one_cm = "minecraft:horse_one_cm"
    minecart_one_cm = "minecraft:minecart_one_cm"
    pig_one_cm = "minecraft:pig_one_cm"
    strider_one_cm = "minecraft:strider_one_cm"
    inspect_dropper = "minecraft:inspect_dropper"
    open_enderchest = "minecraft:open_enderchest"
    fish_caught = "minecraft:fish_caught"
    leave_game = "minecraft:leave_game"
    inspect_hopper = "minecraft:inspect_hopper"
    interact_with_anvil = "minecraft:interact_with_anvil"
    interact_with_beacon = "minecraft:interact_with_beacon"
    interact_with_blast_furnace = "minecraft:interact_with_blast_furnace"
    interact_with_brewingstand = "minecraft:interact_with_brewingstand"
    interact_with_campfire = "minecraft:interact_with_campfire"
    interact_with_cartography_table = "minecraft:interact_with_cartography_table"
    interact_with_crafting_table = "minecraft:interact_with_crafting_table"
    interact_with_furnace = "minecraft:interact_with_furnace"
    interact_with_grindstone = "minecraft:interact_with_grindstone"
    interact_with_lectern = "minecraft:interact_with_lectern"
    interact_with_loom = "minecraft:interact_with_loom"
    interact_with_smithing_table = "minecraft:interact_with_smithing_table"
    interact_with_smoker = "minecraft:interact_with_smoker"
    interact_with_stonecutter = "minecraft:interact_with_stonecutter"
    drop = "minecraft:drop"
    enchant_item = "minecraft:enchant_item"
    jump = "minecraft:jump"
    mob_kills = "minecraft:mob_kills"
    play_record = "minecraft:play_record"
    play_noteblock = "minecraft:play_noteblock"
    tune_noteblock = "minecraft:tune_noteblock"
    deaths = "minecraft:deaths"
    pot_flower = "minecraft:pot_flower"
    player_kills = "minecraft:player_kills"
    raid_trigger = "minecraft:raid_trigger"
    raid_win = "minecraft:raid_win"
    clean_shulker_box = "minecraft:clean_shulker_box"
    open_shulker_box = "minecraft:open_shulker_box"
    sneak_time = "minecraft:sneak_time"
    talked_to_villager = "minecraft:talked_to_villager"
    target_hit = "minecraft:target_hit"
    play_time = "minecraft:play_time"
    time_since_death = "minecraft:time_since_death"
    time_since_rest = "minecraft:time_since_rest"
    total_world_time = "minecraft:total_world_time"
    sleep_in_bed = "minecraft:sleep_in_bed"
    traded_with_villager = "minecraft:traded_with_villager"
    trigger_trapped_chest = "minecraft:trigger_trapped_chest"
    use_cauldron = "minecraft:use_cauldron"

    @staticmethod
    def mined(block):
        """
        Returns a scoreboard criteria string for the number of blocks of the type that have been mined.
        Args:
            block: The block, like `scute.blocks.Block.stone`
        """
        return f"minecraft.mined:minecraft.{block}"

    @staticmethod
    def broken(item):
        """
        Returns a scoreboard criteria string for the number of items that have run out of durability.
        Args:
            item: The item, like `scute.items.Item.stone_pickaxe`
        """
        return f"minecraft.broken:minecraft.{item}"

    @staticmethod
    def crafted(item):
        """
        Returns a scoreboard criteria string for the number of items of a type that have been crafted.
        Args:
            item: The item, like `scute.items.Item.diamond_chestplate`
        """
        return f"minecraft.crafted:minecraft.{item}"

    @staticmethod
    def used(item):
        """
        Returns a scoreboard criteria string for the number of items of a type that have been used.
        Args:
            item: The item, like `scute.items.Item.stone_shovel`
        """
        return f"minecraft.used:minecraft.{item}"

    @staticmethod
    def picked_up(item):
        """
        Returns a scoreboard criteria string for the number of items of a type that have been picked up.
        Args:
            item: The item, like `scute.items.Item.diamond`
        """
        return f"minecraft.picked_up:minecraft.{item}"

    @staticmethod
    def dropped(item):
        """
        Returns a scoreboard criteria string for the number of items of a type that have been dropped.
        Args:
            item: The item, like `scute.items.Item.diamond`
        """
        return f"minecraft.dropped:minecraft.{item}"

    @staticmethod
    def killed(entity):
        """
        Returns a scoreboard criteria string for the number of entities of a type that the player has killed.
        Args:
            entity: The entity, like TODO :)
        """
        pass

    @staticmethod
    def killed_by(entity):
        """
        Returns a scoreboard criteria string for the number of times the player has been killed by entities of a type.
        Args:
            entity: The entity, like TODO :)
        """
        pass


class DisplaySlots:
    """
    An enum for display slots for scoreboards
    """

    list = "list"
    sidebar = "sidebar"
    belowName = "belowName"

    @staticmethod
    def sidebar_team(colour: str):
        """
        Returns a display slot for a team with the specified colour
        Args:
            colour: The colour of the team to show the scoreboard to, like `scute.json_text.Colour.red`
        """
        return f"sidebar.team.{colour}"
