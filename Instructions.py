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

def WRITE(value):
    # evalToRegInstr(value,  REG.A)
    asm_code = set_register_const( REG.A, value)
    print(type(asm_code))
    print(type(makeInstr('WRITE')))
    asm_code.append(makeInstr('WRITE'))
    return asm_code



def set_register_const( reg, val):
    asm_code = []
    asm_code.append(RST(reg))

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