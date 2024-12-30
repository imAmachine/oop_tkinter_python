import unittest

from game.game_field import GameField
from window.field_config import FieldConfig

class TestGameField(unittest.TestCase):
    def setUp(self):
        self.field_config = FieldConfig(field_size=(10, 20), window_size=(500, 800), theme='light') # элемент конфигурации игрового поля
        self.game_field = GameField(self.field_config)
        self.game_field.occupied_cells = []

    def test_remove_full_row(self):
        for x in range(10):
            self.game_field.occupied_cells.append({'x': x, 'y': 19, 'color': 'red'})

        self.game_field.remove_row(19)
        self.assertFalse(any(cell['y'] == 19 for cell in self.game_field.occupied_cells))
        self.assertTrue(all(cell['y'] != 19 for cell in self.game_field.occupied_cells))

if __name__ == '__main__':
    unittest.main()
