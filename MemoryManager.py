from NonTerminals.Declarations import VarDeclaration


class MemoryManager:

    _instance = None
    symbol_table = dict()
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

    def add_variable(self, declaration: VarDeclaration):
        if declaration.pid in self.symbol_table:
            raise MemoryManagerException(f"Redeklaracja zmiennej + {declaration.pid}")
        else:
            declaration.set_memory_id(self.allocate_variable())
            self.symbol_table.update({declaration.pid: declaration})

    def get_address(self, pid):
        try:
            declaration = self.symbol_table[pid]
            return declaration.get_memory_id()
        except KeyError:
            raise MemoryManagerException(f"Proba uzycia niezadeklaroanej zmiennej: {pid}")

    def get_variable(self, pid):
        try:
            declaration: VarDeclaration = self.symbol_table[pid]
            return declaration
        except KeyError:
            raise MemoryManagerException(f"Proba uzycia niezadeklaroanej zmiennej: {pid}")


class MemoryManagerException(Exception):
    def __init__(self, msg):
        self.message = msg

