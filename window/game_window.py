from tkinter import Tk

class GameWindow(Tk):
    def __init__(self, screen_title: str = 'Title', window_size: tuple=(800, 600), screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.window_size = window_size
        self.title(screen_title)
        self.resizable(False, False)
        self.center_window()

    def center_window(self):
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        center_x, center_y = int(screen_width / 2 - self.window_size[0] / 2), int(screen_height / 2 - self.window_size[1] / 2)
        self.geometry(f'{self.window_size[0]}x{self.window_size[1]}+{center_x}+{center_y}')