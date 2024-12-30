from game.game_manager import GameManager
from window.game_window import GameWindow
from window.field_config import FieldConfig


if __name__ == "__main__":
    root = GameWindow(screen_title='Tetris by VLD v3', window_size=(625, 800)) # игровое поле
    field_config = FieldConfig(field_size=(10, 20), window_size=(500, root.window_size[1]), theme='light') # элемент конфигурации игрового поля
    preview_config = FieldConfig(field_size=(4, 4), window_size=(200, 200), theme='light') # элемент конфигурации окна предпросмотра фигуры

    # объявление и запуск логики игры
    game_manager = GameManager(field_config, preview_config, main_window=root)
    root.mainloop()
