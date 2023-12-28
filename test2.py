# a = 1
# c = a + 3
# print(c)
from MemoryManager import MemoryManager
from NonTerminals.Declarations import VarDeclaration


mem = MemoryManager()
mem2 = MemoryManager()
print(id(mem))
print(id(mem2))
decl = VarDeclaration("abc", False, False, -1)
mem.add_variable(decl)

print(mem.get_address("abc"))

