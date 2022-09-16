from distutils.file_util import move_file
import math
from pygame import K_DOWN, K_RIGHT, K_LEFT, K_UP
import pygame.sprite, pygame.image, pygame.transform, pygame.key, pygame.draw
import math

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w=50,h=50, speed=5, health=100, power=20, armor=50, weapon='axe', *groups):
        super().__init__(*groups)

        self.alpha = 0 #угол между викингом и точкой, куда ему надо идти
        self.STATE = 1 #1 - stand, 2 - run, 3 - дойти до точки клика

        self.pos_click_x = 0
        self.pos_click_y = 0

        self.direction_move_to_click_y = 1 # 1 - вверх 2 - вниз
        self.direction_move_to_click_x = 1 # 1 - право 2 - лево

        
        self.width = w

        self.is_move_left = False #было ли движение влево (нужно, чтобы запомнить и флипануть картинку)

        self.flip = 1 # 1 - право 2 - лево 
        self.speed = speed
        self.image_animation ={
            'stand':[
                pygame.transform.scale(pygame.image.load(f"Viking1/Stand/{i}.png"), (w,h)) for i in range(9)
            ],

            'run':[
                pygame.transform.scale(pygame.image.load(f"Viking1/Run/{i}.png"), (w,h)) for i in range(9)
            ]
        }
        self.current_image = 1
        self.image = self.image_animation['stand'][self.current_image]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def move(self):
        keys = pygame.key.get_pressed()
        self.image = self.image_animation['run'][self.current_image // 5]
  
        if keys[K_RIGHT]:
            self.is_move_left = False
            self.STATE = 2
            self.flip = 1
            self.current_image += 1
            self.rect.x += self.speed
      
        if keys[K_LEFT]: 
            self.is_move_left = True
            self.STATE = 2
            self.flip = 2
            self.current_image += 1
            self.rect.x -= self.speed
            #self.image = pygame.transform.flip(self.image, True, False)
             
        if keys[K_DOWN]:
       
            self.current_image += 1
            self.rect.y += self.speed

        if keys[K_UP]:
    
            self.current_image += 1
            self.rect.y -= self.speed

        if self.current_image * 5 > 5 * len(self.image_animation['run']):
            self.current_image = 0


    def click_to_map(self, mouse, window):

        self.pos_click_x = mouse.x_mouse
        self.pos_click_y = mouse.y_mouse

        a = abs(self.rect.centerx - mouse.x_mouse)
        b = abs(self.rect.centery - mouse.y_mouse)
        c = ((a)**2 + (b)**2)**0.5
        cos = a/c
        self.alpha = math.acos(a/c)
        #print(self.alpha, 'до')
        self.alpha = self.alpha * 180/math.pi 
    
        if self.rect.centerx > mouse.x_mouse: #УСЛОВИЕ 1
            if self.rect.centery > mouse.y_mouse: #УСЛОВИЕ 2
                mouse.STATE_MOUSE = 2
            else:
                mouse.STATE_MOUSE = 3
        else:
            if self.rect.centery > mouse.y_mouse:
                mouse.STATE_MOUSE = 1
            else:
                mouse.STATE_MOUSE = 4

        if mouse.STATE_MOUSE == 1:
            self.direction_move_to_click_x = 1
            self.direction_move_to_click_y = 1
            self.is_move_left = False
            print("Право вверх")

        if mouse.STATE_MOUSE == 2:
            self.direction_move_to_click_x = 2
            self.direction_move_to_click_y = 1
            self.is_move_left = True
            print("Лево вверх")
        if mouse.STATE_MOUSE == 3:
            self.direction_move_to_click_x = 2
            self.direction_move_to_click_y = 2
            self.is_move_left = True
            print("Лево вниз")
        if mouse.STATE_MOUSE == 4:
            self.is_move_left = False
            self.alpha *= -1
            self.direction_move_to_click_x = 1
            self.direction_move_to_click_y = 2
            print("Право вниз")

        self.alpha *= 1 if self.rect.centery >= mouse.y_mouse else -1
        self.alpha *= -1 if self.rect.centerx >= mouse.x_mouse else 1
        
        if self.direction_move_to_click_y == 1 and self.direction_move_to_click_x == 2: #костыль:
            self.alpha *= -1

        if self.alpha == 90: #костыль
            self.direction_move_to_click_y = 1

        if self.alpha == -90: #костыль
            self.alpha = 90
            self.direction_move_to_click_y = 2

        
        print(self.alpha, 'после')


    def move_to_click(self, flag):
        #x - cos y - sin 
        if self.direction_move_to_click_x == 1:
            move_x = math.cos(math.radians(self.alpha)) * self.speed
        else:
            move_x = -math.cos(math.radians(self.alpha)) * self.speed
        if self.direction_move_to_click_y == 2:
            move_y = math.sin(math.radians(self.alpha)) * self.speed
        else:
            move_y = -math.sin(math.radians(self.alpha)) * self.speed
        self.rect.centery += move_y
        self.rect.centerx += move_x
        self.current_image += 1

        if self.current_image * 5 > 5 * len(self.image_animation['run']):
            self.current_image = 0
        
        #если расстояние от викинга до места клика меньше либо равно 80
        #print(((self.rect.centerx - self.pos_click_x)**2 + (self.rect.centery - self.pos_click_y)**2)**0.5)
        if ((self.rect.centerx - self.pos_click_x)**2 + (self.rect.centery - self.pos_click_y)**2)**0.5 <= 50:
        
            self.STATE = 1 #останавилваемся
            flag.is_shown = False


    def draw(self, window):
        window.blit(self.image, (self.rect))

    
  




