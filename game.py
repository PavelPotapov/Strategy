from angar import Angar
from flag import Flag
from random import randint
from menu import Menu
from viking import GameSprite
from trees import Tree
from mouse.mouse import Mouse
import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()


    def custom_draw(self):
        for sprite in sorted(self.sprites(), key=lambda sprite:sprite.rect.centery):
            self.display_surface.blit(sprite.image, (sprite.rect.centerx - sprite.rect.centerx//2, sprite.rect.centery - sprite.rect.centery//2))


pygame.init()
game = True


W = 600
H = 600
FPS = 60

window = pygame.display.set_mode((W,H), flags=pygame.RESIZABLE)
clock = pygame.time.Clock()


mouse = Mouse()
#group = CameraGroup()

menu = Menu(0,0, filename='ambar.png')

viking = GameSprite(100,100, w=100, h=100)
group_heroes = pygame.sprite.Group()
group_heroes.add(viking) 

group_tree = pygame.sprite.Group()

for t in [Tree(randint(0, 2000), randint(0,2000), 'tree.png', w=150, h=150) for i in range(50)]:
    group_tree.add(t)



flag = Flag(0,0,'flag.png', w=50, h=50)
angar = Angar(0,0,'ambar.png')


while game:
    window.fill((0,75,0))

    viking.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #при нажатии ан пробел отменяем движение убираем флажок
                viking.STATE = 1
                flag.is_shown = False
            elif event.key == pygame.K_m and menu.is_shown == False: #при нажатии НА m открывакм меню
                menu.is_shown = True
            elif event.key == pygame.K_m and menu.STATE == 2:
                menu.STATE = 1
            else:
                menu.is_shown = False

        if event.type == pygame.MOUSEBUTTONDOWN:   
            
            mouse.is_mouse_clicked = True
            mouse.x_mouse = pygame.mouse.get_pos()[0]
            mouse.y_mouse = pygame.mouse.get_pos()[1]
            mouse.check_state_mouse()

            #ЕСЛИ НАЖАЛИ НА ПКМ 
            if pygame.mouse.get_pressed()[2]:
                
                mouse.x_mouse = pygame.mouse.get_pos()[0]
                mouse.y_mouse = pygame.mouse.get_pos()[1]
                #показываем флаг и выставляем ему x и y
                flag.is_shown = True
                flag.rect.centerx = mouse.x_mouse
                flag.rect.centery = mouse.y_mouse
                #print(f'Место клика {mouse.x_mouse} {mouse.y_mouse}')
                viking.STATE = 3 #викинг получил указание идти до клика
                viking.click_to_map(mouse, window) #ОПРЕДЕЛЯЕМ УГОЛ И ШАГ ПО ОСИ X И Y дО МЕСТА КЛИКА
                
        if event.type == pygame.MOUSEBUTTONUP:
            mouse.is_mouse_clicked = False


    #ГЕРОЙ ДВИЖЕТСЯ ПО КЛИКУ
    if viking.STATE == 3:
        #pygame.draw.line(window, (255,0,0), (viking.rect.centerx, viking.rect.centery), (mouse.x_mouse, mouse.y_mouse))
        viking.move_to_click(flag)
    


    #ЕСЛИ ГЕРОЙ ДВИГАЛСЯ ВЛЕВО ОСТАВИТЬ ФРЕЙМ КАРТИНКИ С ФЛИПОМ
    if viking.is_move_left:
        viking.image = pygame.transform.flip(viking.image, True, False)
    

    #ФУНКЦИОНАЛ ВЫДЕЛЕНИЯ ОБЪЕКТОВ
    mouse.check_state_mouse()
    if pygame.mouse.get_pressed()[0] and mouse.is_mouse_clicked:
        mouse.draw_mouse_rect_on_window(window=window)


    #ОПРЕДЕЛЯЮ ВЫДЕЛЕННЫЕ ОБЪЕКТЫ
    result = pygame.sprite.spritecollide(mouse, group_tree, False, False)
    result = pygame.sprite.spritecollide(mouse, group_heroes, False, False ) + result

    #ОТРИСОВЫВАЮ РАМКИ У ВЫДЕЛЕННЫХ ОБЪЕКТОВ
    for r in result:
        pygame.draw.rect(window, (0,0,255), r.rect, width=1)


    #отрисоввываем группы
    group_tree.draw(window)
    viking.draw(window)


    #показан флаг
    if flag.is_shown:
        flag.draw(window)


    #показано меню
    if menu.is_shown:
        menu.rect.centerx = viking.rect.centerx + menu.width
        menu.rect.centery = viking.rect.centery

        k = 1
        for elem in menu.menu:
            elem.rect.x = viking.rect.centerx + menu.width // 2
            elem.rect.y = viking.rect.centery - menu.height_point_menu - menu.height//2 + k*menu.height_point_menu
            k += 1
            
        menu.draw(window)

    if menu.STATE == 2:
        menu.is_shown = False
        angar.placement()
        if pygame.key.get_pressed()[pygame.K_p]:
            print('СОЗДАЛИ!')
            group_tree.add(angar.create())
            menu.STATE = 1
     



    
    clock.tick(FPS)
    pygame.display.update()


