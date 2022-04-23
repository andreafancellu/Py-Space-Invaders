import unittest
from src.classes.Shuttle import Shuttle

class TestShuttleMethods(unittest.TestCase):
    
    def test_take_damage(self):
        shuttle = Shuttle("Apollo13", 100)
        shuttle.take_damage(50)
        self.assertEqual(50, shuttle.get_hp())
        shuttle.take_damage(50)
        self.assertEqual(0, shuttle.get_hp())

    def test_die(self):
        shuttle = Shuttle("Apollo13", 100)
        shuttle.take_damage(100)
        self.assertEqual(0, shuttle.get_hp())
        self.assertTrue(shuttle.get_is_dead())

if __name__ == '__main__':
    unittest.main()