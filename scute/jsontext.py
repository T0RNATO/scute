"""
Submodule for json-formatted text, like in /tellraw or item names etc
"""
from scute import _JsonText
from scute.internal.dictToNBT import dictToNBT
from scute.items import Item

def JSONText(string: str,
             italic: bool = False,
             colour: str = None,
             strikethrough: bool = None,
             bold: bool = None,
             underlined: bool = None,
             obfuscated: bool = None,
             click_url: str = None,
             click_command: str = None,
             click_suggest: str = None,
             click_clipboard: str = None,
             hover_text: dict | str = None,
             hover_item: Item = None,
             hover_entity: dict = None,
             ):
    """
    Creates json-formatted text. A maximum of one of the click_* or hover_* arguments can be specified
    Args:
        string: The actual text to show
        italic: Bool. Whether or not to make the text italic
        colour: The colour of the text. E.g: `Colour.red`, `"red"`, `"#FFFFFF"`, or `Colour.hex("#FFFFFF)`
        strikethrough: Bool. Whether or not to make the text struckthrough
        bold: Bool. Whether or not to make the text bold
        underlined: Bool. Whether or not to make the text underlined
        obfuscated: Bool. Whether or not to make the text obfuscated
        click_url: The URL opened when the text is clicked - must include schema
        click_command: The command run by the user when the text is clicked
        click_suggest: The string added to the chat window when the text is clicked
        click_clipboard: The value that is copied to the clipboard when the text is clicked
        hover_text: The json-formatted text that is shown when the text is hovered (or just a string)
        hover_item: The item that is shown when the text is hovered
        hover_entity: The entity that is shown when the text is hovered - e.g. {"type":"pig", "id":"0-0-0-0"}. json-formatted `name` field is optional.
    Returns:
        An JsonText instance, to be passed into various functions
    """
    optionalArgs = {
        "strikethrough": strikethrough,
        "color": colour,
        "bold": bold,
        "underlined": underlined,
        "obfuscated": obfuscated
    }

    text = {
        "text": string,
        "italic": italic,
        **{key: value for key, value in optionalArgs.items() if value is not None}
    }

    if click_url is not None: text["clickEvent"] = {"action": "open_url", "value": click_url}
    if click_command is not None: text["clickEvent"] = {"action": "run_command", "value": click_command}
    if click_suggest is not None: text["clickEvent"] = {"action": "suggest_command", "value": click_suggest}
    if click_clipboard is not None: text["clickEvent"] = {"action": "copy_to_clipboard", "value": click_clipboard}
    if hover_text is not None: text["hoverEvent"] = {"action": "show_text", "contents": hover_text}
    if hover_item is not None:
        data = {
            "action": "show_item",
            "contents": {
                "id": hover_item.id,
                "count": hover_item.count,
            }
        }
        if hover_item.nbt is not None:
            data["contents"]["tag"] = dictToNBT(hover_item.nbt)
        text["hoverEvent"] = data
    if hover_entity is not None:
        if "type" in hover_entity:
            if "id" in hover_entity:
                data = {
                    "action": "show_entity",
                    "contents": {
                        "type": hover_entity["type"],
                        "id": hover_entity["id"],
                    }
                }
                if "name" in hover_entity:
                    data["contents"]["name"] = hover_entity["name"]
                text["hoverEvent"] = data
            else:
                raise Exception("You must specify the UUID of the entity to show in a `show_entity` hover event, under the `id` field")
        else:
            raise Exception(
                "You must specify the type of the entity to show in a `show_entity` hover event, under the `type` field")

    return _JsonText(text)


class Colour:
    black = "black"
    dark_blue = "dark_blue"
    dark_green = "dark_green"
    dark_aqua = "dark_aqua"
    dark_red = "dark_red"
    dark_purple = "dark_purple"
    gold = "gold"
    gray = "gray"
    dark_gray = "gray"
    grey = "gray"
    dark_grey = "gray"
    blue = "blue"
    green = "green"
    aqua = "aqua"
    red = "red"
    light_purple = "light_purple"
    yellow = "yellow"
    white = "white"

    @staticmethod
    def hex(hex: str):
        """
        A custom colour - alternatively, just use a string like "#FFFFFF"
        """
        return hex
