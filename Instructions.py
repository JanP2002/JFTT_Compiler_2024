from MemoryManager import MemoryManager
from MemoryManager import MemoryManagerException
from NonTerminals.ProcCallParam import ProcCallParam
from Register import REG
from typing import List


def makeInstr(instr, X="", Y=""):
    instr_str = "%s %s %s" % (instr, X, Y)
    # self.inc_counter()
    # self.instructions.append(instr_str)
    return instr_str


def GET(reg):
    return makeInstr('GET', reg)


def STORE(reg):
    return makeInstr('STORE', reg)


def LOAD(reg):
    return makeInstr('LOAD', reg)


def INC(reg):
    return makeInstr('INC', reg)


def JUMP(j):
    return makeInstr('JUMP', j)


def DEC(X):
    return makeInstr('DEC', X)


def ADD(X, Y):
    return makeInstr('ADD', X, Y)


def SHL(X):
    return makeInstr('SHL', X)


def SHR(X):
    return makeInstr('SHR', X)


def SUB(X, Y):
    return makeInstr('SUB', X, Y)


def RST(X):
    return makeInstr('RST', X)


def STRK(X):
    return makeInstr('STRK', X)


def evalToRegInstr(value, reg):
    return set_register_const(reg, value)


def write_num(num: int):
    # evalToRegInstr(value,  REG.A)
    asm_code = set_register_const(REG.A, num)
    asm_code.append(makeInstr('WRITE'))
    return asm_code


def write_pid(pid, line_number, parent_proc=None):
    memory_manager: MemoryManager = MemoryManager()
    asm_code = []
    if parent_proc is not None:
        variable_id = parent_proc + "##" + pid
        declaration = memory_manager.get_variable(variable_id, line_number)
        if declaration.is_param:
            if (not declaration.is_initialized) and (not declaration.must_be_initialized):
                declaration.set_uninitialized_error(line_number)
            address = declaration.get_memory_id()
            asm_code.extend(set_register_const(REG.B, address))
            asm_code.append(makeInstr('LOAD', REG.B.value))
            asm_code.append(makeInstr('LOAD', REG.A.value))
            asm_code.append(makeInstr('WRITE'))
        else:
            if not declaration.is_initialized:
                raise MemoryManagerException("Blad w linii %i: Zmienna %s nie jest zainicjalizowana" %
                                             (line_number, declaration.pid))
            address = declaration.get_memory_id()
            asm_code.extend(set_register_const(REG.B, address))
            asm_code.append(makeInstr('LOAD', REG.B.value))
            asm_code.append(makeInstr('WRITE'))
    else:
        declaration = memory_manager.get_variable(pid, line_number)
        if not declaration.is_initialized:
            raise MemoryManagerException("Blad w linii %i: Zmienna %s nie jest zainicjalizowana" %
                                         (line_number, declaration.pid))
        address = declaration.get_memory_id()
        asm_code.extend(set_register_const(REG.B, address))
        asm_code.append(makeInstr('LOAD', REG.B.value))
        asm_code.append(makeInstr('WRITE'))

    return asm_code


def read_pid(pid, line_number, parent_proc=None):
    memory_manager: MemoryManager = MemoryManager()
    asm_code = []
    if parent_proc is not None:
        variable_id = parent_proc + "##" + pid
        declaration = memory_manager.get_variable(variable_id, line_number)
        address = declaration.get_memory_id()
        if declaration.is_param:
            asm_code.extend(set_register_const(REG.B, address))
            asm_code.append(makeInstr('LOAD', REG.B.value))  # w A mamy teraz adres zmiennej pid
            asm_code.append(makeInstr('PUT', REG.B.value))  # w B mamy teraz adres zmiennej pid
            asm_code.append(makeInstr('READ'))
            asm_code.append(makeInstr('STORE', REG.B.value))
            # declaration.must_be_initialized = False
        else:
            asm_code.append(makeInstr('READ'))
            asm_code.extend(set_register_const(REG.B, address))
            asm_code.append(makeInstr('STORE', REG.B.value))
        declaration.is_initialized = True

    else:
        declaration = memory_manager.get_variable(pid, line_number)
        address = declaration.get_memory_id()
        asm_code.append(makeInstr('READ'))
        asm_code.extend(set_register_const(REG.B, address))
        asm_code.append(makeInstr('STORE', REG.B.value))
        declaration.is_initialized = True

    return asm_code


