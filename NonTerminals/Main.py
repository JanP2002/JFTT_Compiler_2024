from MemoryManager import MemoryManager
class Main:

    def __init__(self, declarations, commands, m_manager: MemoryManager):
        self.declarations = declarations
        self.commands = commands
        self.instructions = []
        self.counter = 0
        self.process_commands()
        self.memory_manager = m_manager

    def get_counter(self):
        return self.counter

    def init_symbol_table(self):
        pass

    def inc_counter(self):
        self.counter += 1
        return self

    def add_future_instr(self, future):
        self.inc_counter()
        self.instructions.append(future)
        return self.counter - 1

    def makeInstr(self, instr, X="", Y=""):
        instr_str = "%s %s %s" % (instr, X, Y)
        self.inc_counter()
        self.instructions.append(instr_str)

    def process_commands(self):
        for com in self.commands:
            com.translate(self)

    def translate(self):
        return '\n'.join(self.instructions + ["HALT"])