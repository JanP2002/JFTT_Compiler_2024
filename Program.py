from Instructions import HALT, JUMP
from MemoryManager import MemoryManager


class Program:

    def __init__(self, procedures, main):
        self.procedures = procedures
        self.main = main
        self.instructions = []
        self.counter = 0
        memory_manager: MemoryManager = MemoryManager()
        for proc in procedures:
            activation_record_start = memory_manager.add_procedure(proc.head)
            proc.activation_record_start = activation_record_start
            memory_manager.procedures_table.update({proc.pid: proc})
            memory_manager.add_proc_params(proc.params_declarations)
            memory_manager.add_proc_local_variables(proc.local_declarations)

        memory_manager.add_variables(main.declarations)
        # main.process_commands()
        memory_manager.print_procedures_table()
        memory_manager.print_symbol_table()

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
        # self.instructions.extend(self.main.translate())
        for com in self.main.commands:
            self.instructions.extend(com.translate(self.main))

        self.instructions.append(HALT(self))
        return self.instructions

    def get_asm_code(self):
        asm_list = self.translate()
        asm_code = ""
        for w in asm_list:
            asm_code += w + "\n"
        return asm_code

