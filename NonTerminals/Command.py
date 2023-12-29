import Instructions


class Command:
    def __init__(self, line_number=-1):
        self.line_number = line_number

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


class CommandReadPid(Command):
    def __init__(self, pid):
        super(CommandReadPid, self).__init__()
        self.pid = pid

    def translate(self, p):
        return Instructions.read_pid(self.pid)


class CommandPidAssignNumber(Command):
    def __init__(self, pid, number, line_number):
        super(CommandPidAssignNumber, self).__init__()
        self.pid = pid
        self.number = number
        self.lineNumber = line_number

    def translate(self, p):
        return Instructions.pid_assign_number(self.pid, self.number)


class CommandPidAssignPid(Command):
    def __init__(self, l_pid, r_pid, line_number):
        super(CommandPidAssignPid, self).__init__()
        self.left_pid = l_pid
        self.right_pid = r_pid
        self.line_number = line_number

    def translate(self, p):
        return Instructions.pid_assign_pid(self.left_pid, self.right_pid, self.line_number)
