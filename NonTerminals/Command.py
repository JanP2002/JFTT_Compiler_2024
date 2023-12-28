import Instructions


class Command:
    def __init__(self, line_number=-1):
        self.lineNumber = line_number

    def translate(self, program):
        raise Exception("generateCode() not defined for %s" % self.__class__)


class CommandWriteNum(Command):
    def __init__(self, num):
        super(CommandWriteNum, self).__init__()
        self.num = num

    def translate(self, p):
        return Instructions.write_num(self.num)


class CommandWritePid(Command):
    def __init__(self, pid):
        super(CommandWritePid, self).__init__()
        self.pid = pid

    def translate(self, p):
        return Instructions.write_pid(self.pid)