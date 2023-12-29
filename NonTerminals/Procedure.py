from NonTerminals.ProcHead import ProcHead
from typing import List
from NonTerminals.Declarations import VarDeclaration
from NonTerminals.Command import Command


class Procedure:
    def __init__(self, proc_head: ProcHead, local_declarations: List[VarDeclaration],
                 commands: List[Command], line_number=-1):
        self.pid = proc_head.pid
        self.line_number = line_number
        self.params_declarations = proc_head.args_declarations
        self.local_declarations = local_declarations
        self.commands = commands
        self.instructions = []

    def process_commands(self):
        for com in self.commands:
            self.instructions.extend(com.translate(self))

    def translate(self):
        return self.instructions
