import pygame

from base import Base



class Angar(Base):
    def __init__(self, x, y, filename=None, w=50, h=50, *groups) -> None:
        super().__init__(x, y, filename, w, h, *groups)
        self.RED = (255,0,0)
    
    def create(self):
        self.image.set_alpha(100)
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect.centery = pygame.mouse.get_pos()[1]

        return self
    
    def draw(self, window):
        window.blit(self.image, self.rect.center)

    def placement(self):
        self.image = self.image.convert_alpha()
        self.image.set_colorkey(self.RED)
        self.image.set_alpha(80)
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect.centery = pygame.mouse.get_pos()[1]
        pygame.display.get_surface().blit(self.image, self.rect.center)