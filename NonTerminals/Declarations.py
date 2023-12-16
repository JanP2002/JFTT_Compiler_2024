from MemoryManager import MemoryManager

class Declarations():
    def __init__(self, decl_list):
        self.declarations = decl_list

    # def append_var_declaration(self, pid):
    #     var_decl = VarDeclaration(self.memory_manager, pid)
    #     self.declarations.append(var_decl)



class Declaration():
    def __init__(self):
        pass


class VarDeclaration(Declaration):

    def __init__(self, varname):
        super(Declaration, self).__init__()
        self.pid = varname


