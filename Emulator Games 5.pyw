import os, pygame, random, sys
from pygame.locals import *
from assets.python.terminate import *
from assets.python.waitForPlayerToPressKey import *
from assets.python.DrawTextFileFont import *
from assets.python.keyboardInput import *

version = "Emulator Games 5.2.6"
WINDOWSIZE = (720, 480)
BACKGROUNDCOLOR = (0, 0, 0)
TEXTCOLOUR = (255, 255, 255)
LEFT=musicSelect=1
RIGHT=3
FPS=60
PAGE=NUMBER=gamesNum=MaxNum=systemNum=systemNUMBER=0
GameName = ""
MusicSwitch=isFullscreen=False
pause=True

pygame.init()
pygame.mixer.init()
pygame.display.set_caption(version)
icon = pygame.image.load('assets\\icon.png')
pygame.display.set_icon(icon)
windowSurface = pygame.display.set_mode(WINDOWSIZE)
mainClock = pygame.time.Clock()
pygame.mixer.music.load("assets\\music\\version_5.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.pause()
font = "assets\\moon_get-Heavy.ttf"

main_list = pygame.sprite.Group()
options_list = pygame.sprite.Group()
page_list = pygame.sprite.Group()
select_list = pygame.sprite.Group()
background_list=[]
button_list=[]
for object in sorted(os.listdir("assets\\background"), key=len):
    background_list.append(pygame.image.load("assets\\background\\" + object))
for object in sorted(os.listdir("assets\\buttons"), key=len):
    button_list.append(pygame.image.load("assets\\buttons\\" + object))
theme=button_list[7]
selectImage = pygame.image.load('assets\\Select.png')

class themes():
    def __init__(self, name):
        global systemNum, PAGE, TEXTCOLOUR
        self.buttonsFile = "assets\\themes\\" + str(name) + "\\buttons"
        self.backgroundFile = "assets\\themes\\" + str(name) + "\\background"
        self.buttonsList = []
        self.backgroundList = []
        self.TEXTCOLOUR = open("assets\\themes\\" + str(name) + "\\TEXTCOLOUR.txt")
        for line in self.TEXTCOLOUR:
            if not line == "":
                self.line = line.split(" ")
                self.TEXTCOLOUR = (int(self.line[0]), int(self.line[1]), int(self.line[2]))
        for object in sorted(os.listdir(str(self.buttonsFile)), key=len):
            self.buttonsList.append(pygame.image.load(str(self.buttonsFile) + "\\" + object))
        for object in sorted(os.listdir(str(self.backgroundFile)), key=len):
            self.backgroundList.append(pygame.image.load(str(self.backgroundFile) + "\\" + object))

themeList = []
maxThemeNum=-1
skinNum = 0
for object in os.listdir("assets\\themes"):
    object = themes(object)
    themeList.append(object)
    maxThemeNum+=1

def skin():
    global maxThemeNum, skinNum, button_list, background_list, theme, TEXTCOLOUR
    if maxThemeNum >= 0:
        if skinNum > maxThemeNum:
            skinNum = maxThemeNum
        elif skinNum < 0:
            skinNum = 0
        background_list = []
        background_list = themeList[skinNum].backgroundList
        button_list = []
        button_list = themeList[skinNum].buttonsList
        TEXTCOLOUR = themeList[skinNum].TEXTCOLOUR
        theme=button_list[7]
        for object in main_list:
            object.skin()
        for object in options_list:
            object.skin()
        for object in page_list:
            object.skin()

systems=[]
system=[]
gameslist=[]
system.append("All")
system.append("Search")
systems.append("All")
systems.append("Search")
systemNum += 2
Searchmaxnum=-1
Search = []
SearchList = []
SearchName = ""
All = []

class allList():
    def __init__(self):
        global gamesNum
        for object in os.listdir("roms"):
            self.filename = "roms\\" + str(object)
            for object in os.listdir(str(self.filename)):
                gameslist.append(object)
                All.append(str(self.filename) + "\\" + str(object))
                gamesNum += 1

class searchList():
    def __init__(self, name, nameAgain):
        global Searchmaxnum, Search, SearchList
        Searchmaxnum=-1
        Search = []
        SearchList = []
        SearchName = ""
        for object in os.listdir("roms"):
            self.filename = "roms\\" + str(object)
            self.nameAgain = nameAgain
            for object in os.listdir(str(self.filename)):
                if any(self.nameAgain.lower() in word and len(word) > 1 for word in object.lower().split()) == True:
                    Search.append(object)
                    SearchList.append(str(self.filename) + "\\" + str(object))
                    Searchmaxnum += 1

class lists():
    def __init__(self, name, nameAgain):
        global systemNum, PAGE
        self.filename = "roms\\" + str(name)
        self.maxnum = 0
        self.nameAgain = nameAgain
        name = []
        for object in os.listdir(str(self.filename)):
            name.append(object)
            self.maxnum += 1
        if self.maxnum > 0:
            systems.append(name)
            if not PAGE == 2:
                systemNum += 1
            system.append(self.nameAgain)
        
for object in os.listdir("roms"):
    object = lists(object, object)

allList()
musicList = []
musicNum = 0
for object in sorted(os.listdir("assets\\music"), key=len):
    if str(object).endswith(".mp3"):
        musicList.append("assets\\music\\" + str(object))
        musicNum += 1

class window(pygame.sprite.Sprite):
    def __init__(self, imageType, x, y, sizex, sizey, shade):
        global theme
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(imageType, (sizex, sizey))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.play = False
        self.shade = shade
        self.sizex = sizex
        self.sizey = sizey
    def backbutton(self):
        global PAGE
        if pygame.sprite.spritecollideany(self, select_list):
            if PAGE == 0:
                terminate()
            elif PAGE == 1:
                titleScreen()
            elif PAGE >= 2 and PAGE <= 6 and not PAGE == 3:
                systemSelect()
            elif PAGE == 3:
                settingsSave()
                titleScreen()
    def themebutton(self):
        global PAGE, theme, TEXTCOLOUR
        if pygame.sprite.spritecollideany(self, select_list):
            if theme == button_list[7]:
                theme = button_list[8]
            elif theme == button_list[8]:
                theme = button_list[7]
            main_list.update()
            options_list.update()
            page_list.update()
    def settingsbutton(self):
        global PAGE
        if pygame.sprite.spritecollideany(self, select_list):
            if PAGE == 3:
                settingsSave()
                titleScreen()
            else:
                settingsScreen()
    def leftbutton(self):
        global PAGE, NUMBER
        if pygame.sprite.spritecollideany(self, select_list):
            NUMBER -= 1
            if NUMBER < 0:
                NUMBER = 0
    def rightbutton(self):
        global NUMBER, systemNum, MaxNum
        numcheckplz()
        if pygame.sprite.spritecollideany(self, select_list):
            NUMBER += 1
            if NUMBER >= MaxNum - 1:
                NUMBER = MaxNum - 1
    def musicbutton(self):
        global MusicSwitch, pause
        if pygame.sprite.spritecollideany(self, select_list) or MusicSwitch == True:
            if self.play == True:
                self.image = button_list[4]
                pygame.mixer.music.pause()
                pause=True
                self.play = False
                settingsSave()
            elif self.play == False:
                self.image = button_list[5]
                pygame.mixer.music.unpause()
                pause=False
                self.play = True
                settingsSave()
        MusicSwitch = False
    def changeMusic(self):
        global musicSelect
        if pygame.sprite.spritecollideany(self, select_list):
            musicSelect += 1
            if musicSelect > musicNum - 1:
                musicSelect = 0
            pygame.mixer.music.load(musicList[musicSelect])
            pygame.mixer.music.play(-1, 0.0)
            if self.play == False:
                pygame.mixer.music.pause()
            elif self.play == True:
                pygame.mixer.music.unpause()
    def imagechange(self):
        global pause
        if pause == True:
            self.image = button_list[4]
            self.play = False
        elif pause == False:
            self.image = button_list[5]
            self.play = True
    def enterbutton(self):
        global PAGE, NUMBER
        if pygame.sprite.spritecollideany(self, select_list):
            if PAGE == 0 and gamesNum > 0:
                systemSelect()
            elif PAGE == 1:
                gameSelect()
            elif PAGE == 2:
                startrom()
            elif PAGE == 5:
                os.startfile(str(SearchList[NUMBER]))
            elif PAGE == 6:
                os.startfile(str(All[NUMBER]))
    def background(self):
        self.rect.x -= 1
        if self.rect.x == -512:
            self.rect.x = 0
    def screenbutton(self, skip):
        global isFullscreen
        if pygame.sprite.spritecollideany(self, select_list) or skip == True:
            if bool(isFullscreen) == False:
                windowSurface = pygame.display.set_mode(WINDOWSIZE)
                isFullscreen = True
                self.image = button_list[9]
            elif bool(isFullscreen) == True:
                windowSurface = pygame.display.set_mode(WINDOWSIZE, FULLSCREEN)
                isFullscreen = False
                self.image = button_list[10]
    def themeClickleft(self):
        global skinNum
        if pygame.sprite.spritecollideany(self, select_list):
            skinNum -= 1
            skin()
            settingsSave()
    def themeClickright(self):
        global skinNum
        if pygame.sprite.spritecollideany(self, select_list):
            skinNum += 1
            skin()
            settingsSave()
    def skin(self):
        if self == sheikahtext:
            self.image = pygame.transform.scale(background_list[1], (1536, 480))
        elif self == background:
            self.image = pygame.transform.scale(background_list[0], (720, 480))
        elif self == sheikah:
            self.image = pygame.transform.scale(background_list[random.randint(2,3)], (720, 480))
        elif self == backshade:
            self.image = pygame.transform.scale(theme, (60, 60))
        elif self == settingsshade:
            self.image = pygame.transform.scale(theme, (60, 60))
        elif self == entershade:
            self.image = pygame.transform.scale(theme, (180, 60))
        elif self == musicshade:
            self.image = pygame.transform.scale(theme, (60, 60))
        elif self == optionsshade:
            self.image = pygame.transform.scale(theme, (720, 420))
        elif self == themeshade:
            self.image = pygame.transform.scale(theme, (200, 60))
        elif self == leftshade:
            self.image = pygame.transform.scale(theme, (120, 120))
        elif self == rightshade:
            self.image = pygame.transform.scale(theme, (120, 120))
        elif self == screenshade:
            self.image = pygame.transform.scale(theme, (60, 60))
        elif self == back:
            self.image = pygame.transform.scale(button_list[2], (60, 60))
        elif self == settings:
            self.image = pygame.transform.scale(button_list[6], (60, 60))
        elif self == enter:
            self.image = pygame.transform.scale(button_list[3], (180, 60))
        elif self == left:
            self.image = pygame.transform.scale(button_list[0], (120, 120))
        elif self == right:
            self.image = pygame.transform.scale(button_list[1], (120, 120))
        elif self == theme_button:
            self.image = pygame.transform.scale(button_list[11], (60, 60))
        elif self == themeLeft:
            self.image = pygame.transform.scale(button_list[0], (60, 60))
        elif self == themeRight:
            self.image = pygame.transform.scale(button_list[1], (60, 60))
        elif self == musicamajig:
            self.image = pygame.transform.scale(button_list[4], (60, 60))
            self.imagechange()
        elif self == screen:
            self.image = pygame.transform.scale(button_list[9], (60, 60))
    def update(self):
        if theme == button_list[8] and self.shade == True:
            self.image = pygame.transform.scale(button_list[8], (self.sizex, self.sizey))
        elif theme == button_list[7] and self.shade == True:
            self.image = pygame.transform.scale(button_list[7], (self.sizex, self.sizey))
        

def settingsScreen():
    global PAGE, gamesNum, TEXTCOLOUR
    PAGE=3
    while True:
        select_list.draw(windowSurface)
        DrawText("Theme:", font, 32, (0, 144, 255), windowSurface, 30, 120, 720, 480)
        DrawText("Music:", font, 32, TEXTCOLOUR, windowSurface, 420, 120, 720, 480)
        DrawText("Screen Mode:", font, 32, TEXTCOLOUR, windowSurface, 30, 200, 720, 480)
        mainLoop()
        options_list.draw(windowSurface)
        mainClock.tick(FPS)
        controls()

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
    global NUMBER, PAGE, MusicSwitch, musicSelect, musicNum
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            select_list.update(event.pos[0], event.pos[1])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                back.backbutton()
                enter.enterbutton()
                settings.settingsbutton()
                left.leftbutton()
                right.rightbutton()
                if PAGE == 3:
                    theme_button.themebutton()
                    musicamajig.musicbutton()
                    screen.screenbutton(False)
                    themeLeft.themeClickleft()
                    themeRight.themeClickright()
            if event.button == RIGHT and musicNum > 1:
                musicamajig.changeMusic()
        if event.type == QUIT:
            terminate()
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
                elif PAGE >= 2 and PAGE <= 6 and not PAGE == 3:
                    systemSelect()
                elif PAGE == 3:
                    settingsSave()
                    titleScreen()
            if event.key == K_RETURN:
                if PAGE == 0 and gamesNum > 0:
                    systemSelect()
                elif PAGE == 1:
                    gameSelect()
                elif PAGE == 2:
                    startrom()
                elif PAGE == 5:
                    os.startfile(str(SearchList[NUMBER]))
                elif PAGE == 6:
                    os.startfile(str(All[NUMBER]))
            if event.key == K_LEFT or event.key == K_UP:
                NUMBER -= 1
                if NUMBER < 0:
                    NUMBER = 0
            if event.key == K_RIGHT or event.key == K_DOWN:
                NUMBER += 1
                numcheckplz()

def startrom():
    global NUMBER, GameName, systemNUMBER
    os.startfile('roms\\' + str(system[systemNUMBER]) + "\\" + str(GameName[NUMBER]))
        
def numcheckplz():
    global NUMBER, MaxNum, systemNum, MusicSwitch, musicSelect, musicNum 
    if PAGE == 1:
        MaxNum = systemNum
    if NUMBER >= MaxNum - 1:
        NUMBER = MaxNum - 1
    if NUMBER < 0:
        NUMBER = 0

def mainLoop():
    pygame.display.update()
    sheikahtext.background()
    main_list.draw(windowSurface)
    select_list.draw(windowSurface)
    mainClock.tick(FPS)
    controls()

def titleScreen():
    global PAGE, gamesNum, TEXTCOLOUR
    PAGE=0
    while True:
        DrawText("Emulator Games", font, 32, TEXTCOLOUR, windowSurface, 200, 130, 720, 480)
        DrawText("5", font, 32, TEXTCOLOUR, windowSurface, 348, 200, 720, 480)
        DrawText(str(gamesNum) + " Games", font, 32, TEXTCOLOUR, windowSurface, 10, 422, 720, 480)
        mainLoop()

def systemSelect():
    global PAGE, NUMBER, MaxNum, systemNum, TEXTCOLOUR
    PAGE=1
    NUMBER=0
    MaxNum = systemNum
    numcheckplz()
    while True:
        select_list.draw(windowSurface)
        if NUMBER > 3:
            DrawText(str(system[NUMBER - 4]), font, 16, TEXTCOLOUR, windowSurface, 135, 0, 720, 480)
        if NUMBER > 2:
            DrawText(str(system[NUMBER - 3]), font, 16, TEXTCOLOUR, windowSurface, 135, 40, 720, 480)
        if NUMBER > 1:
            DrawText(str(system[NUMBER - 2]), font, 16, TEXTCOLOUR, windowSurface, 135, 80, 720, 480)
        if NUMBER > 0:
            DrawText(str(system[NUMBER - 1]), font, 16, TEXTCOLOUR, windowSurface, 135, 120, 720, 480)
        DrawText(str(system[NUMBER]), font, 32, TEXTCOLOUR, windowSurface, 125, 150, 720, 480)
        if NUMBER < MaxNum - 1:
            DrawText(str(system[NUMBER + 1]), font, 16, TEXTCOLOUR, windowSurface, 135, 260, 720, 480)
        if NUMBER < MaxNum - 2:
            DrawText(str(system[NUMBER + 2]), font, 16, TEXTCOLOUR, windowSurface, 135, 300, 720, 480)
        if NUMBER < MaxNum - 3:
            DrawText(str(system[NUMBER + 3]), font, 16, TEXTCOLOUR, windowSurface, 135, 340, 720, 480)
        if NUMBER < MaxNum - 4:
            DrawText(str(system[NUMBER + 4]), font, 16, TEXTCOLOUR, windowSurface, 135, 380, 720, 480)
        page_list.draw(windowSurface)
        mainLoop()

def keyboardInput(x, y, Mx, My, letterLimit, fontType, fontSize, textcolour, surface):
    global NUMBER, PAGE, MusicSwitch, musicSelect, musicNum
    WORD = ""
    while True:
        pygame.display.update()
        sheikahtext.background()
        main_list.draw(windowSurface)
        select_list.draw(windowSurface)
        DrawText("Type 1 keyword to search", fontType, 32, textcolour, windowSurface, x, y-48, Mx, My)
        DrawText(WORD, fontType, 32, textcolour, windowSurface, x, y, Mx, My)
        mainClock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                select_list.update(event.pos[0], event.pos[1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    back.backbutton()
                    enter.enterbutton()
                    settings.settingsbutton()
                    left.leftbutton()
                    right.rightbutton()
                if event.button == RIGHT and musicNum > 1:
                    musicamajig.changeMusic()
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if PAGE == 0:
                        terminate()
                    elif PAGE == 1:
                        titleScreen()
                    elif PAGE == 2 or PAGE == 4 or PAGE == 5:
                        systemSelect()
                    elif PAGE == 3:
                        settingsSave()
                        titleScreen()
                if event.key == ord('a'):
                    WORD += "a"
                if event.key == ord('b'):
                    WORD += "b"
                if event.key == ord('c'):
                    WORD += "c"
                if event.key == ord('d'):
                    WORD += "d"
                if event.key == ord('e'):
                    WORD += "e"
                if event.key == ord('f'):
                    WORD += "f"
                if event.key == ord('g'):
                    WORD += "g"
                if event.key == ord('h'):
                    WORD += "h"
                if event.key == ord('i'):
                    WORD += "i"
                if event.key == ord('j'):
                    WORD += "j"
                if event.key == ord('k'):
                    WORD += "k"
                if event.key == ord('l'):
                    WORD += "l"
                if event.key == ord('m'):
                    WORD += "m"
                if event.key == ord('n'):
                    WORD += "n"
                if event.key == ord('o'):
                    WORD += "o"
                if event.key == ord('p'):
                    WORD += "p"
                if event.key == ord('q'):
                    WORD += "q"
                if event.key == ord('r'):
                    WORD += "r"
                if event.key == ord('s'):
                    WORD += "s"
                if event.key == ord('t'):
                    WORD += "t"
                if event.key == ord('u'):
                    WORD += "u"
                if event.key == ord('v'):
                    WORD += "v"
                if event.key == ord('w'):
                    WORD += "w"
                if event.key == ord('x'):
                    WORD += "x"
                if event.key == ord('y'):
                    WORD += "y"
                if event.key == ord('z'):
                    WORD += "z"
                if event.key == ord('1'):
                    WORD += "1"
                if event.key == ord('2'):
                    WORD += "2"
                if event.key == ord('3'):
                    WORD += "3"
                if event.key == ord('4'):
                    WORD += "4"
                if event.key == ord('5'):
                    WORD += "5"
                if event.key == ord('6'):
                    WORD += "6"
                if event.key == ord('7'):
                    WORD += "7"
                if event.key == ord('8'):
                    WORD += "8"
                if event.key == ord('9'):
                    WORD += "9"
                if event.key == ord('0'):
                    WORD += "0"
                if event.key == K_BACKSPACE:
                    WORD = WORD[:-1]
                if event.key == K_SPACE:
                    WORD += " "
                WORD = WORD[:letterLimit]
                if event.key == K_RETURN:
                    return WORD

def gameSelect():
    global PAGE, NUMBER, GameName, MaxNum, TEXTCOLOUR, systemNUMBER, gamesNum
    systemNUMBER = NUMBER
    GameName = systems[NUMBER]
    if GameName == "Search":
        PAGE = 4
        SearchName = keyboardInput(20, 150, 700, 460, 32, font, 32, TEXTCOLOUR, windowSurface)
        searchList(SearchName, SearchName)
        NUMBER=0
        MaxNum=Searchmaxnum
        PAGE = 5
        while True:
            if Searchmaxnum < 0:
                systemSelect()
            if NUMBER > 3:
                DrawText(os.path.splitext(str(Search[NUMBER - 4]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 0, 720, 40)
            if NUMBER > 2:
                DrawText(os.path.splitext(str(Search[NUMBER - 3]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 40, 720, 80)
            if NUMBER > 1:
                DrawText(os.path.splitext(str(Search[NUMBER - 2]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 80, 720, 120)
            if NUMBER > 0:
                DrawText(os.path.splitext(str(Search[NUMBER - 1]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 120, 720, 150)
            DrawText(os.path.splitext(Search[NUMBER])[0], font, 32, TEXTCOLOUR, windowSurface, 20, 150, 720, 260)
            if NUMBER < MaxNum - 1:
                DrawText(os.path.splitext(str(Search[NUMBER + 1]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 260, 720, 300)
            if NUMBER < MaxNum - 2:
                DrawText(os.path.splitext(str(Search[NUMBER + 2]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 300, 720, 340)
            if NUMBER < MaxNum - 3:
                DrawText(os.path.splitext(str(Search[NUMBER + 3]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 340, 720, 380)
            if NUMBER < MaxNum - 4:
                DrawText(os.path.splitext(str(Search[NUMBER + 4]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 380, 720, 480)
            page_list.draw(windowSurface)
            select_list.draw(windowSurface)
            mainLoop()
    elif GameName == "All":
        PAGE=6
        MaxNum = gamesNum
        NUMBER=0
        while True:
            if NUMBER > 3:
                DrawText(os.path.splitext(str(gameslist[NUMBER - 4]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 0, 720, 40)
            if NUMBER > 2:
                DrawText(os.path.splitext(str(gameslist[NUMBER - 3]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 40, 720, 80)
            if NUMBER > 1:
                DrawText(os.path.splitext(str(gameslist[NUMBER - 2]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 80, 720, 120)
            if NUMBER > 0:
                DrawText(os.path.splitext(str(gameslist[NUMBER - 1]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 120, 720, 150)
            DrawText(os.path.splitext(gameslist[NUMBER])[0], font, 32, TEXTCOLOUR, windowSurface, 20, 150, 720, 260)
            if NUMBER < MaxNum - 1:
                DrawText(os.path.splitext(str(gameslist[NUMBER + 1]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 260, 720, 300)
            if NUMBER < MaxNum - 2:
                DrawText(os.path.splitext(str(gameslist[NUMBER + 2]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 300, 720, 340)
            if NUMBER < MaxNum - 3:
                DrawText(os.path.splitext(str(gameslist[NUMBER + 3]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 340, 720, 380)
            if NUMBER < MaxNum - 4:
                DrawText(os.path.splitext(str(gameslist[NUMBER + 4]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 380, 720, 480)
            page_list.draw(windowSurface)
            select_list.draw(windowSurface)
            mainLoop()
    else:
        PAGE=2
        MaxNum = lists(system[NUMBER], system[NUMBER]).maxnum
        NUMBER=0
        while True:
            if NUMBER > 3:
                DrawText(os.path.splitext(str(GameName[NUMBER - 4]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 0, 720, 40)
            if NUMBER > 2:
                DrawText(os.path.splitext(str(GameName[NUMBER - 3]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 40, 720, 80)
            if NUMBER > 1:
                DrawText(os.path.splitext(str(GameName[NUMBER - 2]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 80, 720, 120)
            if NUMBER > 0:
                DrawText(os.path.splitext(str(GameName[NUMBER - 1]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 120, 720, 150)
            DrawText(os.path.splitext(GameName[NUMBER])[0], font, 32, TEXTCOLOUR, windowSurface, 20, 150, 720, 260)
            if NUMBER < MaxNum - 1:
                DrawText(os.path.splitext(str(GameName[NUMBER + 1]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 260, 720, 300)
            if NUMBER < MaxNum - 2:
                DrawText(os.path.splitext(str(GameName[NUMBER + 2]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 300, 720, 340)
            if NUMBER < MaxNum - 3:
                DrawText(os.path.splitext(str(GameName[NUMBER + 3]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 340, 720, 380)
            if NUMBER < MaxNum - 4:
                DrawText(os.path.splitext(str(GameName[NUMBER + 4]))[0], font, 16, TEXTCOLOUR, windowSurface, 135, 380, 720, 480)
            page_list.draw(windowSurface)
            select_list.draw(windowSurface)
            mainLoop()

musicamajig = window(button_list[4], 580, 120, 60, 60, False)
screen = window(button_list[9], 300, 200, 60, 60, False)

def settingsLoad():
    global theme, TEXTCOLOUR, pause, musicSelect, isFullscreen, skinNum, musicNum
    for object in os.listdir("assets"):
        if object.endswith(".settings"):
            r = open("assets\\" + object, "r")
            words = [word.split('\n') for word in r.read().splitlines()]
            for line in words:
                if "skin" in str(line):
                    skinNum = int(line[0].split()[1])
                    skin()
                if "musicSelect" in str(line):
                    musicSelect = int(line[0].split()[1])
                    pygame.mixer.music.load(musicList[musicSelect])
                    pygame.mixer.music.play(-1, 0.0)
                if "theme = darkTheme" in str(line):
                    theme=button_list[7]
                elif "theme = lightTheme" in str(line):
                    theme=button_list[8]
                main_list.update()
                options_list.update()
                page_list.update()
                if "pausefalse" in str(line):
                    pygame.mixer.music.unpause()
                    pause=False
                    musicamajig.imagechange()
                elif "pausetrue" in str(line):
                    pygame.mixer.music.pause()
                    pause=True
                    musicamajig.imagechange()
                if "isFullscreen" in str(line):
                    isFullscreen = str(line).split(" ")[1]
                    if isFullscreen == "False":
                        isFullscreen=False
                        screen.screenbutton(True)
                    elif isFullscreen == "True":
                        isFullscreen=True
                        screen.screenbutton(True)
                if "TEXTCOLOUR" in str(line):
                    line[0]
                    #print(line[0])
                    
def settingsSave():
    global theme, TEXTCOLOUR, pause, isFullscreen, skinNum, maxSkinNum, musicNum
    for object in os.listdir("assets"):
        if object.endswith(".settings"):
            r = open("assets\\" + object, "w+")
            r.write("skin " + str(skinNum) + "\n")
            if theme == button_list[7]:
                r.write("theme = darkTheme \n")
            elif theme == button_list[8]:
                r.write("theme = lightTheme \n")
            if pause == True:
                r.write("pausetrue \n")
            elif pause == False:
                r.write("pausefalse \n")
            r.write("musicSelect " + str(musicSelect) + "\n")
            if isFullscreen == True:
                r.write("isFullscreen False \n")
            elif isFullscreen == False:
                r.write("isFullscreen True \n")
            else:
                r.write("isFullscreen False \n")
            r.write("TEXTCOLOUR = " + str(TEXTCOLOUR) + "\n")
            

settingsLoad()

background = window(background_list[0], 0, 0, 720, 480, False)
sheikah = window(background_list[random.randint(2,3)], 0, 0, 720, 480, False)
sheikahtext = window(background_list[1], 0, 0, 1536, 480, False)

backshade = window(theme, 0, 0, 60, 60, True)
settingsshade = window(theme, 660, 0, 60, 60, True)
entershade = window(theme, 270, 420, 180, 60, True)
musicshade = window(theme, 580, 120, 60, 60, True)
optionsshade = window(theme, 0, 60, 720, 420, True)
leftshade = window(theme, 0, 360, 120, 120, True)
rightshade = window(theme, 600, 360, 120, 120, True)
screenshade = window(theme, 300, 200, 60, 60, True)

back = window(button_list[2], 0, 0, 60, 60, False)
settings = window(button_list[6], 660, 0, 60, 60, False)
enter = window(button_list[3], 270, 420, 180, 60, False)
left = window(button_list[0], 0, 360, 120, 120, False)
right = window(button_list[1], 600, 360, 120, 120, False)

theme_button = window(button_list[11], 240, 120, 60, 60, False)
themeshade = window(theme, 170, 120, 200, 60, True)

themeLeft = window(button_list[0], 180, 120, 60, 60, False)
themeRight = window(button_list[1], 300, 120, 60, 60, False)

main_list.add(background)
main_list.add(sheikah)
main_list.add(sheikahtext)

main_list.add(backshade)
main_list.add(settingsshade)
main_list.add(entershade)
options_list.add(optionsshade)
options_list.add(musicshade)
options_list.add(themeshade)
options_list.add(screenshade)
page_list.add(leftshade)
page_list.add(rightshade)

options_list.add(musicamajig)
options_list.add(enter)
options_list.add(theme_button)
options_list.add(themeLeft)
options_list.add(themeRight)
options_list.add(screen)
main_list.add(back)
main_list.add(settings)
main_list.add(enter)
page_list.add(left)
page_list.add(right)

select_list.add(select())
settingsLoad()
titleScreen()
