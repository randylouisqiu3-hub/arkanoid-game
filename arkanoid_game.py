import pygame   
from random import randint
from time import sleep

#Make a game scene   
pygame.init()   
window = pygame.display.set_mode((500, 500))   
BACK = (255, 95, 60)   
window.fill(BACK)   
clock = pygame.time.Clock()   
   
#Variable for losing   
game_over = False   
   
#Variable for the coordinates of rect   
rect_x = 200   
rect_y = 300
start_x = 5
start_y = 5
   
#Class area   
class Area():       
    #Contructor   
    def __init__(self, x=0, y=0, width=10, height=10, color=None):   
        self.rect = pygame.Rect(x, y, width, height)   
        self.fill_color = color   
        self.outline_rect = None   
        self.frame_color = None   
        self.thickness = 0   
   
    #Set color   
    def color(self, new_color):   
        self.fill_color = new_color   
   
    #Fill area   
    def fill(self):   
        pygame.draw.rect(window, self.fill_color, self.rect)   
    #detect collide point   
    def collidepoint(self, x, y):   
        return self.rect.collidepoint(x, y)   
    #detect collide rect   
    def colliderect(self, rect):   
        return self.rect.colliderect(rect)



class Picture(Area):
    def __init__ (self, filename, x=0, y=0, width=10, height=10):   
        super().__init__(x, y, width, height)   
        self.image = pygame.image.load(filename)   
        self.image = pygame.transform.scale(self.image, (width, height))
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

YELLOW = (255, 255, 0)
DARK_BLUE = (34, 0, 255)
BLUE = (0, 255, 247)

#Welcome screen
window.fill(DARK_BLUE)
font = pygame.font.SysFont('verdana', 30)
win_text = font.render('Welcome to Arkanoid!', True, BLUE)
window.blit(win_text, (100, 200))
pygame.display.update()
sleep(3)

random_x = randint(0, 450)

#Objects
Ball = Picture('ball.png', random_x, rect_y, 50, 50)
Platform = Picture('platform.png', random_x, 400, 80, 25)
Enemy = Picture('enemy.png', 100, 60, 50, 50)

#Monsters
count = 24

Monsters = []
for j in range(3):
    y = start_y + j*55
    x = start_x + 27*j
    for i in range(count):
        d = Picture('enemy.png', x, y, 60, 60)
        Monsters.append(d)
        x = x + 60
        if x > 500 - 60:
            x = start_x + 27*j
            y = y + 70
        
        count = count - 1

#Score label
score = 0

font = pygame.font.SysFont('verdana', 25)
score_text = font.render('Score: ' + str(score), True, YELLOW)

game_over = False
win = False

#Set ball speed
speed_x = -3
speed_y = -3

#Set platform speed
platform_speed = 20

window.fill(BACK)
pygame.display.update()
clock.tick(40)   
sleep(0.6)
Ball.draw()
pygame.display.update()
clock.tick(40)   
sleep(0.5)
Platform.draw()  
pygame.display.update()
clock.tick(40)   
sleep(0.5)
for m in Monsters:
    m.draw()
    sleep(0.05)
    pygame.display.update()
    clock.tick(40)   
sleep(0.2)
score_text = font.render('Score: ' + str(score), True, YELLOW)
window.blit(score_text, (10, 450))

pygame.display.update()
clock.tick(40)   

sleep(1.5)


while not game_over and not win: 
    #Moving platform
    for event in pygame.event.get():   
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_RIGHT:
                    Platform.rect.x += platform_speed
            if event.key == pygame.K_LEFT:   
                    Platform.rect.x -= platform_speed
    Ball.rect.x += speed_x
    Ball.rect.y += speed_y

    res = Ball.colliderect(Platform.rect)
    #if ball touch monsters
    for m in Monsters:
        if Ball.colliderect(m.rect):
            Monsters.remove(m)
            score += 1
            score_text = font.render('Score: ' + str(score), True, YELLOW)
            res = True
            break
    if len(Monsters) == 0:
        win = True
    #Bounce
    if Ball.rect.y < 0:
        speed_y *= -1
    if Ball.rect.x > 450 or Ball.rect.x < 0:
        speed_x *= -1
    if res:
        speed_y *= -1
    
    #Lose condition
    if Ball.rect.y > 500:
        game_over = True

    window.fill(BACK)
    Ball.draw()
    Platform.draw()  
    for m in Monsters:
        m.draw()
    window.blit(score_text, (10, 450))
    pygame.display.update()   
    clock.tick(40)   

if win == True:
    window.fill((144, 238, 144))
    font = pygame.font.SysFont('verdana', 60)
    win_text = font.render('YOU WIN!!!', True, (0, 0, 0))
    window.blit(win_text, (100, 200))
    pygame.display.update()
    sleep(4.5)
elif game_over == True:
    window.fill((255, 95, 87))
    font = pygame.font.SysFont('verdana', 60)
    lose_text = font.render('You lost!', True, (0, 0, 0))
    window.blit(lose_text, (125, 200))
    pygame.display.update()
    sleep(4)