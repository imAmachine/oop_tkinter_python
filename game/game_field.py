from tkinter import Canvas, Misc
from typing import Any
from game.structs.grid_renderer import GridRenderer
from interfaces import IRender
from window.field_config import FieldConfig

import time


class GameField(Canvas, IRender):
    def __init__(self, field_config: FieldConfig, master: Misc | None = None, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self.field_config = field_config
        self.occupied_cells = []

        if self.field_config.theme == 'dark':
            self.config(bg='black')
        elif self.field_config.theme == 'light':
            self.config(bg='white')
        else:
            raise Exception('Такой цветовой темы нет')

        self.grid_renderer = GridRenderer(self, field_config)
        self.grid_renderer.draw()

    def _get_cell_coords(self, x, y, padding=1):
        """Возвращает координаты ячейки с учётом отступов для отображения сетки."""
        cell_size = self.field_config.cell_size
        x0 = x * cell_size + padding
        y0 = y * cell_size + padding
        x1 = x0 + cell_size - 2 * padding
        y1 = y0 + cell_size - 2 * padding
        return (x0, y0, x1, y1)
    
    def get_occupied_cell(self, x, y):
        occupied_cell = [cell for cell in self.occupied_cells if cell['x'] == x and cell['y'] == y]
        if len(occupied_cell) > 0:
            return occupied_cell[0]
        return None
    
    def add_cell(self, x, y, color):
        """Добавляет блок в список и рисует его на экране."""
        if not self.is_cell_occupied(x, y):
            self.occupied_cells.append({"x": x, "y": y, "color": color})

    def remove_row(self, y):
        """Удаляет все блоки на указанной строке и сдвигает блоки выше вниз."""
        # Удаление всех блоков на строке y
        self.occupied_cells = [cell for cell in self.occupied_cells if cell["y"] != y]

        # Сдвигаем блоки выше на одну строку вниз
        for cell in self.occupied_cells:
            if cell["y"] < y:
                cell["y"] += 1

        # Перерисовка поля
        self.update()
    
    def clear_occupied(self):
        self.occupied_cells.clear()
        self.update()

    def update_canvas_size(self, width, height):
        self.config(width=width, height=height)

    def _draw_cell(self, x: int, y: int, color: str, tag: str = '') -> None:
        """Рисует закрашенную ячейку по индексу (x, y) заданного цвета с тэгом."""
        x0, y0, x1, y1 = self._get_cell_coords(x, y)
        self.create_rectangle(x0, y0, x1, y1, outline='', fill=color, tag=tag)

    def update(self):
        self.delete('all')
        self.draw()

    def draw(self):
        """Перерисовывает все блоки на экране."""
        start_time = time.perf_counter()
        
        for cell in self.occupied_cells:
            self._draw_cell(cell['x'], cell['y'], cell['color'])
        
        cell_size = self.field_config.cell_size
        self.update_canvas_size(width=cell_size * self.field_config.field_size[0], height=cell_size * self.field_config.field_size[1])
        self.grid_renderer = GridRenderer(self, self.field_config)
        self.grid_renderer.draw()
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Время выполнения метода draw: {execution_time:.6f} секунд")
