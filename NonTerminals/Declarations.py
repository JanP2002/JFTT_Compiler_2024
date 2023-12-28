from MemoryManager import memory_manager
from MemoryManager import MemoryManagerException

# class Declarations():
#     def __init__(self, decl_list):
#         self.declarations = decl_list
#
#     # def append_var_declaration(self, pid):
#     #     var_decl = VarDeclaration(self.memory_manager, pid)
#     #     self.declarations.append(var_decl)


class VarDeclaration:
    def __init__(self, pid, is_arr=False, is_local=False, line_number=-1):
        self.pid = pid
        self.line_number = line_number
        self.is_array = is_arr
        self.is_local = is_local
        self.memory_id = None
        self.length = 1
        self.is_initialized = False

    def initialize(self):
        #TODO:
        pass

    def is_array(self):
        return self.is_array == True

    def to_string(self):
        return str((self.pid, self.memory_id, self.length, "Array" if self.is_array else "Var"))


class ArrayDeclaration(VarDeclaration):
    def __init__(self, pid, array_beg, array_end, is_local=False, line_number=-1):
        super(VarDeclaration, self).__init__(pid, True, is_local, line_number)
        if array_beg > array_end:
            raise MemoryManagerException("Nieprawidlowy zakres tablicy %s(%i, %i) w linii %i" %
                                         (pid, array_beg, array_end, line_number))
        self.array_beg = array_beg
        self.array_end = array_end
        self.length = array_end - array_beg + 1



