from lexer import lexer, tokens
import ply.yacc as yacc
from Program import Program
from NonTerminals.Main import Main
from NonTerminals.Command import CommandWrite
from MemoryManager import MemoryManager
from NonTerminals.Declarations import Declarations
from NonTerminals.Declarations import VarDeclaration

memory_Manager = MemoryManager()
# register_Manager = RegisterManager()
def p_program_all_main(p):
    """program_all : main"""
    p[0] = Program(p[1], memory_Manager)


# def p_procedues_wih_decl(p):
#     """procedures: empy"""

def p_main_commands(p):
    """main : PROGRAM IS IN commands END"""
    p[0] = Main([], p[4], memory_Manager)


def p_main_declarations_commands(p):
    """main : PROGRAM IS declarations IN commands END"""
    declarations = Declarations(p[3])
    print(p[5])
    p[0] = Main(declarations, p[5], memory_Manager)


def p_declarations_append(p):
    """declarations : declarations pid"""
    if not p[1]:
        p[1] = []

    p[1].append( VarDeclaration( p[2] ))
    p[0] = p[1]

def p_declerations(p):
    """declarations : pid"""
    p[0] = [VarDeclaration( p[1] )]

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

# def p_command_READ(p):
#     """command  : READ identifier SEMICOLON"""
#     # p[0] = CommandRead(p[2])


def p_command_WRITE(p):
    """command  : WRITE value SEMICOLON"""
    p[0] = CommandWrite(p[2])


# def p_expression_value(p):
#     """expression   : value"""
#     p[0] = p[1]


# def p_value_identifier(p):
#     """value    : identifier"""
#     # p[0] = ValueFromIdentifier(p[1], lineNumber=p.lineno(1))


def p_value_num(p):
    """value   : num"""
    p[0] = p[1]


# def p_identifier(p):
#     """identifier   : pid"""
#     # p[0] = Identifier(p[1])


def p_error(p):
    raise SyntaxError("Unexpected token '%s' at line %i" % (p.value, p.lineno))


parser = yacc.yacc()