# TODO: Dostosowac do procedur
def pid_assign_number(pid, number, line_num, parent_proc=None):
    memory_manager: MemoryManager = MemoryManager()
    declaration = memory_manager.get_variable(pid, line_num)
    address = declaration.get_memory_id()
    asm_code = set_register_const(REG.A, number)
    asm_code.extend(set_register_const(REG.B, address))
    asm_code.append(makeInstr('STORE', REG.B.value))
    declaration.is_initialized = True
    return asm_code


# TODO: Dostosowac do procedur
def pid_assign_pid(left_pid, right_pid, line_number, parent_proc=None):
    memory_manager: MemoryManager = MemoryManager()
    l_declaration = memory_manager.get_variable(left_pid, line_number)
    r_declaration = memory_manager.get_variable(right_pid, line_number)
    if not r_declaration.is_initialized:
        raise MemoryManagerException("Blad w linii %i: nizainicjowana zmienna %s" % (line_number, right_pid))
    l_address = l_declaration.get_memory_id()
    r_address = r_declaration.get_memory_id()
    asm_code = set_register_const(REG.E, r_address)  # adres zmiennej right_pid w reg e
    asm_code.append(makeInstr('LOAD', REG.E.value))
    asm_code.extend(set_register_const(REG.B, l_address))
    asm_code.append(makeInstr('STORE', REG.B.value))
    l_declaration.is_initialized = True
    return asm_code


