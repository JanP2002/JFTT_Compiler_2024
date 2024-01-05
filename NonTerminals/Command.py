import Instructions
from typing import List

from MemoryManager import MemoryManager, MemoryManagerException
from NonTerminals.ProcCallParam import ProcCallParam
from Register import REG


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
        asm_code = Instructions.set_register_const(REG.A, self.num)
        asm_code.append(Instructions.makeInstr('WRITE'))
        return asm_code


class CommandWritePid(Command):
    def __init__(self, pid, line_number=-1):
        super(CommandWritePid, self).__init__(line_number)
        self.pid = pid

    def translate(self, p):
        memory_manager: MemoryManager = MemoryManager()
        asm_code = []
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if declaration.is_param:
                if (not declaration.is_initialized) and (not declaration.must_be_initialized):
                    declaration.set_uninitialized_error(self.pid, self.line_number)
                address = declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))
                asm_code.append(Instructions.makeInstr('WRITE'))
            else:
                if not declaration.is_initialized:
                    raise MemoryManagerException("Blad w linii %i: Zmienna %s nie jest zainicjalizowana" %
                                                 (self.line_number, declaration.pid))
                address = declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))
                asm_code.append(Instructions.makeInstr('WRITE'))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            if not declaration.is_initialized:
                raise MemoryManagerException("Blad w linii %i: Zmienna %s nie jest zainicjalizowana" %
                                             (self.line_number, declaration.pid))
            address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.B, address))
            asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))
            asm_code.append(Instructions.makeInstr('WRITE'))

        return asm_code


class CommandReadPid(Command):
    def __init__(self, pid, line_number=-1):
        super(CommandReadPid, self).__init__(line_number)
        self.pid = pid

    def translate(self, p):
        memory_manager: MemoryManager = MemoryManager()
        asm_code = []
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            address = declaration.get_memory_id()
            if declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))  # w A mamy teraz adres zmiennej pid
                asm_code.append(Instructions.makeInstr('PUT', REG.B.value))  # w B mamy teraz adres zmiennej pid
                asm_code.append(Instructions.makeInstr('READ'))
                asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
                # declaration.must_be_initialized = False
            else:
                asm_code.append(Instructions.makeInstr('READ'))
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
            declaration.is_initialized = True

        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            address = declaration.get_memory_id()
            asm_code.append(Instructions.makeInstr('READ'))
            asm_code.extend(Instructions.set_register_const(REG.B, address))
            asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
            declaration.is_initialized = True

        return asm_code


class CommandPidAssignNumber(Command):
    def __init__(self, pid, number, line_number):
        super(CommandPidAssignNumber, self).__init__(line_number)
        self.pid = pid
        self.number = number

    def translate(self, p):
        memory_manager: MemoryManager = MemoryManager()
        asm_code = []
        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + "##" + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            if declaration.is_param:
                address = declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))  # w A mamy teraz adres zmiennej pid
                asm_code.append(Instructions.makeInstr('PUT', REG.B.value))  # w B mamy teraz adres zmiennej pid
                asm_code.extend(Instructions.set_register_const(REG.A, self.number))
                asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
                declaration.is_initialized = True
            else:
                address = declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.A, self.number))
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
                declaration.is_initialized = True
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.A, self.number))
            asm_code.extend(Instructions.set_register_const(REG.B, address))
            asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
            declaration.is_initialized = True
        return asm_code


