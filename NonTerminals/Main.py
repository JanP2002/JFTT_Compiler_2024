class Main:

    def __init__(self, declarations, commands):
        self.declarations = declarations
        self.commands = commands
        self.instructions = []
        self.counter = 0
        self.process_commands()

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

    def makeInstr(self, instr, X, Y=""):
        instrStr = "%s %s %s" % (instr, X, Y)
        self.inc_counter()
        self.instructions.append(instrStr)

    def process_commands(self):
        for com in self.commands:
            com.translate(self)

    def generate_code(self):
        return '\n'.join(self.instructions + ["HALT"])