import pygame
import os
pygame.init()

def path_file(flie_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, flie_name)
    return path

WIN_WIDTH = 1200
WIN_HEIGHT = 600
FPS = 40
GREEN = (0,180,100)
GRAY = (80,80,80)
BLACK = (0,0,0)
WAIT = (255,255,255)
RED = (255,0,0)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

fon = pygame.image.load(path_file("fon.jpg"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))

win_picture = pygame.image.load(path_file("winn.jpg"))
win_picture = pygame.transform.scale(win_picture, (WIN_WIDTH, WIN_HEIGHT))

lose_picture = pygame.image.load(path_file("game_over.jpg"))
lose_picture = pygame.transform.scale(lose_picture, (WIN_WIDTH, WIN_HEIGHT))


pygame.mixer.music.load(path_file("sake_binksa.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

music_door_lock = pygame.mixer.Sound(path_file("door_lock.wav"))
music_win = pygame.mixer.Sound(path_file("win.wav"))
music_lose = pygame.mixer.Sound(path_file("lose.wav"))
music_shoot = pygame.mixer.Sound(path_file("fair.wav"))

class Button():
    def __init__(self,color, x,y, width,height, text ):
        self.color = color
        self.rect = pygame.Rect(x, y, width,height)
        self.font30 = pygame.font.SysFont("arial", 30)
        self.text = self.font30.render(text, True, BLACK)
    
    def button_show(self, px_x, px_y):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, (self.rect.x + px_x, self.rect.y + px_y))

button_start = Button(WAIT, 550, 150, 100, 50,"Start")      
button_skin = Button(WAIT, 550, 250, 100, 50,"Skin")  
button_exit = Button(WAIT, 550, 350, 100, 50,"Exit")  
button_menu = Button(WAIT, 1100, 0, 100, 50,"Menu")
button_reset = Button(WAIT, 500, 450, 100, 50,"Reset")


button_enemi1 = Button(WAIT,350,350,100,50,"Lyffi")
button_enemi2 = Button(WAIT,550,350,100,50,"Sanji")
button_enemi3 = Button(WAIT,750,350,100,50,"Frenk")


class GamaSpritr(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width, height))
        

    def reset(self):
        window.blit(self.image,(self.rect.x , self.rect.y))

class Player(GamaSpritr):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.speed_x = 0
        self.speed_y = 0

        self.direction = "right"
        self.image_r = self.image
        self.image_l = pygame.transform.flip(self.image, True, False)


    def update(self):
        if self.speed_x > 0 and self.rect.right < WIN_WIDTH or self.speed_x < 0 and self.rect.left > 0:
            self.rect.x += self.speed_x
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        elif self.speed_x < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)

        if self.speed_y < 0 and self.rect.top > 0 or self.speed_y > 0 and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speed_y 
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_y > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
        elif self.speed_y < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
    def shoot(self):
        if self.direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 15, 15, path_file("pngwing.com.png"), 5)
            bullets.add(bullet)
        if self.direction == "left":
            bullet = Bullet(self.rect.left - 15, self.rect.centery, 15, 15, path_file("pngwing.com.png"), -5)
            bullets.add(bullet)

class Bullet(GamaSpritr):
    def __init__(self, x, y, width, height, img, speed):
        super().__init__(x, y, width, height, img)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIN_WIDTH or self.rect.right < 0:
            self.kill()

class Enemy(GamaSpritr):
    def __init__(self, x, y, width, height, img, speed, direction, min_coord, max_coord):
        super().__init__(x, y, width, height, img)
        self.speed = speed
        self.direction = direction
        self.min_coord = min_coord
        self.max_coord = max_coord
 
    def update(self):
        if self.direction == "right" or self.direction == "left":
            if self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed
            
            if self.rect.right >= self.max_coord:
                self.direction = "left"
            if self.rect.left <= self.min_coord:
                self.direction = "right"

        elif self.direction == "up" or self.direction == "down":
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed

            if self.rect.top <= self.min_coord:
                self.direction = "down"
            if self.rect.bottom >= self.max_coord:
                self.direction = "up"

players_skin = pygame.sprite.Group()
player2 = Player(350, 230, 100, 100, path_file("luffi.png"))
player4 = Player(550, 230, 100, 100, path_file("candi.png"))
player6 = Player(750, 230, 100, 100, path_file("frenk.png"))
players_skin.add(player2,player4,player6)

player = Player(30, 0, 100, 100, path_file("luffi.png"))
lock = GamaSpritr(625, 350, 125, 20, path_file("lock.png"))

castles = pygame.sprite.Group()

keys = pygame.sprite.Group()
key = GamaSpritr(550, 90, 100, 100, path_file("key.png"))
keys.add(key)

bullets = pygame.sprite.Group()

ydons = pygame.sprite.Group()
ydon = GamaSpritr(550, 90, 100, 100, path_file("ydon.png"))
ydons.add(ydon)
ydons_2 = pygame.sprite.Group()
ydon_2 = GamaSpritr(30, 0, 100, 100, path_file("ydon.png"))
ydons_2.add( ydon_2)

