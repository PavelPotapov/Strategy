import pygame
from base import Base


class MenuPoints(pygame.sprite.Sprite):
    def __init__(self,x,y, filename=None, w=50,h=50, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(filename), (w,h))
        self.rect = self.image.get_rect()
        self.width = w
        self.height = h
        self.rect.x = x
        self.rect.y = y

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Menu(Base):
    def __init__(self, x, y, filename, w=100, h=200, count=3, *groups) -> None:
        super().__init__(x, y, filename, w, h, *groups)
        self.height_point_menu = h // count #
        self.menu = [MenuPoints(x+10, y+self.height_point_menu*i + 3, filename=filename, w=w-3, h=h//count-3)  for i in range(count)]
        self.image = pygame.Surface((w,h))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = w
        self.height = h
        self.is_shown = False #показано ли меню
        self.STATE = 1 #1 -2 - кликнули по пункту меню 3 4 


    def draw(self, window):
        pygame.draw.rect(window, (0,255,0), self.rect)

        for elem in self.menu:
            elem.draw(window)
            if elem.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                if pygame.mouse.get_pressed()[0]:
                    self.STATE = 2 
                pygame.draw.rect(window, (255,0,0), elem.rect, width=1)
                
        
        
        