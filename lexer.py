import ply.lex as lex
from ply.lex import TOKEN

reserved = {
    'PROGRAM': 'PROGRAM',
    'IN': 'IN',
    'IS': 'IS',
    'END': 'END',
    'READ': 'READ',
    'WRITE': 'WRITE'
}

tokens = ['ASSIGN', 'SEMICOLON', 'COMMA', 'num', 'pid'] + list(reserved.values())

t_ignore = ' \t'
t_SEMICOLON = r';'
t_COMMA = r','
t_ASSIGN = r':='
t_pid = r'[_a-z]+'


def t_comment(t):
    r'\#(.*?(\\\n)*)+\n'
    t.lexer.lineno += 1


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_num(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_error(t):
    raise Exception("Illegal character '%s' at line %i" % (t.value[0], t.lineno))


reserved_re = '|'.join(reserved.values())


@TOKEN(reserved_re)
def t_control(t):
    control_token = reserved.get(t.value)
    if not control_token:
        raise SyntaxError("Bad control sequence '%s'" % t.value)
    t.type = control_token
    return t


lexer = lex.lex()



