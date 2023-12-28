from MemoryManager import MemoryManager


class AbsIdentifier:
    def __init__(self, pid, m_manager: MemoryManager):
        self.pid = pid
        self.memory_manager = m_manager


class Identifier(AbsIdentifier):
    def __init__(self, pid):
        super().__init__(pid)

    # def translate_id_to_a_reg(self):
    #     address = self.memory_manager.get_address(self.pid)
    #     asm_code = []
    #     asm_code.extend(setRegisterConst(REG.B, address))
    #     #TODO: dokończyc
