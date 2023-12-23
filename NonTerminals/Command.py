import Instructions


class Command:
    def __init__(self, line_number=-1):
        self.lineNumber = line_number

    def translate(self, program):
        raise Exception("generateCode() not defined for %s" % self.__class__)


class CommandWrite(Command):
    def __init__(self, value):
        super(CommandWrite, self).__init__()
        self.value = value

    def translate(self, p):
        return Instructions.WRITE(self.value)
