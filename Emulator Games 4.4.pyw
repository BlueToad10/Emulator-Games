import os, pygame
from pygame.locals import *
from terminate import *
from waitForPlayerToPressKey import *
from DrawTextFileFont import *

WINDOWSIZE = (720, 480)
BACKGROUNDCOLOR = (0, 0, 0)
LEFT=musicSelect=1
RIGHT=3
FPS=60
PAGE=NUMBER=gamesNum=systemNum=nesNum=snesNum=n64Num=gbNum=gbaNum=gcwiiNum=musicNum=0
Branch = "System"
GameName = ""
MaxNum=6
MusicSwitch=False

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Emulator Games 4.4.1")
icon = pygame.transform.scale(pygame.image.load('GameBoy.png'), (32, 32))
pygame.display.set_icon(icon)
windowSurface = pygame.display.set_mode(WINDOWSIZE)
mainClock = pygame.time.Clock()
pygame.mixer.music.load("4.0.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.pause()

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

musicList = []
nes = []
snes = []
n64 = []
gb = []
gba = []
gcWii = []

nesGames=[]
snesGames=[]
n64Games=[]
gbGames=[]
gbaGames=[]
gcWiiGames=[]
for object in os.listdir():
    if str(object).endswith(".nes"):
        nes.append(object)
        nesGames.append(os.path.splitext(object)[0])
        nesNum += 1
        gamesNum += 1
    elif str(object).endswith(".smc") or str(object).endswith(".sfc"):
        snes.append(object)
        snesGames.append(os.path.splitext(object)[0])
        snesNum += 1
        gamesNum += 1
    elif str(object).endswith(".n64") or str(object).endswith(".z64"):
        n64.append(object)
        n64Games.append(os.path.splitext(object)[0])
        n64Num += 1
        gamesNum += 1
    elif str(object).endswith(".gbc") or str(object).endswith(".gb"):
        gb.append(object)
        gbGames.append(os.path.splitext(object)[0])
        gbNum += 1
        gamesNum += 1
    elif str(object).endswith(".gba") or str(object).endswith(".GBA"):
        gba.append(object)
        gbaGames.append(os.path.splitext(object)[0])
        gbaNum += 1
        gamesNum += 1
    elif str(object).endswith(".iso") or str(object).endswith(".wbfs"):
        gcWii.append(object)
        gcWiiGames.append(os.path.splitext(object)[0])
        gcwiiNum += 1
        gamesNum += 1
    elif str(object).endswith(".mp3"):
        musicList.append(object)
        musicNum += 1
system = []
if nesNum > 0:
    system.append("Nintendo Entertainment System")
    systemNum += 1
if snesNum > 0:
    system.append("Super Nintendo Entertainment System")
    systemNum += 1
if n64Num > 0:
    system.append("Nintendo 64")
    systemNum += 1
if gbNum > 0:
    system.append("GameBoy")
    systemNum += 1
if gbaNum > 0:
    system.append("GameBoy Advance")
    systemNum += 1
if gcwiiNum > 0:
    system.append("GameCube and Wii")
    systemNum += 1

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
        global NUMBER, Branch, systemNum
        if Branch == "System":
            self.MaxNum = systemNum
        elif Branch == "Nintendo Entertainment System":
            self.MaxNum = nesNum
        elif Branch == "Super Nintendo Entertainment System":
            self.MaxNum = snesNum
        elif Branch == "Nintendo 64":
            self.MaxNum = n64Num
        elif Branch == "GameBoy":
            self.MaxNum = gbNum
        elif Branch == "GameBoy Advance":
            self.MaxNum = gbaNum
        elif Branch == "GameCube and Wii":
            self.MaxNum = gcwiiNum
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
        global MusicSwitch
        if pygame.sprite.spritecollideany(self, select_list) or MusicSwitch == True:
            if self.play == True:
                self.image = musicImage2
                pygame.mixer.music.pause()
                self.play = False
            elif self.play == False:
                self.image = musicImage
                pygame.mixer.music.unpause()
                self.play = True
        MusicSwitch = False
    def changeMusic(self):
        if self.play == False:
            pygame.mixer.music.pause()
        elif self.play == True:
            pygame.mixer.music.unpause()

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
            if PAGE == 0 and gamesNum > 0:
                systemSelect()
            elif PAGE == 1:
                gameSelect()
            elif PAGE == 2:
                if Branch == "Nintendo Entertainment System":
                    os.startfile(str(nes[NUMBER]))
                elif Branch == "Super Nintendo Entertainment System":
                    os.startfile(str(snes[NUMBER]))
                elif Branch == "Nintendo 64":
                    os.startfile(str(n64[NUMBER]))
                elif Branch == "GameBoy":
                    os.startfile(str(gb[NUMBER]))
                elif Branch == "GameBoy Advance":
                    os.startfile(str(gba[NUMBER]))
                elif Branch == "GameCube and Wii":
                    os.startfile(str(gcWii[NUMBER]))

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

musicamajig = music()

def controls():
    global NUMBER, Branch, nesNum, snesNum, n64Num, gbNum, gbaNum, MaxNum, PAGE, gamesNum, systemNum, MusicSwitch, musicSelect, musicNum
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            select_list.update(event.pos[0], event.pos[1])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                background_list2.update()
                background_list3.update()
            if event.button == RIGHT:
                musicSelect += 1
                if musicSelect > musicNum - 1:
                    musicSelect = 0
                pygame.mixer.music.load(musicList[musicSelect])
                pygame.mixer.music.play(-1, 0.0)
                musicamajig.changeMusic()
        if event.type == KEYDOWN:
            if event.key == ord('m'):
                MusicSwitch = True
                musicamajig.update()
            if event.key == ord('o'):
                musicSelect += 1
                if musicSelect > musicNum - 1:
                    musicSelect = 0
                pygame.mixer.music.load(musicList[musicSelect])
                pygame.mixer.music.play()
                musicamajig.changeMusic()
            if event.key == K_ESCAPE:
                if PAGE == 0:
                    terminate()
                elif PAGE == 1:
                    titleScreen()
                elif PAGE == 2:
                    systemSelect()
            if event.key == K_RETURN:
                if PAGE == 0 and gamesNum > 0:
                    systemSelect()
                elif PAGE == 1:
                    gameSelect()
                elif PAGE == 2:
                    if Branch == "Nintendo Entertainment System":
                        os.startfile(str(nes[NUMBER]))
                    elif Branch == "Super Nintendo Entertainment System":
                        os.startfile(str(snes[NUMBER]))
                    elif Branch == "Nintendo 64":
                        os.startfile(str(n64[NUMBER]))
                    elif Branch == "GameBoy":
                        os.startfile(str(gb[NUMBER]))
                    elif Branch == "GameBoy Advance":
                        os.startfile(str(gba[NUMBER]))
                    elif Branch == "GameCube and Wii":
                        os.startfile(str(gcWii[NUMBER]))
            if event.key == K_LEFT or event.key == K_UP:
                NUMBER -= 1
                if NUMBER < 0:
                    NUMBER = 0
            if event.key == K_RIGHT or event.key == K_DOWN:
                NUMBER += 1
                numcheckplz()

def numcheckplz():
    global NUMBER, Branch, nesNum, snesNum, n64Num, gbNum, gbaNum, MaxNum, PAGE, gamesNum, systemNum, MusicSwitch, musicSelect, musicNum 
    if Branch == "System":
        MaxNum = systemNum
    elif Branch == "Nintendo Entertainment System":
        MaxNum = nesNum
    elif Branch == "Super Nintendo Entertainment System":
        MaxNum = snesNum
    elif Branch == "Nintendo 64":
        MaxNum = n64Num
    elif Branch == "GameBoy":
        MaxNum = gbNum
    elif Branch == "GameBoy Advance":
        MaxNum = gbaNum
    elif Branch == "GameCube and Wii":
        MaxNum = gcwiiNum
    if NUMBER >= MaxNum - 1:
        NUMBER = MaxNum - 1
    if NUMBER < 0:
        NUMBER = 0

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
        DrawText("4.4", "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 325, 150, 720, 480)
        DrawText(str(gamesNum) + " games", "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 10, 422, 720, 480)
        mainLoop()

def systemSelect():
    global PAGE, NUMBER, Branch, MaxNum, systemNum
    PAGE=1
    NUMBER=0
    Branch = "System"
    numcheckplz()
    while True:
        background_list.draw(windowSurface)
        background_list2.draw(windowSurface)
        background_list3.draw(windowSurface)
        select_list.draw(windowSurface)
        if NUMBER > 3:
            DrawText(str(system[NUMBER - 4]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 0, 720, 480)
        if NUMBER > 2:
            DrawText(str(system[NUMBER - 3]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 40, 720, 480)
        if NUMBER > 1:
            DrawText(str(system[NUMBER - 2]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 80, 720, 480)
        if NUMBER > 0:
            DrawText(str(system[NUMBER - 1]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 120, 720, 480)
        DrawText(str(system[NUMBER]), "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 125, 150, 720, 480)
        if NUMBER < MaxNum - 1:
            DrawText(str(system[NUMBER + 1]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 260, 720, 480)
        if NUMBER < MaxNum - 2:
            DrawText(str(system[NUMBER + 2]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 300, 720, 480)
        if NUMBER < MaxNum - 3:
            DrawText(str(system[NUMBER + 3]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 340, 720, 480)
        if NUMBER < MaxNum - 4:
            DrawText(str(system[NUMBER + 4]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 380, 720, 480)
        mainLoop()

def gameSelect():
    global PAGE, NUMBER, Branch, GameName, MaxNum
    PAGE=2
    Branch = system[NUMBER]
    NUMBER=0
    while True:
        background_list.draw(windowSurface)
        if Branch == "Nintendo Entertainment System":
            GameName = nesGames
            numcheckplz()
        elif Branch == "Super Nintendo Entertainment System":
            GameName = snesGames
            numcheckplz()
        elif Branch == "Nintendo 64":
            GameName = n64Games
            numcheckplz()
        elif Branch == "GameBoy":
            GameName = gbGames
            numcheckplz()
        elif Branch == "GameBoy Advance":
            GameName = gbaGames
            numcheckplz()
        elif Branch == "GameCube and Wii":
            GameName = gcWiiGames
            numcheckplz()

        if NUMBER > 3:
            DrawText(str(GameName[NUMBER - 4]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 0, 720, 40)
        if NUMBER > 2:
            DrawText(str(GameName[NUMBER - 3]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 40, 720, 80)
        if NUMBER > 1:
            DrawText(str(GameName[NUMBER - 2]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 80, 720, 120)
        if NUMBER > 0:
            DrawText(str(GameName[NUMBER - 1]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 120, 720, 150)
        DrawText(GameName[NUMBER], "moon_get-Heavy.ttf", 32, (255, 255, 255), windowSurface, 20, 150, 720, 260)
        if NUMBER < MaxNum - 1:
            DrawText(str(GameName[NUMBER + 1]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 260, 720, 300)
        if NUMBER < MaxNum - 2:
            DrawText(str(GameName[NUMBER + 2]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 300, 720, 340)
        if NUMBER < MaxNum - 3:
            DrawText(str(GameName[NUMBER + 3]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 340, 720, 380)
        if NUMBER < MaxNum - 4:
            DrawText(str(GameName[NUMBER + 4]), "moon_get-Heavy.ttf", 16, (255, 255, 255), windowSurface, 135, 380, 720, 480)
        background_list2.draw(windowSurface)
        background_list3.draw(windowSurface)
        select_list.draw(windowSurface)
        mainLoop()

background_list.add(background(backgroundImage))
background_list3.add(back())
background_list2.add(left())
background_list2.add(right())
background_list3.add(enter())
background_list3.add(musicamajig)
select_list.add(select())
titleScreen()