# TODO: Dostosowac do wywolan z wnetrzna innych procedur
def proc_call(proc_pid, params: List[ProcCallParam], line_number, parent_proc=None):
    memory_manager: MemoryManager = MemoryManager()
    asm_code = []
    if parent_proc is not None:
        called_procedure = memory_manager.get_procedure(proc_pid, line_number)
        called_proc_label = called_procedure.label
        parent_procedure = memory_manager.get_procedure(parent_proc, line_number)
        parent_proc_label = parent_procedure.label
        if called_proc_label >= parent_proc_label:
            raise MemoryManagerException("Blad w linii %i: Procedura %s nie jest zdefiniowana" %
                                         (line_number, proc_pid))
        params_pattern_list = called_procedure.params_declarations
        n_passed = len(params)
        n_pattern = len(params_pattern_list)
        if n_passed != n_pattern:
            raise ProcCallException("Blad w linii %i: Podano nieprawidlowa liczbe parametrow procedury %s" %
                                    (line_number, proc_pid))

        for i in range(n_pattern):
            passed_param_id = parent_proc + "##" + params[i].pid
            passed_param_variable = memory_manager.get_variable(passed_param_id, params[i].line_number)
            if passed_param_variable.is_local:
                passed_param_address = passed_param_variable.memory_id
                asm_code.extend(set_register_const(REG.A, passed_param_address))
                proc_param_id = proc_pid + "##" + params_pattern_list[i].pid
                proc_param_declaration = memory_manager.get_variable(proc_param_id, line_number)
                if proc_param_declaration.must_be_initialized and (not passed_param_variable.is_initialized):
                    raise MemoryManagerException("Blad w linii %i: Proba uzycia niezainicjalizowanej zmiennej %s" %
                                                 (proc_param_declaration.uninitialized_usage_line,
                                                  params_pattern_list[i].pid))
                proc_param_address = proc_param_declaration.memory_id
                asm_code.extend(set_register_const(REG.B, proc_param_address))
                asm_code.append(makeInstr('STORE', REG.B.value))

            elif passed_param_variable.is_param:
                formal_param_address = passed_param_variable.memory_id
                asm_code.extend(set_register_const(REG.B, formal_param_address))
                asm_code.append(makeInstr('LOAD', REG.B.value))
                proc_param_id = proc_pid + "##" + params_pattern_list[i].pid
                proc_param_declaration = memory_manager.get_variable(proc_param_id, line_number)
                if proc_param_declaration.must_be_initialized and ((not passed_param_variable.is_initialized)
                                                                   and (not passed_param_variable.must_be_initialized)):
                    passed_param_variable.set_uninitialized_error(line_number)

                proc_param_address = proc_param_declaration.memory_id
                asm_code.extend(set_register_const(REG.B, proc_param_address))
                asm_code.append(makeInstr('STORE', REG.B.value))

            else:
                raise ProcCallException("Nieprawidlowe zagniezdzone wywolanie procedury")

            asm_code.extend(set_register_const(REG.C, 4))
            return_address = called_procedure.activation_record_start
            asm_code.extend(set_register_const(REG.B, return_address))
            asm_code.append(makeInstr('STRK', REG.A.value))
            asm_code.append(makeInstr('ADD', REG.C.value))
            asm_code.append(makeInstr('STORE', REG.B.value))
            asm_code.append(makeInstr('JUMP', proc_pid + ":"))

    else:
        procedure = memory_manager.get_procedure(proc_pid, line_number)
        params_pattern_list = procedure.params_declarations
        n_passed = len(params)
        n_pattern = len(params_pattern_list)
        if n_passed != n_pattern:
            raise ProcCallException("Blad w linii %i: Podano nieprawidlowa liczbe parametrow procedury %s" %
                                    (line_number, proc_pid))

        for i in range(n_pattern):
            passed_param_variable = memory_manager.get_variable(params[i].pid, params[i].line_number)
            passed_param_address = passed_param_variable.memory_id
            asm_code.extend(set_register_const(REG.A, passed_param_address))
            proc_param_id = proc_pid + "##" + params_pattern_list[i].pid
            proc_param_declaration = memory_manager.get_variable(proc_param_id, line_number)
            if proc_param_declaration.must_be_initialized and (not passed_param_variable.is_initialized):
                raise MemoryManagerException("Blad w linii %i: Proba uzycia niezainicjalizowanej zmiennej %s" %
                                             (proc_param_declaration.uninitialized_usage_line,
                                              params_pattern_list[i].pid))
            proc_param_address = proc_param_declaration.memory_id
            asm_code.extend(set_register_const(REG.B, proc_param_address))
            asm_code.append(makeInstr('STORE', REG.B.value))

        asm_code.extend(set_register_const(REG.C, 4))
        return_address = procedure.activation_record_start
        asm_code.extend(set_register_const(REG.B, return_address))
        asm_code.append(makeInstr('STRK', REG.A.value))
        asm_code.append(makeInstr('ADD', REG.C.value))
        asm_code.append(makeInstr('STORE', REG.B.value))
        asm_code.append(makeInstr('JUMP', proc_pid + ":"))

    return asm_code


def proc_return(proc_pid, line_number):
    memory_manager: MemoryManager = MemoryManager()
    procedure = memory_manager.get_procedure(proc_pid, line_number)
    return_address = procedure.activation_record_start
    asm_code = set_register_const(REG.B, return_address)
    asm_code.append(makeInstr('LOAD', REG.B.value))
    asm_code.append(makeInstr('JUMPR', REG.A.value))
    for decl in procedure.local_declarations:
        decl.is_initialized = False
    return asm_code


def set_register_const(reg, val):
    asm_code = [RST(reg)]

    bin_val = bin(val)[2:]  # number to binary representation
    length = len(bin_val)  # how many digits
    for i, digit in enumerate(bin_val):
        if digit == '1':
            asm_code.append(INC(reg))  # reg = reg + 1
        if i < length - 1:
            asm_code.append(SHL(reg))  # reg = reg << 1
    return asm_code


def HALT(p):
    return makeInstr('HALT')


# def LOAD_NUMBER_VALUE_TO_REGISTER( number, reg):
#     set_register_const( reg, number)


class ProcCallException(Exception):
    def __init__(self, msg):
        self.message = msg
