from interfaces import IRender

class FigureRenderer(IRender):
    def __init__(self, game_field, figure=None):
        self.game_field = game_field
        self.figure = figure

    def draw(self):
        """Рисует фигуру на игровом поле."""
        if self.figure:
            for cell in self.figure.blocks:
                x, y = cell
                self.game_field._draw_cell(x, y, self.figure.color, tag="figure")

    def update(self):
        """Обновляет позицию фигуры на поле, если фигура двигается."""
        if self.figure:
            self.game_field.delete("figure")
            self.draw()