class CommandPidAssignPid(Command):
    def __init__(self, l_pid, r_pid, line_number):
        super(CommandPidAssignPid, self).__init__(line_number)
        self.left_pid = l_pid
        self.right_pid = r_pid

    def translate(self, p):
        memory_manager: MemoryManager = MemoryManager()
        asm_code = []
        if self.parent_procedure is not None:
            l_variable_id = self.parent_procedure + "##" + self.left_pid
            r_variable_id = self.parent_procedure + "##" + self.right_pid
            l_declaration = memory_manager.get_variable(l_variable_id, self.line_number)
            r_declaration = memory_manager.get_variable(r_variable_id, self.line_number)
            if l_declaration.is_local and r_declaration.is_local:
                if not r_declaration.is_initialized:
                    raise MemoryManagerException(
                        "Blad w linii %i: nizainicjowana zmienna %s" % (self.line_number, self.right_pid))
                l_address = l_declaration.get_memory_id()
                r_address = r_declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.E, r_address))  # adres zmiennej right_pid w reg e
                asm_code.append(Instructions.makeInstr('LOAD', REG.E.value))
                asm_code.extend(Instructions.set_register_const(REG.B, l_address))
                asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
                l_declaration.is_initialized = True
            elif l_declaration.is_param and r_declaration.is_local:
                if not r_declaration.is_initialized:
                    raise MemoryManagerException(
                        "Blad w linii %i: nizainicjowana zmienna %s" % (self.line_number, self.right_pid))
                l_address = l_declaration.get_memory_id()
                r_address = r_declaration.get_memory_id()  # adres zmiennej right_pid
                asm_code.extend(Instructions.set_register_const(REG.B, l_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))  # w A mamy teraz adres zmiennej left_pid
                asm_code.append(Instructions.makeInstr('PUT', REG.B.value))  # w B mamy teraz adres zmiennej left_pid
                asm_code.extend(Instructions.set_register_const(REG.E, r_address))  # adres zmiennej right_pid w reg e
                asm_code.append(Instructions.makeInstr('LOAD', REG.E.value))
                asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
                l_declaration.is_initialized = True
            elif l_declaration.is_local and r_declaration.is_param:
                if (not r_declaration.is_initialized) and (not r_declaration.must_be_initialized):
                    r_declaration.set_uninitialized_error(self.right_pid, self.line_number)
                l_address = l_declaration.get_memory_id()  # adres zmiennej left_pid
                r_address = r_declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.E, r_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.E.value))  # w A mamy teraz adres zmiennej right_pid
                # asm_code.append(makeInstr('PUT', REG.E.value))  # w E mamy teraz adres zmiennej right_pid
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))  # w A mamy teraz wartosc zmiennej right_pid
                asm_code.extend(Instructions.set_register_const(REG.B, l_address))
                asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
                l_declaration.is_initialized = True
            else:  # l_declaration.is_param and r_declaration.is_param
                if (not r_declaration.is_initialized) and (not r_declaration.must_be_initialized):
                    r_declaration.set_uninitialized_error(self.right_pid, self.line_number)
                l_address = l_declaration.get_memory_id()
                r_address = r_declaration.get_memory_id()
                asm_code.extend(Instructions.set_register_const(REG.B, l_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.B.value))  # w A mamy teraz adres zmiennej left_pid
                asm_code.append(Instructions.makeInstr('PUT', REG.B.value))  # w B mamy teraz adres zmiennej left_pid

                asm_code.extend(Instructions.set_register_const(REG.E, r_address))
                asm_code.append(Instructions.makeInstr('LOAD', REG.E.value))  # w A mamy teraz adres zmiennej right_pid
                # asm_code.append(makeInstr('PUT', REG.E.value))  # w E mamy teraz adres zmiennej right_pid
                asm_code.append(Instructions.makeInstr('LOAD', REG.A.value))  # w A mamy teraz wartosc zmiennej right_pid
                asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
                l_declaration.is_initialized = True
        else:
            l_declaration = memory_manager.get_variable(self.left_pid, self.line_number)
            r_declaration = memory_manager.get_variable(self.right_pid, self.line_number)
            if not r_declaration.is_initialized:
                raise MemoryManagerException("Blad w linii %i: nizainicjowana zmienna %s" % (self.line_number,
                                                                                             self.right_pid))
            l_address = l_declaration.get_memory_id()
            r_address = r_declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.E, r_address))  # adres zmiennej right_pid w reg e
            asm_code.append(Instructions.makeInstr('LOAD', REG.E.value))
            asm_code.extend(Instructions.set_register_const(REG.B, l_address))
            asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
            l_declaration.is_initialized = True
        return asm_code


class CommandPidAssignNumOpNum(Command):
    def __init__(self, pid, num1, num2, operation, line_number):
        super(CommandPidAssignNumOpNum, self).__init__(line_number)
        self.pid = pid
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    def translate(self, p):
        memory_manager: MemoryManager = MemoryManager()
        asm_code = []

        if self.parent_procedure is not None:
            variable_id = self.parent_procedure + '##' + self.pid
            declaration = memory_manager.get_variable(variable_id, self.line_number)
            address = declaration.get_memory_id()
            if declaration.is_param:
                asm_code.extend(Instructions.set_register_const(REG.B, address))
                asm_code.append(Instructions.LOAD(REG.B))  # w A mamy teraz adres zmiennej pid
                asm_code.append(Instructions.makeInstr('PUT', REG.B.value))  # w B mamy teraz adres zmiennej pid

            else:
                asm_code.extend(Instructions.set_register_const(REG.B, address))
        else:
            declaration = memory_manager.get_variable(self.pid, self.line_number)
            address = declaration.get_memory_id()
            asm_code.extend(Instructions.set_register_const(REG.B, address))

        if self.operation == '+':
            result = self.num1 + self.num2
            asm_code.extend(Instructions.set_register_const(REG.A, result))
        elif self.operation == '-':
            result = 0
            if self.num2 < self.num1:
                result = self.num1 - self.num2
            asm_code.extend(Instructions.set_register_const(REG.A, result))
        elif self.operation == "*":
            result = self.num1 * self.num2
            asm_code.extend(Instructions.set_register_const(REG.A, result))
        elif self.operation == '/':
            result = 0
            if self.num2 != 0:
                result = self.num1 // self.num2
            asm_code.extend(Instructions.set_register_const(REG.A, result))
        elif self.operation == '%':
            result = 0
            if self.num2 != 0:
                result = self.num1 % self.num2
            asm_code.extend(Instructions.set_register_const(REG.A, result))
        else:
            raise Exception("Nieprawidlowa operacja")
        asm_code.append(Instructions.makeInstr('STORE', REG.B.value))
        declaration.is_initialized = True
        return asm_code

# asm_code.extend(set_register_const(REG.A, num1))
# asm_code.extend(set_register_const(REG.B, num2))
# if operation == '+':
#     asm_code.extend(generate_adding(num1, num2))
# elif operation == '-':
#     asm_code.extend(generate_subtraction(num1, num2))
# else:
#     raise Exception("Nieprawidlowa operacja")


class ProcCall(Command):
    def __init__(self, proc_pid, params: List[ProcCallParam], line_number):
        super(ProcCall, self).__init__(line_number)
        self.procedure_pid = proc_pid
        self.is_proc_call = True
        self.params = params

    def translate(self, p):
        return Instructions.proc_call(self.procedure_pid, self.params, self.line_number, self.parent_procedure)
