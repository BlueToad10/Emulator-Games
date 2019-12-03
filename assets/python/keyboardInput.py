import pygame
from pygame.locals import *
from assets.python.terminate import *
from assets.python.DrawTextFileFont import *

#class keyboard(pygame.sprite.Sprite):
    #def __init__(self, imageType, x, y, sizex, sizey):
        #global theme
        #pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.transform.scale(imageType, (sizex, sizey))
        #self.rect = self.image.get_rect()
        #self.rect.x = x
        #self.rect.y = y
        #self.sizex = sizex
        #self.sizey = sizey
   # def a(self):
        #global WORD
        #if pygame.sprite.spritecollideany(self, select_list):
            #WORD += "a"

def keyboardInput(x, y, Mx, My, letterLimit, fontType, fontSize, textcolour, surface):
    WORD = ""
    while True:
        pygame.display.update()
        DrawText(WORD, fontType, 32, textcolour, windowSurface, x, y, Mx, My)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
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
                if event.key == K_RETURN:
                    return WORD
                WORD = WORD[:letterLimit]
