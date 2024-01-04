from enum import Enum


class REG(Enum):
    PLUS = '+'
    MINUS = '-'

    def __str__(self):
        return self.value
