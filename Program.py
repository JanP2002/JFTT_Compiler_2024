from Instructions import HALT, JUMP


class Program:

    def __init__(self, main):
        self.main = main
        # self.memory_manager = memory_manager
        self.instructions = []
        self.counter = 0



    def get_counter(self):
        return self.counter

    # def init_symbol_table(self):
    #     pass

    def inc_counter(self):
        self.counter += 1
        return self

    # def add_future_instr(self, future):
    #     self.inc_counter()
    #     self.instructions.append(future)
    #     return self.counter - 1

    # def makeInstr(self, instr, X="", Y=""):
    #     instr_str = "%s %s %s" % (instr, X, Y)
    #     self.inc_counter()
    #     self.instructions.append(instr_str)


    # def translate(self):
    #     return '\n'.join(self.instructions + ["HALT"])

    def translate(self):
        # self.instructions.join()
        # '\n'.join(self.instructions + HALT(self))
        # return self.main.translate().join()
        self.instructions.append(JUMP(":main"))
        self.instructions.extend(self.main.translate())
        self.instructions.append(HALT(self))
        # ins = '\n'.join(JUMP(self, ":main"))
        # asm_code.join(self.main.translate() + HALT(self))
        return self.instructions

    def get_asm_code(self):
        asm_list = self.translate()
        asm_code = ""
        for w in asm_list:
            asm_code += w + "\n"
        return asm_code

