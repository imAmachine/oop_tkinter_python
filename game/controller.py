class Controller:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.movement_job = None

        self.game_manager.game_field.bind("<KeyPress-Left>", self.start_move_left)
        self.game_manager.game_field.bind("<KeyRelease-Left>", self.stop_move)
        
        self.game_manager.game_field.bind("<KeyPress-Right>", self.start_move_right)
        self.game_manager.game_field.bind("<KeyRelease-Right>", self.stop_move)

        self.game_manager.game_field.bind("<KeyPress-Down>", self.start_move_down)
        self.game_manager.game_field.bind("<KeyRelease-Down>", self.stop_move)

        self.game_manager.game_field.bind("<KeyPress-Up>", self.rotate_figure)
        
        self.game_manager.game_field.bind("<KeyPress-space>", self.start_game)

        self.game_manager.game_field.focus_set()

    def start_game(self, event):
        if not self.game_manager.game_started:
            self.game_manager.start_game()
    
    def start_move_left(self, event):
        self.stop_move()
        self.move_figure(-1, 0)

    def start_move_right(self, event):
        self.stop_move()
        self.move_figure(1, 0)

    def start_move_down(self, event):
        self.stop_move()
        self.move_figure(0, 1)

    def move_figure(self, dx, dy):
        self.game_manager.move_figure(dx, dy)
        self.game_manager.figure_renderer.update()

        self.movement_job = self.game_manager.game_field.after(100, self.move_figure, dx, dy)

    def stop_move(self, event=None):
        if self.movement_job:
            self.game_manager.game_field.after_cancel(self.movement_job)
            self.movement_job = None

    def rotate_figure(self, event):
        self.game_manager.rotate_figure(-1)
        self.game_manager.figure_renderer.update()
