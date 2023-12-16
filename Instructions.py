from Register import REG


def GET(p, reg):
    p.makeInstr('GET', reg)


def STORE(p, reg):
    p.makeInstr('STORE', reg)


def LOAD(p, reg):
    p.makeInstr('LOAD', reg)


def INC(p, reg):
    p.makeInstr('INC', reg)


def JUMP(p, j):
    p.makeInstr('JUMP', j)


def DEC(p, X):
    p.makeInstr('DEC', X)

def ADD(p, X, Y):
    p.makeInstr('ADD', X, Y)

def SHL(p, X):
    p.makeInstr('SHL', X)

def SHR(p, X):
    p.makeInstr('SHR', X)

def SUB(p, X, Y):
    p.makeInstr('SUB', X, Y)

def RST(p, X):
    p.makeInstr('RST', X)


def evalToRegInstr(value, p, reg):
        set_register_const(p, reg, value)

def WRITE(p, value):
    # evalToRegInstr(value, p, REG.A)
    set_register_const(p, REG.A, value)
    p.makeInstr('WRITE')



def set_register_const(p, reg, val):
    RST(p, reg)

    bin_val = bin(val)[2:]   # number to binary representation
    length = len(bin_val)    # how many digits
    for i, digit in enumerate(bin_val):
        if digit == '1':
            INC(p, reg)         # reg = reg + 1
        if i < length - 1:
            SHL(p, reg)   # reg = reg << 1


# def LOAD_NUMBER_VALUE_TO_REGISTER(p, number, reg):
#     set_register_const(p, reg, number)