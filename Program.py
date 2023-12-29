from Instructions import HALT, JUMP


class Program:

    def __init__(self, procedures, main):
        self.procedures = procedures
        self.main = main
        self.instructions = []
        self.counter = 0

    def get_counter(self):
        return self.counter

    def inc_counter(self):
        self.counter += 1
        return self

    # def add_future_instr(self, future):
    #     self.inc_counter()
    #     self.instructions.append(future)
    #     return self.counter - 1

    def translate(self):
        self.instructions.append(JUMP(":main"))
        self.instructions.extend(self.main.translate())
        self.instructions.append(HALT(self))
        return self.instructions

    def get_asm_code(self):
        asm_list = self.translate()
        asm_code = ""
        for w in asm_list:
            asm_code += w + "\n"
        return asm_code

