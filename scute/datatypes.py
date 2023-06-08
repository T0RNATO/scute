class NumberType:
    letter = None
    int = False
    def __init__(self, number):
        if self.int:
            self.number = int(number)
        else:
            self.number = number

    def getNbt(self):
        return str(self.number) + self.letter

class Byte(NumberType):
    letter = "b"
    int = True

class Long(NumberType):
    letter = "l"
    int = True

class Short(NumberType):
    letter = "s"
    int = True

class Float(NumberType):
    letter = "f"

class Double(NumberType):
    letter = "d"