import pygame, sys, random, time, threading, os
from pygame import mixer
# 7/22/2021
#todo make main menue, add power ups, colision, sound effects, music, pictures
pygame.init()
pygame.mixer.init()
os.getcwd()
levelScreen = 'menu'
s_width = 800
s_height = 600
screen = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Meteor Dodge")
meteor_list = []
player_list = []
meteor_count = 0
gamelevel = 1
player_lives = 3
meteorTime = 5

def getFile(filename):
    return os.path.join(os.path.dirname(__file__),os.path.join(('Source'), filename))
pygame.display.set_icon(pygame.image.load(getFile('icon.png')))
def comicsans(size):
    return pygame.font.Font(getFile('COMIC.TTF'), size)
def is_colide(x1,y1, w1, h1, x2, y2, w2, h2):
    if x1 > x2 and x1 + w1 < x2 + w2 and y1 > y2 and y1 + h1 < y2 + h2:
        return True
    else:
        return False
bg = pygame.image.load(getFile('meteor dodge menu.jpg'))
class button():
    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img

    def draw(self, w):
        w.blit(pygame.image.load(self.img), (self.x, self.y))
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y +self.height:
                return True
        return False


class Player(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = 7
        self.hitbox = (self.x +10, self.y+10, 40, 70)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0 + self.speed:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < s_width - self.w - self.speed:
            self.x += self.speed

    def draw(self, screen):
        self.move()
        screen.blit(pygame.image.load(getFile('rocketship.png')), (self.x, self.y))
        self.hitbox = (self.x + 10, self.y + 10, 40, 70)
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox,)
        #pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.w, self.h))

class Meteor(object):
    def __init__(self, level):
        self.level = level
        if self.level == 1:
            self.speed = 5
        elif self.level == 2:
            self.speed = 7
        elif self.level == 3:
            self.speed = 9
        elif self.level == 4:
            self.speed = 11
        elif self.level == 5:
            self.speed = random.randint(7, 16)
            meteorTime == .40
            self.size = random.randint(70, 160)
        if self.level < 5:
            self.size = random.randint(50, 130)
        self.x = random.randint(30, 770)
        self.y = 0
        self.run = True
        self.hitbox = (self.x, self.y, self.size, self.size)


    def move(self):
        self.y += self.speed

    def limit(self):
        if self.y > s_height:
            self.run = False

    def draw(self, screen):
        if self.run:
            self.move()
            self.limit()
            self.img = pygame.image.load(getFile('meteor.png'))
            self.newimg = pygame.transform.scale(self.img, (self.size, self.size))
            screen.blit(self.newimg, (self.x, self.y))
            self.hitbox = (self.x, self.y, self.size, self.size)
            for e in player_list:
                #   meteor y      player y       bottom of meteor y              bottom of player y
                if self.hitbox[1] + self.hitbox[3] > e.hitbox[1] and self.hitbox[1] < e.hitbox[1] + e.hitbox[3]:
                    if self.hitbox[0] < e.hitbox[0] + e.hitbox[2] and self.hitbox[0] + self.hitbox[2] > e.hitbox[0]:
                        print('hit')
                        self.hit()
            #pygame.draw.rect(screen, (255,0,0), self.hitbox)
            #pygame.draw.circle(screen, (139,69,19), (self.x, self.y), self.size)

    def hit(self):
        global player_lives
        self.run = False
        player_lives -= 1
        pygame.mixer.Channel(4).play(pygame.mixer.Sound(getFile('Explosion.wav')))
        print("player lives: " + str(player_lives))
        for m in meteor_list:
            m.run = False

def meteor_loop():
    global meteor_list
    global meteor_count
    global gamelevel
    global player_lives
    global meteorTime
    for meteor in meteor_list:
        meteor.run = False
    meteor_count = 0
    gamelevel = 1
    player_lives = 3

    start = True
    meteorTime = 5
    while start:

        meteor = Meteor(gamelevel)
        meteor_count += 1
        print('Meteor: ' + str(meteor_count))
        print('Delay: '+ str(meteorTime))
        meteor_list.append(meteor)
        time.sleep(meteorTime)
        if meteor_count == 100:
            return
        if player_lives == 0:
            return
        if meteorTime > .6:
            meteorTime -= .10







