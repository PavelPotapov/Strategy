from base import Base

class Tree(Base):
    def __init__(self,x,y, filename, w=50,h=50, *groups) -> None:
        super().__init__(x,y, filename, w=w,h=h, *groups)
    