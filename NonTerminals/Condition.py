#W Reg A 0, lub dodatnia
import Instructions
from MemoryManager import MemoryManager
from Register import REG
from enum import Enum


class COP(Enum):
    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="
    EQ = "="
    NE = "!="

    def __str__(self):
        return self.value


def generate_compare(cop: COP):
    asm_code = []
    if cop == COP.LT:
        asm_code.append(Instructions.makeInstr('GET', REG.D))
        asm_code.append(Instructions.makeInstr('SUB', REG.C))
    elif cop == COP.GT:
        asm_code.append(Instructions.makeInstr('GET', REG.C))
        asm_code.append(Instructions.makeInstr('SUB', REG.D))
    elif cop == COP.LE: # C <= D:
        asm_code.append(Instructions.makeInstr('INC', REG.C))#?
        asm_code.append(Instructions.makeInstr('GET', REG.C))
        asm_code.append(Instructions.makeInstr('SUB', REG.D))
        #TODO:

    return asm_code


def load_num(reg: REG, val):
    asm_code = []
    asm_code.extend(Instructions.set_register_const(reg, val))
    return asm_code









class Condition:
    def __init__(self, val1, val2, compare_op, line_number, parent_proc=None):
        self.compare_operator = compare_op
        self.val1 = val1
        self.val2 = val2
        self.parent_proc = parent_proc
        self.line_number = line_number

    def translate(self, program):
        raise Exception("generateCode() not defined for %s" % self.__class__)


class ConditionNumNum(Condition):
    def __init__(self, val1, val2, compare_op):
        super(ConditionNumNum, self).__init__(compare_op, val1, val2)

    def translate(self, p):
        asm_code = []
        if self.compare_operator == COP.LT:
            if self.val1 < self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))
        elif self.compare_operator == COP.GT:
            if self.val1 > self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))
        elif self.compare_operator == COP.GE:
            if self.val1 >= self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))
        elif self.compare_operator == COP.LE:
            if self.val1 <= self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))
        elif self.compare_operator == COP.EQ:
            if self.val1 == self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))
        elif self.compare_operator == COP.NE:
            if self.val1 != self.val2:
                asm_code.extend(Instructions.set_register_const(REG.A, 1))
            else:
                asm_code.extend(Instructions.set_register_const(REG.A, 0))

        return asm_code


class ConditionPidNum(Condition):
    def __init__(self, val1, val2, compare_op):
        super(ConditionPidNum, self).__init__(compare_op, val1, val2)

    def translate(self, p):
        asm_code = []
        # asm_code.append(Instructions.makeInstr('LOAD', REG.A))
        # asm_code.append(Instructions.makeInstr('PUT', REG.C))
        # asm_code.append(Instructions.set_register_const(REG.D, self.val2))
        asm_code.extend(Instructions.load_pid(REG.C, self.val1, self.line_number, self.parent_proc))
        asm_code.extend(load_num(REG.D, self.val2))


