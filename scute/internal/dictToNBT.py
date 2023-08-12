import json

from scute.datatypes import _NumberType


def encode_value(value):
    out = ""
    # If the value is a NBT number like 1b, get its NBT representation
    if issubclass(type(value), _NumberType):
        out += value.getNbt()
    # If the value is a dict or list, encode it
    elif isinstance(value, dict) or isinstance(value, list):
        out += encode_dict_or_list(value)
    # If the value is a string, just add it
    elif isinstance(value, str):
        out += f'"{value}"'
    # If the value is an int, just add it
    elif isinstance(value, int):
        out += str(value)

    return out


def encode_dict_or_list(obj):
    out = ""
    index = 0
    if isinstance(obj, dict):
        out = "{"
        # Loop through keys and values of the dict
        for key, value in obj.items():
            if index != 0:
                out += ", "

            # Add the key and value to the output
            out += str(key) + ": "
            out += encode_value(value)
            index += 1

        out += "}"

    elif isinstance(obj, list):
        out += "["
        for value in obj:
            if index != 0:
                out += ", "
            out += encode_value(value)

        out += "]"

    return out


class dtn(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encode(self, obj):
        return encode_dict_or_list(obj)


def dictToNBT(dic):
    return json.dumps(dic, cls=dtn)
