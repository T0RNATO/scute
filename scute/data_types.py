"""
Various data types used in NBT.
"""
from typing import TypeVar, Union


class _NumberType:
    letter = None
    int = False

    def __init__(self, number):
        if self.int:
            self.number = int(number)
        else:
            self.number = number

    def __str__(self):
        return str(self.number) + self.letter

    def getNbt(self):
        return str(self.number) + self.letter


class Byte(_NumberType):
    letter = "b"
    int = True


class Long(_NumberType):
    letter = "l"
    int = True


class Short(_NumberType):
    letter = "s"
    int = True


class Float(_NumberType):
    letter = "f"


class Double(_NumberType):
    letter = "d"


_NumberTypeVar = TypeVar("_NumberTypeVar", bound=_NumberType)
_NbtValue = Union[_NumberTypeVar, int, str, float, dict]
