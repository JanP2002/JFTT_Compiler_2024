class MemoryManager:
    def __init__(self):
        self.symbol_table = dict()
        self.next_free = 0

    def allocate_variable(self):
        self.next_free += 1
        return self.next_free-1

    def add_variable(self, pid):
        if pid in self.symbol_table:
            raise MemoryManagerException(f"Redeklaracja zmiennej + {pid}")
        else:
            self.symbol_table.update({pid: self.allocate_variable()})

    def get_address(self, pid):
        #TODO: Obsluga wyjatku
        return self.symbol_table.get(pid)


class MemoryManagerException(Exception):
    def __init__(self, msg):
        self.message = msg
