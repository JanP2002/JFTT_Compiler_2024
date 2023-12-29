class VarDeclaration:
    def __init__(self, pid, is_arr=False, line_number=-1):
        self.pid = pid
        self.line_number = line_number
        self.is_array = is_arr
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


class VarLocalDeclaration(VarDeclaration):
    def __init__(self, pid, is_array=False, line_number=-1, parent_function=None):
        super(VarDeclaration, self).__init__(pid, False, line_number)
        self.parent_function = parent_function


class VarParamDeclaration(VarDeclaration):
    def __init__(self, pid, is_array=False, line_number=-1, parent_function=None):
        super(VarDeclaration, self).__init__(pid, False, line_number)
        self.parent_function = parent_function


class ArrayDeclaration(VarDeclaration):
    def __init__(self, pid, array_beg, array_end, line_number=-1):
        super(VarDeclaration, self).__init__(pid, True, line_number)
        if array_beg > array_end:
            raise ArrayRangeException("Nieprawidlowy zakres tablicy %s(%i, %i) w linii %i" % (pid, array_beg, array_end,
                                                                                              line_number))
        self.array_beg = array_beg
        self.array_end = array_end
        self.length = array_end - array_beg + 1


class ArrayRangeException(Exception):
    def __init__(self, msg):
        self.message = msg
