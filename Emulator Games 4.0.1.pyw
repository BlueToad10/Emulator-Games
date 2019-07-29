import os, pygame
from pygame.locals import *
from terminate import *
from waitForPlayerToPressKey import *
from DrawTextFileFont import *

WINDOWSIZE = (720, 480)
BACKGROUNDCOLOR = (0, 0, 0)
LEFT=1
FPS=60
PAGE=NUMBER=0
nesNum=snesNum=n64Num=gbNum=gbaNum=0
Branch = "System"
MaxNum=5
gamesNum = 0

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Emulator Games 4.0.1")
icon = pygame.transform.scale(pygame.image.load('GameBoy.png'), (32, 32))
pygame.display.set_icon(icon)
windowSurface = pygame.display.set_mode(WINDOWSIZE)
mainClock = pygame.time.Clock()
pygame.mixer.music.load("Super Paper Mario OST - Lineland Road.mp3")

background_list = pygame.sprite.Group()
background_list2 = pygame.sprite.Group()
background_list3 = pygame.sprite.Group()
select_list = pygame.sprite.Group()

backgroundImage = pygame.image.load('ground.png')
backImage = pygame.image.load('Back.png')
leftImage = pygame.image.load('ArrowLeft.png')
rightImage = pygame.image.load('ArrowRight.png')
selectImage = pygame.image.load('Select.png')
enterImage = pygame.image.load('Enter.png')
musicImage = pygame.image.load('Music on.png')
musicImage2 = pygame.image.load('Music off.png')
                                         
system = ["Nes", "Snes", "N64", "Gb", "Gba"]
nes = []
snes = []
n64 = []
gb = []
gba = []
for object in os.listdir():
    if str(object).endswith(".nes"):
        nes.append(object)
        nesNum += 1
        gamesNum += 1
    elif str(object).endswith(".smc") or str(object).endswith(".sfc"):
        snes.append(object)
        snesNum += 1
        gamesNum += 1
    elif str(object).endswith(".n64") or str(object).endswith(".z64"):
        n64.append(object)
        n64Num += 1
        gamesNum += 1
    elif str(object).endswith(".gbc") or str(object).endswith(".gb"):
        gb.append(object)
        gbNum += 1
        gamesNum += 1
    elif str(object).endswith(".gba") or str(object).endswith(".GBA"):
        gba.append(object)
        gbaNum += 1
        gamesNum += 1

