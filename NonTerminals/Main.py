from MemoryManager import MemoryManager
class Main:

    def __init__(self, declarations, commands, m_manager: MemoryManager):
        self.memory_manager = m_manager
        self.declarations = declarations
        self.commands = commands
        self.instructions = []
        # self.asm_code = ""
        self.process_commands()





    # def add_future_instr(self, future):
    #     self.inc_counter()
    #     self.instructions.append(future)
    #     return self.counter - 1
    #
    # def makeInstr(self, instr, X="", Y=""):
    #     instr_str = "%s %s %s" % (instr, X, Y)
    #     self.inc_counter()
    #     self.instructions.append(instr_str)

    def process_commands(self):
        for com in self.commands:
            self.instructions.extend(com.translate(self))

    def translate(self):
        return self.instructions
