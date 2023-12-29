from lexer import lexer, tokens
import ply.yacc as yacc
from Program import Program
from NonTerminals.Main import Main
from NonTerminals.Command import CommandWriteNum, CommandWritePid, CommandReadPid, CommandPidAssignNumber, \
    CommandPidAssignPid
from NonTerminals.Declarations import VarDeclaration
from MemoryManager import MemoryManager



def p_program_all_main(p):
    """program_all : main"""
    p[0] = Program(p[1])


# def p_procedues_wih_decl(p):
#     """procedures: empy"""

def p_main_commands(p):
    """main : PROGRAM IS IN commands END"""
    p[0] = Main([], p[4])


def p_main_declarations_commands(p):
    """main : PROGRAM IS declarations IN commands END"""
    # print(*p[3])
    p[0] = Main(p[3], p[5])


def p_declarations_append(p):
    """declarations : declarations COMMA pid"""
    if not p[1]:
        p[1] = []
    decl1 = VarDeclaration(p[3], False, False, -1)
    p[1].append(decl1)
    p[0] = p[1]


def p_declerations(p):
    """declarations : pid"""
    p[0] = [VarDeclaration( p[1], False, False, -1)]

def p_commands_append(p):
    """commands  : commands command"""
    if not p[1]:
        p[1] = []
    p[1].append(p[2])
    p[0] = p[1]


def p_commands(p):
    """commands  : command"""
    p[0] = [p[1]]


def p_command_write_num(p):
    """command  : WRITE num SEMICOLON"""
    p[0] = CommandWriteNum(p[2])


def p_command_write_pid(p):
    """command  : WRITE pid SEMICOLON"""
    p[0] = CommandWritePid(p[2])


def p_command_read_pid(p):
    """command : READ pid SEMICOLON"""
    p[0] = CommandReadPid(p[2])


def p_command_pid_assign_num(p):
    """command  : pid ASSIGN num SEMICOLON"""
    # p[0] = CommandAssign(p[1], p[3], line=p.lineno(2))
    p[0] = CommandPidAssignNumber(p[1], p[3], p.lineno(2))


def p_command_pid_assign_pid(p):
    """command  : pid ASSIGN pid SEMICOLON"""
    # p[0] = CommandAssign(p[1], p[3], line=p.lineno(2))
    p[0] = CommandPidAssignPid(p[1], p[3], p.lineno(2))


def p_error(p):
    raise SyntaxError("Unexpected token '%s' at line %i" % (p.value, p.lineno))


parser = yacc.yacc()
