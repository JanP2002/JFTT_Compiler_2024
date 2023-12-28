
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

    def is_array(self):
        return self.is_array

    def to_string(self):
        return str((self.pid, self.memory_id, self.length, "Array" if self.is_array else "Var"))

    def set_memory_id(self, mem_id):
        self.memory_id = mem_id

    def get_memory_id(self):
        return self.memory_id


class ArrayDeclaration(VarDeclaration):
    def __init__(self, pid, array_beg, array_end, is_local=False, line_number=-1):
        super(VarDeclaration, self).__init__(pid, True, is_local, line_number)
        if array_beg > array_end:
            raise ArrayRangeException("Nieprawidlowy zakres tablicy %s(%i, %i) w linii %i" % (pid, array_beg, array_end,
                                                                                              line_number))
        self.array_beg = array_beg
        self.array_end = array_end
        self.length = array_end - array_beg + 1


class ArrayRangeException(Exception):
    def __init__(self, msg):
        self.message = msg
