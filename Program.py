import Instructions
from Instructions import HALT, JUMP, proc_return
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
        self.instructions.append(JUMP("main:"))
        for proc in self.procedures:
            proc.label = len(self.instructions)
            for com in proc.commands:
                com.set_parent_procedure(proc.pid)
                self.instructions.extend(com.translate(proc))
            self.instructions.extend(proc_return(proc.pid, proc.line_number))

        first_comm = self.main.commands[0].translate(self.main)
        first_comm[0] = "main: " + first_comm[0]
        self.instructions.extend(first_comm)
        for i in range(1, len(self.main.commands)):
            self.instructions.extend(self.main.commands[i].translate(self.main))

        self.instructions.append(HALT(self))
        return self.instructions

    def get_asm_code(self):
        asm_list_labels = self.translate()
        asm_list = []
        tmp_label = None
        for code_line in asm_list_labels:
            line_list = code_line.split()
            if not line_list[0] == 'LABEL':
                if tmp_label is None:
                    asm_list.append(code_line)
                else:
                    code_tmp = tmp_label + " " + code_line
                    asm_list.append(code_tmp)
                    tmp_label = None
            else:
                tmp_label = line_list[1]

        for proc in self.procedures:
            asm_list[proc.label] = proc.pid + ": " + asm_list[proc.label]
        labels_dict = dict()
        jump_usages = []
        jzero_usages = []
        jpos_usages = []
        for i in range(len(asm_list)):
            line_list = asm_list[i].split()
            if line_list[0].endswith(":"):
                labels_dict.update({line_list[0][:-1]: i})
                asm_list[i] = asm_list[i].split(" ", 1)[1]#usuniecie etykiety
            elif line_list[0] == 'JUMP' and line_list[1].endswith(":"):
                jump_usages.append(i)
            elif line_list[0] == 'JZERO' and line_list[1].endswith(":"):
                jzero_usages.append(i)
            elif line_list[0] == 'JPOS' and line_list[1].endswith(":"):
                jpos_usages.append(i)
        for usage in jump_usages:
            line_list = asm_list[usage].split()
            label_value = labels_dict[line_list[1][:-1]]
            asm_list[usage] = Instructions.makeInstr('JUMP', label_value)
        for usage in jzero_usages:
            line_list = asm_list[usage].split()
            label_value = labels_dict[line_list[1][:-1]]
            asm_list[usage] = Instructions.makeInstr('JZERO', label_value)
        for usage in jpos_usages:
            line_list = asm_list[usage].split()
            label_value = labels_dict[line_list[1][:-1]]
            asm_list[usage] = Instructions.makeInstr('JPOS', label_value)

        asm_code = ""
        for w in asm_list:
            asm_code += w + "\n"
        return asm_code

