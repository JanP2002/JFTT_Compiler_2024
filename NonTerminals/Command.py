import Instructions


class Command:
    def __init__(self, line_number=-1):
        self.line_number = line_number
        self.parent_procedure = None

    def set_parent_procedure(self, proc_pid):
        self.parent_procedure = proc_pid

    def translate(self, program):
        raise Exception("generateCode() not defined for %s" % self.__class__)


class CommandWriteNum(Command):
    def __init__(self, num, line_number=-1):
        super(CommandWriteNum, self).__init__(line_number)
        self.num = num

    def translate(self, p):
        return Instructions.write_num(self.num)


class CommandWritePid(Command):
    def __init__(self, pid, line_number=-1):
        super(CommandWritePid, self).__init__(line_number)
        self.pid = pid

    def translate(self, p):
        return Instructions.write_pid(self.pid, self.line_number, self.parent_procedure)


class CommandReadPid(Command):
    def __init__(self, pid, line_number=-1):
        super(CommandReadPid, self).__init__(line_number)
        self.pid = pid

    def translate(self, p):
        return Instructions.read_pid(self.pid, self.line_number, self.parent_procedure)


class CommandPidAssignNumber(Command):
    def __init__(self, pid, number, line_number):
        super(CommandPidAssignNumber, self).__init__(line_number)
        self.pid = pid
        self.number = number

    def translate(self, p):
        return Instructions.pid_assign_number(self.pid, self.number, self.line_number, self.parent_procedure)


class CommandPidAssignPid(Command):
    def __init__(self, l_pid, r_pid, line_number):
        super(CommandPidAssignPid, self).__init__(line_number)
        self.left_pid = l_pid
        self.right_pid = r_pid

    def translate(self, p):
        return Instructions.pid_assign_pid(self.left_pid, self.right_pid, self.line_number, self.parent_procedure)
