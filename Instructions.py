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

def SHL(p, X, Y):
    p.makeInstr('SHL', X, Y)

def SHR(p, X, Y):
    p.makeInstr('SHR', X, Y)

def SUB(p, X, Y):
    p.makeInstr('SUB', X, Y)

def RST(p, X):
    p.makeInstr('RST', X)

def WRITE(p, value):
    value.evalToRegInstr(p, REG.A)
    p.makeInstr('WRITE', value)

def set_register_const(p, reg, val):
    RST(p, reg)

    bin_val = bin(val)[2:]   # number to binary representation
    length = len(bin_val)    # how many digits
    for i, digit in enumerate(bin_val):
        if digit == '1':
            INC(p, reg)         # reg = reg + 1
        if i < length - 1:
            SHL(p, reg)   # reg = reg << 1