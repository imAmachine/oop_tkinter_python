from tkinter import BOTH, Frame, Label
from game.controller import Controller
from game.figure import Figure
from game.game_field import GameField
from game.structs.figure_renderer import FigureRenderer
from game.structs.grid_renderer import GridRenderer


class GameManager:
    def __init__(self, field_config, preview_config, main_window) -> None:
        self.game_started = False
        self.score = 0

        # layout фрейм
        self.game_container = Frame(main_window)
        self.game_container.pack(fill=BOTH, expand=True)

        # Настройка колонок
        preview_width = preview_config.cell_size * preview_config.field_size[0]
        field_width = field_config.cell_size * field_config.field_size[0]
        field_height = field_config.cell_size * field_config.field_size[1]
        
        self.game_container.grid_columnconfigure(0, minsize=field_width, weight=0)
        self.game_container.grid_columnconfigure(1, minsize=preview_width, weight=1)
        self.game_container.grid_rowconfigure(0, weight=1)

        # Основное поле игры
        self.game_field = GameField(field_config, master=self.game_container)
        self.game_field.grid(row=0, column=0, padx=5, pady=0, sticky='n')

        # Поле предпросмотра
        preview_config.field_size = (0, 0)
        self.preview_field = GameField(preview_config, master=self.game_container)
        self.preview_field.grid(row=0, column=1, padx=0, pady=30, sticky='n')
        
        # Метка для отображения очков под полем предпросмотра
        self.score_label = Label(self.game_container, text=f"Очки: {self.score}", font=("Arial", 12))
        self.score_label.grid(row=0, column=1, padx=0, pady=5, sticky='n')

        # установка размера canvas у поля
        self.game_field.config(width=field_width, height=field_height)

        # отрисовщики фигур
        self.figure_renderer = FigureRenderer(game_field=self.game_field, figure=None)
        self.next_figure_renderer = FigureRenderer(game_field=self.preview_field, figure=None)

        # логика управления
        self.controller = Controller(self)

        # фигуры и время падения
        self.current_figure = None
        self.next_figure = None
        self.down_ms = 400

        # Метка завершения игры
        self.game_over_label = Label(self.game_field, text="Игра завершена\nЧтобы начать новую игру, нажмите <space>", font=("Arial", 12), fg="red", bg="black")
        self.game_over_label.place(relx=0.5, rely=0.5, anchor="center")
        self.fg_down_timer = None # таймер для падения фигуры

    def _start_timer(self):
        """Запускает таймер для перемещения фигуры вниз."""
        self._stop_timer()
        
        if self.game_started:
            self.fg_down_timer = self.game_field.after(self.down_ms, self._move_down)

    def _stop_timer(self):
        if self.fg_down_timer:
            self.game_field.after_cancel(self.fg_down_timer)  # Остановка таймера
            self.fg_down_timer = None
    
    def start_game(self):
        """Запускает новую игру, сбрасывая параметры."""
        self.game_started = True
        self.score = 0

        self.game_over_label.place_forget()  # Скрыть сообщение о завершении игры
        self.game_field.clear_occupied()
        self._create_figure_for_preview()
        self._spawn_current_figure()
        
        # Установка таймера
        self._start_timer()

    def update_score(self, lines_count):
        """Обновляет очки и обновляет текст метки."""
        standart_scaler = 100
        multipliers = {1: 1, 2: 2, 3: 5, 4: 10}
        
        self.score += (lines_count * standart_scaler) * multipliers.get(lines_count, 1)
        self.score_label.config(text=f"Очки: {self.score}")
    
    def check_lines(self, min_y: int) -> None:
        counter = 0
        field_size = self.game_field.field_config.field_size
        for y in range(min_y, min_y + 4):
            if y >= field_size[1]:
                break
            if len([cell for cell in self.game_field.occupied_cells if cell['y'] == y]) == field_size[0]:
                self.game_field.remove_row(y)
                counter += 1
        
        if counter > 0:
            self.update_score(counter)

    def _create_figure_for_preview(self) -> Figure:
        self.next_figure = Figure(0, 0)
        fg_size = self.next_figure.get_size()
        field_config = self.preview_field.field_config
        field_config.field_size = (fg_size[0], fg_size[1])
        self.preview_field.update()

        self.next_figure_renderer.figure = self.next_figure
        self.next_figure_renderer.update()
        
    def _spawn_current_figure(self) -> None:
        self.current_figure = self.next_figure
        self._create_figure_for_preview()

        fg_size = self.current_figure.get_size()
        x = self.game_field.field_config.field_size[0] // 2 - fg_size[0] // 2
        self.current_figure.set_position(x=x)

        if self._check_collision(0, 0):
            self.game_started = False
            self.end_game()
            return
        
        self.figure_renderer.figure = self.current_figure
        self.figure_renderer.update()
        
    def end_game(self):
        """Логика завершения игры."""
        self._stop_timer()
        self.current_figure = None
        self.next_figure = None
        self.game_over_label.place(relx=0.5, rely=0.5, anchor="center")

    def move_figure(self, dx, dy) -> bool:
        """Перемещает фигуру, если нет столкновений."""
        return self.current_figure.move(dx, dy, self._check_collision)

    def rotate_figure(self, direction) -> None:
        """Поворот фигуры."""
        self.current_figure.rotate(direction, self._check_collision, self.game_field.field_config.field_size)
        self.figure_renderer.update()

    def _check_collision(self, dx, dy) -> bool:
        """Проверяет столкновение фигуры с границами и занятыми клетками."""
        for cell in self.current_figure.blocks:
            x, y = cell
            new_x, new_y = x + dx, y + dy
            if new_x < 0 or new_x >= self.game_field.field_config.field_size[0]:
                return True  # столкновение с границами по горизонтали
            if new_y >= self.game_field.field_config.field_size[1]:
                return True  # столкновение с нижней границей
            if self.game_field.get_occupied_cell(new_x, new_y):
                return True  # столкновение с другой фигурой
        return False

    def _move_down(self) -> None:
        """Перемещает фигуру вниз или фиксирует её положение."""
        if not self.move_figure(0, 1):
            self._fix_figure()
            self._spawn_current_figure()
        
        self.figure_renderer.update()
        self.game_field.after(self.down_ms, self._move_down)

    def _fix_figure(self) -> None:
        """Фиксирует текущую фигуру на поле."""
        for x, y in self.current_figure.blocks:
            self.game_field.occupied_cells.append({'x': x, 
                                                   'y': y, 
                                                   'color': self.current_figure.color})
        
        self.check_lines(self.current_figure.position[1] - 1)
        self.game_field.update()