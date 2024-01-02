from NonTerminals.ProcHead import ProcHead
from typing import List
from NonTerminals.Declarations import VarDeclaration
from NonTerminals.Command import Command


class Procedure:
    def __init__(self, proc_head: ProcHead, local_declarations: List[VarDeclaration],
                 commands: List[Command]):
        self.pid = proc_head.pid
        self.line_number = proc_head.line_number
        self.params_declarations = proc_head.args_declarations
        for declaration in local_declarations:
            declaration.is_local = True
            declaration.parent_procedure = self.pid
        self.local_declarations = local_declarations
        self.commands = commands
        self.instructions = []
        self.activation_record_start = -1
        self.head = proc_head
        self.label = -1

    def set_activation_record(self, start_id):
        self.activation_record_start = start_id
