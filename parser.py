from NonTerminals.Condition import Condition, ConditionNumNum, ConditionNumPid, ConditionPidNum, ConditionPidPid
from NonTerminals.ProcCallParam import ProcCallParam
from NonTerminals.ProcHead import ProcHead
from NonTerminals.Procedure import Procedure
from lexer import lexer, tokens
import ply.yacc as yacc
from Program import Program
from NonTerminals.Main import Main
from NonTerminals.Command import CommandWriteNum, CommandWritePid, CommandReadPid, CommandPidAssignNumber, \
    CommandPidAssignPid, ProcCall, CommandPidAssignNumOpNum, CommandIf
from NonTerminals.Declarations import VarDeclaration, VarParamDeclaration


def p_program_all_procedures_main(p):
    """program_all : procedures main"""
    p[0] = Program(p[1], p[2])


def p_procedures_declarations_commands(p):
    """procedures : procedures PROCEDURE proc_head IS declarations IN commands END"""
    if not p[1]:
        p[1] = []

    curr_procedure = Procedure(p[3], p[5], p[7])
    p[1].append(curr_procedure)
    p[0] = p[1]


def p_procedures_commands(p):
    """procedures : procedures PROCEDURE proc_head IS IN commands END"""
    if not p[1]:
        p[1] = []

    curr_procedure = Procedure(p[3], [], p[6])
    p[1].append(curr_procedure)
    p[0] = p[1]


def p_procedures_empty(p):
    """procedures : """
    p[0] = []


def p_proc_head(p):
    """proc_head : pid l_paren args_decl r_paren"""
    p[0] = ProcHead(p[1], p[3], p.lineno(1))


def p_proc_call(p):
    """proc_call : pid l_paren args r_paren"""
    p[0] = ProcCall(p[1], p[3], p.lineno(1))


def p_args_decl_append(p):
    """args_decl : args_decl COMMA pid"""
    if not p[1]:
        p[1] = []
    decl1 = VarParamDeclaration(p[3], False, p.lineno(2))
    p[1].append(decl1)
    p[0] = p[1]


def p_args_decl(p):
    """args_decl : pid"""
    p[0] = [VarParamDeclaration(p[1], False, p.lineno(1))]


def p_args_append(p):
    """args : args COMMA pid"""
    if not p[1]:
        p[1] = []
    param1 = ProcCallParam(p[3], p.lineno(2))
    p[1].append(param1)
    p[0] = p[1]


def p_args(p):
    """args : pid"""
    p[0] = [ProcCallParam(p[1], p.lineno(1))]


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
    decl1 = VarDeclaration(p[3], False, p.lineno(2))
    p[1].append(decl1)
    p[0] = p[1]


def p_declarations(p):
    """declarations : pid"""
    p[0] = [VarDeclaration(p[1], False, p.lineno(1))]


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
    p[0] = CommandWritePid(p[2], p.lineno(2))


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


def p_command_pid_assign_num_op_num(p):
    """command : pid ASSIGN num op num SEMICOLON"""
    p[0] = CommandPidAssignNumOpNum(p[1], p[3], p[5], p[4], p.lineno(2))


def p_command_if(p):
    """command : IF condition THEN commands ENDIF"""
    p[0] = CommandIf(p[2], p[4], p.lineno(1))


def p_condition_num_num(p):
    """condition : num cop num"""
    p[0] = ConditionNumNum(p[1], p[3], p[2], p.lineno(1))


def p_condition_num_pid(p):
    """condition : num cop pid"""
    p[0] = ConditionNumPid(p[1], p[3], p[2], p.lineno(1))


def p_condition_pid_num(p):
    """condition : pid cop num"""
    p[0] = ConditionPidNum(p[1], p[3], p[2], p.lineno(1))


def p_condition_pid_pid(p):
    """condition : pid cop pid"""
    p[0] = ConditionPidPid(p[1], p[3], p[2], p.lineno(1))


def p_cop(p):
    """cop : LT
    | GT
    | LE
    | GE
    | EQ
    | NE"""
    p[0] = p[1]


def p_command_proc_call(p):
    """command : proc_call SEMICOLON"""
    p[0] = p[1]


def p_error(p):
    raise SyntaxError("Unexpected token '%s' at line %i" % (p.value, p.lineno))


parser = yacc.yacc()