class background(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
    def update(self):
        self.rect.x = self.rect.x - 1
        if self.rect.x <= -512:
            self.rect.x = 0

class back(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = backImage
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
    def update(self):
        global PAGE
        if pygame.sprite.spritecollideany(self, select_list):
            if PAGE == 0:
                terminate()
            elif PAGE == 1:
                titleScreen()
            elif PAGE == 2:
                systemSelect()

class left(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = leftImage
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 360
    def update(self):
        global PAGE, NUMBER
        if pygame.sprite.spritecollideany(self, select_list):
            NUMBER -= 1
            if NUMBER < 0:
                NUMBER = 0

class right(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rightImage
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 360
        self.MaxNum = 0
    def update(self):
        global PAGE, NUMBER, Branch
        if Branch == "system":
            self.MaxNum = 5
        elif Branch == "nes":
            self.MaxNum = nesNum
        elif Branch == "snes":
            self.MaxNum = snesNum
        elif Branch == "n64":
            self.MaxNum = n64Num
        elif Branch == "gb":
            self.MaxNum = gbNum
        elif Branch == "gba":
            self.MaxNum = gbaNum
        if pygame.sprite.spritecollideany(self, select_list):
            NUMBER += 1
            if NUMBER >= self.MaxNum - 1:
                NUMBER = self.MaxNum - 1

class music(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = musicImage2
        self.rect = self.image.get_rect()
        self.rect.x = 660
        self.rect.y = 0
        self.play = False
    def update(self):
        global PAGE, NUMBER
        if pygame.sprite.spritecollideany(self, select_list):
            if self.play == False:
                pygame.mixer.music.play(-1, 0.0)
                self.play = True
                self.image = musicImage
            elif self.play == True:
                pygame.mixer.music.pause()
                self.play = False
                self.image = musicImage2

class enter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enterImage
        self.rect = self.image.get_rect()
        self.rect.x = 270
        self.rect.y = 420
    def update(self):
        global PAGE, NUMBER, Branch
        if pygame.sprite.spritecollideany(self, select_list):
            if PAGE == 0:
                systemSelect()
            elif PAGE == 1:
                gameSelect()
            elif PAGE == 2:
                if Branch == "nes":
                    os.startfile(str(nes[NUMBER]))
                elif Branch == "snes":
                    os.startfile(str(snes[NUMBER]))
                elif Branch == "n64":
                    os.startfile(str(n64[NUMBER]))
                elif Branch == "gb":
                    os.startfile(str(gb[NUMBER]))
                elif Branch == "gba":
                    os.startfile(str(gba[NUMBER]))

class select(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = selectImage
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

def controls():
    global NUMBER, Branch, nesNum, snesNum, n64Num, gbNum, gbaNum, MaxNum, PAGE
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            select_list.update(event.pos[0], event.pos[1])
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            background_list2.update()
            background_list3.update()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if PAGE == 0:
                    terminate()
                elif PAGE == 1:
                    titleScreen()
                elif PAGE == 2:
                    systemSelect()
            if event.key == K_RETURN:
                if PAGE == 0:
                    systemSelect()
                elif PAGE == 1:
                    gameSelect()
                elif PAGE == 2:
                    if Branch == "nes":
                        os.startfile(str(nes[NUMBER]))
                    elif Branch == "snes":
                        os.startfile(str(snes[NUMBER]))
                    elif Branch == "n64":
                        os.startfile(str(n64[NUMBER]))
                    elif Branch == "gb":
                        os.startfile(str(gb[NUMBER]))
                    elif Branch == "gba":
                        os.startfile(str(gba[NUMBER]))
            if event.key == K_LEFT:
                NUMBER -= 1
                if NUMBER < 0:
                    NUMBER = 0
            if event.key == K_RIGHT:
                if Branch == "system":
                    MaxNum = 5
                elif Branch == "nes":
                    MaxNum = nesNum
                elif Branch == "snes":
                    MaxNum = snesNum
                elif Branch == "n64":
                    MaxNum = n64Num
                elif Branch == "gb":
                    MaxNum = gbNum
                elif Branch == "gba":
                    MaxNum = gbaNum
                NUMBER += 1
                if NUMBER >= MaxNum - 1:
                    NUMBER = MaxNum - 1

def mainLoop():
    pygame.display.update()
    background_list.update()
    mainClock.tick(FPS)
    controls()

def titleScreen():
    global PAGE, Branch, gamesNum
    PAGE=0
    while True:
        background_list.draw(windowSurface)
        background_list3.draw(windowSurface)
        select_list.draw(windowSurface)
        DrawText("Emulator Games", "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 200, 100, 720, 480)
        DrawText("4.0", "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 325, 150, 720, 480)
        DrawText(str(gamesNum) + " games", "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 10, 422, 720, 480)
        mainLoop()

def systemSelect():
    global PAGE, NUMBER, Branch
    PAGE=1
    NUMBER=0
    Branch = "system"
    while True:
        background_list.draw(windowSurface)
        background_list2.draw(windowSurface)
        background_list3.draw(windowSurface)
        select_list.draw(windowSurface)
        DrawText(str(system[NUMBER]), "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 325, 150, 720, 480)
        mainLoop()

def gameSelect():
    global PAGE, NUMBER, Branch
    PAGE=2
    Branch = system[NUMBER].lower()
    NUMBER=0
    while True:
        background_list.draw(windowSurface)
        background_list2.draw(windowSurface)
        background_list3.draw(windowSurface)
        select_list.draw(windowSurface)
        if Branch == "nes":
            DrawText(nes[NUMBER], "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 50, 150, 720, 480)
        elif Branch == "snes":
            DrawText(snes[NUMBER], "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 50, 150, 720, 480)
        elif Branch == "n64":
            DrawText(n64[NUMBER], "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 50, 150, 720, 480)
        elif Branch == "gb":
            DrawText(gb[NUMBER], "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 50, 150, 720, 480)
        elif Branch == "gba":
            DrawText(gba[NUMBER], "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 50, 150, 720, 480)
        mainLoop()

background_list.add(background(backgroundImage))
background_list3.add(back())
background_list2.add(left())
background_list2.add(right())
background_list3.add(enter())
background_list3.add(music())
select_list.add(select())
titleScreen()