def game_win_menu():
    winbg = pygame.image.load(getFile('gamewin.jpg'))
    clock = pygame.time.Clock()
    winms = pygame.mixer.Channel(5).play(pygame.mixer.Sound(getFile('victory.wav')))
    againB = button(230, 350, 330, 100, getFile('menu1.jpg'))
    while True:
        clock.tick(30)
        screen.blit(winbg, (0,0))
        againB.draw(screen)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if againB.isOver(pos):

                    s1 = pygame.mixer.Channel(1).play(pygame.mixer.Sound(getFile('playsound.wav')))

                    main_menu()
            if event.type == pygame.MOUSEMOTION:
                if againB.isOver(pos):
                    againB.img = getFile('menubutton2.jpg')
                    s2 = pygame.mixer.Channel(0).play(pygame.mixer.Sound(getFile('click.wav')))

                else:
                    againB.img = getFile('menu1.jpg')

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def game_over_menu():
    global gamelevel
    winbg = pygame.image.load(getFile('gameover.jpg'))
    clock = pygame.time.Clock()
    winms = pygame.mixer.Channel(5).play(pygame.mixer.Sound(getFile('lose.wav')))
    againB = button(230, 350, 330, 100, getFile('menu1.jpg'))
    while True:
        clock.tick(30)
        screen.blit(winbg, (0, 0))
        againB.draw(screen)
        round = comicsans(50).render('You got to level: ' + str(gamelevel), True, (255, 255, 255))
        screen.blit(round, (200, 200))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if againB.isOver(pos):
                    s1 = pygame.mixer.Channel(1).play(pygame.mixer.Sound(getFile('playsound.wav')))
                    main_menu()
            if event.type == pygame.MOUSEMOTION:
                if againB.isOver(pos):
                    againB.img = getFile('menubutton2.jpg')
                    s2 = pygame.mixer.Channel(0).play(pygame.mixer.Sound(getFile('click.wav')))

                else:
                    againB.img = getFile('menu1.jpg')

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def game_menu():
    global player_lives
    global gamelevel
    global meteor_count
    threading.Thread(target=meteor_loop).start()

    screen.fill((0, 0, 0))
    gamems1 = pygame.mixer.Sound(getFile('gamemusic.wav'))
    gamems1.set_volume(0.1)
    pygame.mixer.Channel(3).play(gamems1, loops=-1)
    count = comicsans(200).render('3', True, (255,255,255))
    screen.blit(count, (300, 100))
    pygame.display.update()
    time.sleep(1)
    screen.fill((0, 0, 0))
    count = comicsans(200).render('2', True, (255, 255, 255))
    screen.blit(count, (300, 100))
    pygame.display.update()
    time.sleep(1)
    screen.fill((0, 0, 0))
    count = comicsans(200).render('1', True, (255, 255, 255))
    screen.blit(count, (300, 100))
    pygame.display.update()
    time.sleep(1)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(pygame.image.load(getFile('gamebg.jpg')), (0, 0))
        levelcount = comicsans(50).render('Level: ' + str(gamelevel), True, (255, 255, 255))

        for meteor in meteor_list:
            meteor.draw(screen)

        screen.blit(levelcount, (10, 10))
        if player_lives == 3:
            pygame.draw.circle(screen, (255, 0, 0), (760, 30), 25)
            pygame.draw.circle(screen, (255, 0, 0), (700, 30), 25)
            pygame.draw.circle(screen, (255, 0, 0), (640, 30), 25)
        elif player_lives == 2:
            pygame.draw.circle(screen, (255, 0, 0), (760, 30), 25)
            pygame.draw.circle(screen, (255, 0, 0), (700, 30), 25)
        elif player_lives == 1:
            pygame.draw.circle(screen, (255, 0, 0), (760, 30), 25)
        elif player_lives == 0:
            pygame.mixer.Channel(3).pause()
            game_over_menu()

        if meteor_count == 10:
            gamelevel = 2
        elif meteor_count == 20:
            gamelevel = 3
        elif meteor_count == 35:
            gamelevel = 4
        elif meteor_count == 55:
            gamelevel = 5
        elif meteor_count == 100:
            pygame.mixer.Channel(3).pause()
            game_win_menu()

        for player in player_list:
            player.draw(screen)

        pygame.display.update()

player = Player(400, 500, 60, 80)
player_list.append(player)

def main_menu():
    bgm = pygame.mixer.Sound(getFile('bgmusic.wav'))
    bgm.set_volume(0.2)
    pygame.mixer.Channel(2).play(bgm, loops=-1)

    pygame.mixer.music.set_volume(0.5)
    startB = button(230, 350, 330, 100, getFile('start button1.jpg'))
    clock = pygame.time.Clock()
    while True:
        screen.blit(bg, (0, 0))
        startB.draw(screen)

        for event in pygame.event.get():

            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startB.isOver(pos):
                    pygame.mixer.Channel(2).pause()
                    s1 = pygame.mixer.Channel(1).play(pygame.mixer.Sound(getFile('playsound.wav')))
                    game_menu()


            if event.type == pygame.MOUSEMOTION:
                if startB.isOver(pos):
                    startB.img = getFile('start button2.jpg')
                    s2 = pygame.mixer.Channel(0).play(pygame.mixer.Sound(getFile('click.wav')))

                else:
                    startB.img = getFile('start button1.jpg')

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(30)
main_menu()




