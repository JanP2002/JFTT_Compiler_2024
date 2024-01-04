import Instructions
from typing import List
from NonTerminals.ProcCallParam import ProcCallParam


class Command:
    def __init__(self, line_number=-1):
        self.line_number = line_number
        self.parent_procedure = None
        self.is_proc_call = False
        self.parent_procedure_label = None

    def set_parent_procedure(self, proc_pid):
        self.parent_procedure = proc_pid

    def set_parent_procedure_label(self, label):
        self.parent_procedure_label = label

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


class CommandPidAssignNumOpNum(Command):
    def __init__(self, pid, num1, num2, operation, line_number):
        super(CommandPidAssignNumOpNum, self).__init__(line_number)
        self.pid = pid
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    def translate(self, p):
        return Instructions.pid_assign_num_op_num(self.pid, self.num1, self.num2,
                                                  self.operation, self.line_number, self.parent_procedure)


class ProcCall(Command):
    def __init__(self, proc_pid, params: List[ProcCallParam], line_number):
        super(ProcCall, self).__init__(line_number)
        self.procedure_pid = proc_pid
        self.is_proc_call = True
        self.params = params

    def translate(self, p):
        return Instructions.proc_call(self.procedure_pid, self.params, self.line_number, self.parent_procedure)
