from lexer import lexer, tokens
import ply.yacc as yacc

#test
def program_all_main():
    """program_all : main"""


def main():
    """START declarations IN commands END |
    START IN commands END"""


def p_declarations_empty(p):
    """declarations : """
    p[0] = []


def p_commands_append(p):
    """commands  : commands command"""
    if not p[1]:
        p[1] = []
    p[1].append(p[2])
    p[0] = p[1]


def p_commands(p):
    """commands  : command"""
    p[0] = [p[1]]


# def p_command_ASSIGN(p):
#     """command  : identifier ASSIGN expression SEMICOLON"""
#     # p[0] = CommandAssign(p[1], p[3], line=p.lineno(2))

def p_command_READ(p):
    """command  : READ identifier SEMICOLON"""
    # p[0] = CommandRead(p[2])


def p_command_WRITE(p):
    """command  : WRITE value SEMICOLON"""
    # p[0] = CommandWrite(p[2])


def p_expression_value(p):
    """expression   : value"""
    p[0] = p[1]


def p_value_identifier(p):
    """value    : identifier"""
    # p[0] = ValueFromIdentifier(p[1], lineNumber=p.lineno(1))


def p_value_num(p):
    """value    : num"""
    # p[0] = Number(p[1])


def p_identifier(p):
    """identifier   : pid"""
    # p[0] = Identifier(p[1])


def p_error(p):
    raise SyntaxError("Unexpected token '%s' at line %i" % (p.value, p.lineno))


parser = yacc.yacc()

