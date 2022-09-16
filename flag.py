from base import Base


class Flag(Base):
    def __init__(self, x, y, filename, w=50, h=50, *groups) -> None:
        super().__init__(x, y, filename, w, h, *groups)
        self.is_shown = False #ПОКАЗАН ЛИ ФЛАЖОК НА ЭКРАНЕ
        