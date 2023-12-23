import unittest
from MemoryManager import MemoryManager
from MemoryManager import MemoryManagerException


class MyTestCase(unittest.TestCase):
    def test_something(self):
        manager = MemoryManager()
        pid1 = "a"
        pid2 = "b"
        manager.add_variable(pid1)
        manager.add_variable(pid2)
        self.assertEqual(manager.symbol_table["a"], 0)
        self.assertEqual(manager.symbol_table["b"], 1)
        self.assertEqual(manager.get_address(pid2), 1)

    def test_redeclaration(self):
        with self.assertRaises(MemoryManagerException):
            manager = MemoryManager()
            pid1 = "a"
            pid2 = "b"
            manager.add_variable(pid1)
            manager.add_variable(pid2)
            manager.add_variable(pid2)

    def test_using_undeclared_variable(self):
        with self.assertRaises(MemoryManagerException):
            manager = MemoryManager()
            manager.get_address("za")



if __name__ == '__main__':
    unittest.main()