enemies_1 = pygame.sprite.Group()
worog = Enemy(1100, 200, 100, 100, path_file("dofi.png"), 3, "left", 500, 1200)
worog2 = Enemy(400, 200, 100, 100, path_file("dofi.png"), 3, "down", 200, 600)
enemies_1.add(worog,worog2)
enemies_2 = pygame.sprite.Group()
worog4 = Enemy(400, 200, 100, 100, path_file("dofi.png"), 3, "down", 200, 600)
worog5 = Enemy(1100, 200, 100, 100, path_file("dofi.png"), 3, "left", 500, 1000)
enemies_2.add(worog4, worog5)

cel = GamaSpritr(850, 380, 110, 110, path_file("korona.png"))

walls = pygame.sprite.Group()
lock = GamaSpritr(625, 350, 125, 20, path_file("lock.png"))
wall_1 = GamaSpritr(0, 0, 20, 200,path_file("ctena.png"))
wall_2 = GamaSpritr(0, 200, 20, 200,path_file("ctena.png"))
wall_3 = GamaSpritr(0, 400, 20, 200,path_file("ctena.png"))
wall_4 = GamaSpritr(140, 0, 20, 200,path_file("ctena.png"))
wall_5 = GamaSpritr(0, 600, 20, 200,path_file("ctena.png"))
wall_6 = GamaSpritr(140, 200, 200, 20,path_file("ctena.png"))
wall_7 = GamaSpritr(320, 100, 20, 100,path_file("ctena.png"))
wall_8 = GamaSpritr(320, 200, 20, 200,path_file("ctena.png"))
wall_9 = GamaSpritr(130, 400, 190, 20,path_file("ctena.png"))
wall_10 = GamaSpritr(320, 400, 20, 80,path_file("ctena.png"))
wall_11 = GamaSpritr(320, 470, 75, 20,path_file("ctena.png"))
wall_12 = GamaSpritr(510, 500, 20, 200,path_file("ctena.png"))
wall_13 = GamaSpritr(510, 300, 100, 20,path_file("ctena.png"))
wall_14 = GamaSpritr(510, 400, 20, 200,path_file("ctena.png"))
wall_15 = GamaSpritr(510, 300, 20, 200,path_file("ctena.png"))
wall_16 = GamaSpritr(520, 0, 20, 180,path_file("ctena.png"))
wall_17 = GamaSpritr(520, 180, 200, 20,path_file("ctena.png"))
wall_18 = GamaSpritr(610, 300, 20, 200,path_file("ctena.png"))
wall_19 = GamaSpritr(750, 300, 20, 190,path_file("ctena.png"))
wall_20 = GamaSpritr(750, 300, 200, 20,path_file("ctena.png"))
wall_21 = GamaSpritr(700, 180, 200, 20,path_file("ctena.png"))
wall_22 = GamaSpritr(900, 0, 20, 60,path_file("ctena.png"))
wall_23 = GamaSpritr(750, 470, 200, 20,path_file("ctena.png"))
wall_24 = GamaSpritr(950, 470, 120, 20,path_file("ctena.png"))
wall_25 = GamaSpritr(800, 300, 500, 20,path_file("ctena.png"))
walls.add(lock, wall_1,wall_2,wall_3, wall_4, wall_5, wall_6, wall_7, wall_8, wall_9, wall_10, wall_11, wall_12, wall_13, wall_14, wall_15, wall_16, wall_17, wall_18, wall_19, wall_20, wall_21, wall_22, wall_23, wall_24, wall_25)



level = 0

