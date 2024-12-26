class FieldConfig:
    def __init__(self, field_size: tuple[int], window_size: tuple[int], theme: str = 'white') -> None:
        self.field_size = field_size
        self.window_size = window_size

        self.cell_size = min(window_size[0] // field_size[0], 
                             window_size[1] // field_size[1])
        self.theme = theme