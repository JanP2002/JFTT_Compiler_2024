from MemoryManager import MemoryManager
from MemoryManager import MemoryManagerException
from Register import REG


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


def DEC( X):
    return makeInstr('DEC', X)

def ADD( X, Y):
    return makeInstr('ADD', X, Y)

def SHL( X):
    return makeInstr('SHL', X)

def SHR( X):
    return makeInstr('SHR', X)

def SUB( X, Y):
    return makeInstr('SUB', X, Y)

def RST( X):
    return makeInstr('RST', X)


def evalToRegInstr(value,  reg):
    return set_register_const( reg, value)


def write_num(num: int):
    # evalToRegInstr(value,  REG.A)
    asm_code = set_register_const( REG.A,num)
    asm_code.append(makeInstr('WRITE'))
    return asm_code


def write_pid(pid, line_number, parent_proc=None):
    memory_manager: MemoryManager = MemoryManager()
    declaration = memory_manager.get_variable(pid, line_number)
    if not declaration.is_initialized:
        raise MemoryManagerException("Blad w linii %i: Zmienna %s nie jest zainicjalizowana" %
                                     (line_number, declaration.pid))
    address = declaration.get_memory_id()
    asm_code = set_register_const(REG.B, address)
    asm_code.append(makeInstr('LOAD', REG.B.value))
    asm_code.append(makeInstr('WRITE'))
    return asm_code


def read_pid(pid, line_number, parent_proc=None):
    memory_manager: MemoryManager = MemoryManager()
    declaration = memory_manager.get_variable(pid, line_number)
    address = declaration.get_memory_id()
    asm_code = [makeInstr('READ')]
    asm_code.extend(set_register_const(REG.B, address))
    asm_code.append(makeInstr('STORE', REG.B.value))
    declaration.is_initialized = True
    return asm_code


def pid_assign_number(pid, number, line_num, parent_proc=None):
    memory_manager: MemoryManager = MemoryManager()
    declaration = memory_manager.get_variable(pid, line_num)
    address = declaration.get_memory_id()
    asm_code = set_register_const(REG.A, number)
    asm_code.extend(set_register_const(REG.B, address))
    asm_code.append(makeInstr('STORE', REG.B.value))
    declaration.is_initialized = True
    return asm_code


def pid_assign_pid(left_pid, right_pid, line_number, parent_proc=None):
    memory_manager: MemoryManager = MemoryManager()
    l_declaration = memory_manager.get_variable(left_pid, line_number)
    r_declaration = memory_manager.get_variable(right_pid, line_number)
    if not r_declaration.is_initialized:
        raise MemoryManagerException("Blad w linii %i: nizainicjowana zmienna %s" % (line_number, right_pid))
    l_address = l_declaration.get_memory_id()
    r_address = r_declaration.get_memory_id()
    asm_code = set_register_const(REG.E, r_address)#adres zmiennej right_pid w reg e
    asm_code.append(makeInstr('LOAD', REG.E.value))
    asm_code.extend(set_register_const(REG.B, l_address))
    asm_code.append(makeInstr('STORE', REG.B.value))
    l_declaration.is_initialized = True
    return asm_code


def set_register_const( reg, val):
    asm_code = [RST(reg)]

    bin_val = bin(val)[2:]   # number to binary representation
    length = len(bin_val)    # how many digits
    for i, digit in enumerate(bin_val):
        if digit == '1':
            asm_code.append(INC( reg))         # reg = reg + 1
        if i < length - 1:
            asm_code.append(SHL( reg))   # reg = reg << 1
    return asm_code


def HALT(p):
    return makeInstr('HALT')
# def LOAD_NUMBER_VALUE_TO_REGISTER( number, reg):
#     set_register_const( reg, number)
