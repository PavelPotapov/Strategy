import pygame


class Base(pygame.sprite.Sprite):
    def __init__(self,x,y, filename=None, w=50,h=50, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(filename), (w,h))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self, window):
        window.blit(self.image, (self.rect.centerx, self.rect.centery))