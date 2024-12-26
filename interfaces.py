from abc import ABC, abstractmethod

class IRender(ABC):
    @abstractmethod
    def draw(self):
        """Абстрактный метод отрисовки объекта."""
        pass

    @abstractmethod
    def update(self):
        """Абстрактный метод обновления состояния объекта перед отрисовкой."""
        pass