game = True
play = False
while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        

        if level == 0:
            if event.type == pygame.MOUSEMOTION:
                x,y = event.pos
                if button_start.rect.collidepoint(x,y):
                    button_start.color = GRAY
                 
                elif button_exit.rect.collidepoint(x,y):
                    button_exit.color = GRAY
                
                elif button_skin.rect.collidepoint(x,y):
                    button_skin.color = GRAY
                

                else:
                    button_start.color = WAIT
                    button_exit.color = WAIT
                    button_skin.color = WAIT
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y =  event.pos
                if button_start.rect.collidepoint(x,y):
                    if play == False:
                        play = True

                        player.rect.x = 30
                        player.rect.y = 0

                        bullets.empty()

                        enemies_1 = pygame.sprite.Group()
                        worog = Enemy(1100, 200, 100, 100, path_file("dofi.png"), 3, "left", 500, 1200)
                        worog2 = Enemy(400, 200, 100, 100, path_file("dofi.png"), 3, "down", 200, 600)
                        enemies_1.add(worog,worog2)
                        enemies_2 = pygame.sprite.Group()
                        worog4 = Enemy(400, 200, 100, 100, path_file("dofi.png"), 3, "down", 200, 600)
                        worog5 = Enemy(1100, 200, 100, 100, path_file("dofi.png"), 3, "left", 500, 1000)
                        enemies_2.add(worog4, worog5)

                        pygame.mixer.music.load(path_file("sake_binksa.mp3"))
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)

                        level = 1
                elif button_skin.rect.collidepoint(x,y):
                    level = 2
                elif button_exit.rect.collidepoint(x,y):
                    game = False
            

        elif level == 1 or level == 1.1 or level == 1.2 or level == 1.3 or level == 10:   
            if event.type == pygame.MOUSEMOTION:
                x,y = event.pos
                if button_menu.rect.collidepoint(x,y):
                    button_menu.color = GRAY
                               
                else:
                    button_menu.color = WAIT
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y =  event.pos
                if button_menu.rect.collidepoint(x,y):
                    level = 0 
                    play = False
                               

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 5
                    player.direction = "right"
                    player.image = player.image_r
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = -5
                    player.direction = "left"
                    player.image = player.image_l
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = -5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 5
                if event.key == pygame.K_e:
                    music_shoot.play()
                    player.shoot()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 0

        elif level == 2:
            if event.type == pygame.MOUSEMOTION:
                x,y = event.pos
                if button_enemi1.rect.collidepoint(x,y):
                    button_enemi1.color = GRAY
                 
                elif button_enemi2.rect.collidepoint(x,y):
                    button_enemi2.color = GRAY

                elif button_menu.rect.collidepoint(x,y):
                    button_menu.color = GRAY
                
                elif button_enemi3.rect.collidepoint(x,y):
                    button_enemi3.color = GRAY
                else:
                    button_enemi1.color = WAIT
                    button_enemi2.color = WAIT
                    button_enemi3.color = WAIT 
                    button_menu.color = WAIT
             
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y =  event.pos     
                if button_enemi1.rect.collidepoint(x,y):
                    player = Player(30, 0, 100, 100, path_file("luffi.png"))
                    play = True
                    level = 1
                elif button_enemi2.rect.collidepoint(x,y):
                    player = Player(30, 0, 100, 100, path_file("candi.png"))
                    play = True
                    level = 1
                elif button_enemi3.rect.collidepoint(x,y):
                    player = Player(30, 0, 100, 100, path_file("frenk.png"))
                    play = True
                    level = 1
                elif button_menu.rect.collidepoint(x,y):
                    level = 0
        
        elif level == 10:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y =  event.pos     
                if button_reset.rect.collidepoint(x,y):
                    level = 1
                    


    if level == 0:
        window.blit(fon,(0,0))
        button_start.button_show(18,10)
        button_exit.button_show(25,10)
        button_skin.button_show(22,10)
    elif level == 1:
        if play == True:
            window.blit(fon, (0,0)) 
            button_menu.button_show(18, 10)
            player.reset()
            player.update()
            
            enemies_1.draw(window)
            enemies_1.update()
            ydons.draw(window)
            cel.reset()
            walls.draw(window)
            bullets.draw(window)
            bullets.update()

        
            if pygame.sprite.spritecollide(player, ydons, True):
                level = 1.2
            
            
            if pygame.sprite.spritecollide(player, enemies_1, False):
                level = 10

            pygame.sprite.groupcollide(bullets, walls, True, False)
            pygame.sprite.groupcollide(bullets, enemies_1, True, True)

    elif level == 1.2:
        if play == True:
            window.blit(fon, (0,0)) 
            button_menu.button_show(18, 10)
            player.reset()
            player.update()
            enemies_2.draw(window)
            enemies_2.update()
            ydons_2.draw(window)
            #cel.reset()
            walls.draw(window)
            bullets.draw(window)
            bullets.update()

            if pygame.sprite.spritecollide(player,ydons_2, True):
                level = 1.3

            if pygame.sprite.spritecollide(player, enemies_2, False):
                level = 10
                #pygame.mixer.music.stop()

            pygame.sprite.groupcollide(bullets, walls, True, False)
            pygame.sprite.groupcollide(bullets, enemies_2, True, True)

    elif level == 1.3:
        if play == True:
            window.blit(fon, (0,0)) 
            button_menu.button_show(18, 10)
            player.reset()
            player.update()
            enemies_2.draw(window)
            enemies_2.update()
            cel.reset()
            walls.draw(window)
            keys.draw(window)
                
            bullets.draw(window)
            bullets.update()
            castles.draw(window)

            if pygame.sprite.spritecollide(player, keys, True):
                lock.kill()
                
                castles.add(lock)
            
            if pygame.sprite.spritecollide(player, castles,True):
                music_door_lock.play()

            if pygame.sprite.collide_rect(player,cel):
                pygame.mixer.music.stop()
                music_win.play()
                button_menu.button_show(18, 10)                
                window.blit(win_picture,(0,0))

            

            pygame.sprite.groupcollide(bullets, walls, True, False)
            


    elif level == 2:
        window.blit(fon,(0,0))
        button_enemi1.button_show(20,10)
        button_enemi2.button_show(20,10)
        button_enemi3.button_show(20,10)
        button_menu.button_show(18,10)
        players_skin.draw(window)

    elif level == 10:  
        play = False
        window.blit(lose_picture,(0,0))
        button_menu.button_show(18, 10)
        pygame.mixer.music.stop()
        music_lose.play()
        

    clock.tick(FPS)
    pygame.display.update()