from NonTerminals.Declarations import VarDeclaration, VarParamDeclaration
from typing import List
from NonTerminals.ProcHead import ProcHead


class MemoryManager:

    _instance = None
    symbol_table = dict()
    procedures_table = dict()
    next_free = 0

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass

    def allocate_variable(self):
        self.next_free += 1
        return self.next_free-1

    def add_procedure(self, proc_head: ProcHead):
        if proc_head.pid in self.procedures_table:
            raise MemoryManagerException(
                f"Blad w linii {proc_head.line_number}: Redeklaracja procedury {proc_head.pid}")
        else:
            activation_record = self.allocate_variable()
            return activation_record

    def add_variables(self, declarations: List[VarDeclaration]):
        for declaration in declarations:
            if declaration.pid in self.symbol_table:
                raise MemoryManagerException(
                    f"Blad w linii {declaration.line_number}: Redeklaracja zmiennej {declaration.pid}")
            else:
                declaration.set_memory_id(self.allocate_variable())
                self.symbol_table.update({declaration.pid: declaration})

    def add_variable(self, declaration: VarDeclaration, line_number):
        if declaration.pid in self.symbol_table:
            raise MemoryManagerException(
                f"Blad w linii {line_number}: Redeklaracja zmiennej + {declaration.pid}")
        else:
            declaration.set_memory_id(self.allocate_variable())
            self.symbol_table.update({declaration.pid: declaration})

    def add_proc_local_variables(self, declarations: List[VarDeclaration]):
        for declaration in declarations:
            parent_proc = declaration.parent_procedure
            variable_id = parent_proc + "##" + declaration.pid
            if variable_id in self.symbol_table:
                raise MemoryManagerException(
                    f"Blad w linii {declaration.line_number}: Redeklaracja zmiennej + {declaration.pid}")
            else:
                declaration.set_memory_id(self.allocate_variable())
                self.symbol_table.update({variable_id: declaration})

    def add_proc_params(self, declarations: List[VarParamDeclaration]):
        for declaration in declarations:
            parent_proc = declaration.parent_procedure
            param_id = parent_proc + "##" + declaration.pid
            if param_id in self.symbol_table:
                raise MemoryManagerException(
                    f"Blad w linii {declaration.line_number}: Redeklaracja zmiennej + {declaration.pid}")
            else:
                declaration.set_memory_id(self.allocate_variable())
                self.symbol_table.update({param_id: declaration})

    def get_address(self, pid, line_number):
        try:
            declaration = self.symbol_table[pid]
            return declaration.get_memory_id()
        except KeyError:
            raise MemoryManagerException(
                f"Blad w linii {line_number}: Proba uzycia niezadeklaroanej zmiennej: {pid}")

    def get_variable(self, pid, line_number):
        try:
            declaration: VarDeclaration = self.symbol_table[pid]
            return declaration
        except KeyError:
            raise MemoryManagerException(
                f"Blad w linii {line_number}: Proba uzycia niezadeklaroanej zmiennej: {pid}")

    def print_symbol_table(self):
        print("Tablica symboli:")
        for key, value in self.symbol_table.items():
            print(f"Klucz: {key}, Wartość: {value}")

    def print_procedures_table(self):
        print("Tablica procedur:")
        for key, value in self.procedures_table.items():
            print(f"Klucz: {key}, Wartość: {value}")


class MemoryManagerException(Exception):
    def __init__(self, msg):
        self.message = msg

