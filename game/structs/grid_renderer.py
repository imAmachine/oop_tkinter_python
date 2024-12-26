from interfaces import IRender

class GridRenderer(IRender):
    def __init__(self, game_field, field_config):
        self.game_field = game_field

        if field_config.theme == 'dark':
            self.grid_color = 'white'
        elif field_config.theme == 'light':
            self.grid_color = 'lightgrey'
        else:
            raise Exception('Такой цветовой темы нет')

        self.cell_size = field_config.cell_size
        self.field_size = field_config.field_size

    def draw(self):
        """Рисует сетку на canvas с использованием тэгов для удаления."""
        x_size, y_size = self.field_size
        cell_size = self.cell_size

        # вертикальные линии
        for x in range(0, x_size):
            self.game_field.create_line(
                x * cell_size, 0, x * cell_size, y_size * cell_size,
                fill=self.grid_color, tag="grid"
            )
        
        # горизонтальные линии
        for y in range(0, y_size):
            self.game_field.create_line(
                0, y * cell_size, x_size * cell_size, y * cell_size,
                fill=self.grid_color, tag="grid"
            )

    def update(self):
        """Обновление сетки при изменении размеров или параметров."""
        self.game_field.delete("grid")
        self.draw()
