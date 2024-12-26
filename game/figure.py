import random


class Figure:
    SHAPES = {
        'I': {
            'shape': [(0, 0), (1, 0), (2, 0), (3, 0)],
            'color': 'cyan',
            'rotation_point': (1.5, 0.5)  # центр между 2-м и 3-м блоком
        },
        'O': {
            'shape': [(0, 0), (1, 0), (0, 1), (1, 1)],
            'color': 'yellow',
            'rotation_point': (0.5, 0.5)  # центр квадрата
        },
        'T': {
            'shape': [(1, 0), (0, 1), (1, 1), (2, 1)],
            'color': 'purple',
            'rotation_point': (1, 1)  # центральный блок
        },
        'S': {
            'shape': [(1, 0), (2, 0), (0, 1), (1, 1)],
            'color': 'green',
            'rotation_point': (1, 1)  # центральный блок
        },
        'Z': {
            'shape': [(0, 0), (1, 0), (1, 1), (2, 1)],
            'color': 'red',
            'rotation_point': (1, 1)  # центральный блок
        },
        'L': {
            'shape': [(0, 0), (0, 1), (1, 1), (2, 1)],
            'color': 'orange',
            'rotation_point': (1, 1)  # второй блок снизу
        },
        'J': {
            'shape': [(2, 0), (0, 1), (1, 1), (2, 1)],
            'color': 'blue',
            'rotation_point': (1, 1)  # второй блок снизу
        }
    }

    def __init__(self, x, y):
        self.type = random.choice(list(self.SHAPES.keys()))
        shape_data = self.SHAPES[self.type]
        self.blocks = shape_data['shape']
        self.color = shape_data['color']
        self.rotation_point = shape_data['rotation_point']
        self.position = (x, y)
        self.blocks = [(block[0] + self.position[0], block[1] + self.position[1]) 
                      for block in self.blocks]

    def _get_rotated_blocks(self, direction):
        """Возвращает новые координаты блоков после поворота"""
        rotation_x = self.position[0] + self.rotation_point[0]
        rotation_y = self.position[1] + self.rotation_point[1]
        
        return [self._rotate_single_point(x, y, rotation_x, rotation_y, direction) 
                for x, y in self.blocks]

    def _rotate_single_point(self, x, y, center_x, center_y, direction):
        """Поворачивает одну точку вокруг центра"""
        rel_x = x - center_x
        rel_y = y - center_y
        
        if direction == 1:  # по часовой
            new_x = rel_y
            new_y = -rel_x
        else:  # против часовой
            new_x = -rel_y
            new_y = rel_x
            
        return (int(center_x + new_x), int(center_y + new_y))

    def _get_wall_kicks(self):
        """Возвращает список проверяемых смещений в зависимости от типа фигуры"""
        if self.type == 'I':
            return [
                (0, 0),
                (-1, 0),
                (2, 0),
                (-1, -2),
                (2, 1),
                (-2, 0)
            ]
        else:
            return [
                (0, 0),
                (1, 0),
                (-1, 0),
                (0, -1),
                (1, -1),
                (-1, -1)
            ]

    def _is_valid_position(self, blocks, field_size):
        """Проверяет, находятся ли все блоки в пределах поля"""
        return all(0 <= x < field_size[0] and y < field_size[1] 
                  for x, y in blocks)

    def _apply_kick(self, blocks, kick_x, kick_y):
        """Применяет смещение к блокам"""
        return [(x + kick_x, y + kick_y) for x, y in blocks]

    def _try_rotation_with_kicks(self, new_blocks, collision_func, field_size):
        """Пытается применить поворот с учётом всех возможных смещений"""
        for kick_x, kick_y in self._get_wall_kicks():
            test_blocks = self._apply_kick(new_blocks, kick_x, kick_y)
            
            if not self._is_valid_position(test_blocks, field_size):
                continue
                
            self.blocks = test_blocks
            
            if not collision_func(0, 0):
                self.position = (self.position[0] + kick_x, 
                               self.position[1] + kick_y)
                return True
                
        return False
    
    def get_size(self):
        width, height = max(self.blocks, key = lambda x: x[0])[0], max(self.blocks, key = lambda x: x[1])[1]
        return width + 1, height + 1

    def set_position(self, x = 0, y = 0):
        self.position = (self.position[0] + x, self.position[1] + y)
        self.blocks = [(block[0] + x, block[1] + y) for block in self.blocks]

    def move(self, dx, dy, collision_func) -> bool:
        """Перемещает фигуру."""
        if not collision_func(dx, dy):
            self.set_position(dx, dy)
            return True
        return False
    
    def rotate(self, direction, collision_func, field_size):
        """
        Основной метод вращения фигуры.
        direction = 1: по часовой стрелке, direction = -1: против часовой стрелки
        """
        original_blocks = self.blocks.copy()
        new_blocks = self._get_rotated_blocks(direction)
        
        if self._try_rotation_with_kicks(new_blocks, collision_func, field_size):
            return True
            
        self.blocks = original_blocks
        return False