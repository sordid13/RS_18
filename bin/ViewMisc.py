import pygame
import os
from .Constants import *
from .Events import *

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 230, 0)
BLUE = (0, 0, 255)
YELLOW = (250, 250, 0)
PURPLE = (128, 0, 128)
PINK = (255, 182, 193)

fontName = ''

imgFolder = os.path.join("asset")

class DynamicText(pygame.sprite.Sprite):
    def __init__(self, text, x, y, parent, color, fontSize, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.text = text
        self.color = color
        self.fontSize = fontSize
        self.parent = parent
        self.x = x
        self.y = y
        font = pygame.font.Font(None, 48)
        self.image = font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.midright = (0, self.y)

    def Update(self):
        if self.rect.left < self.parent.rect.right:
            self.rect.move_ip(1, 0)
        else:
            self.kill()
            self.parent.dynamic = None


class Text(pygame.sprite.Sprite):
    def __init__(self, text, x, y, color, fontSize, group=None, align=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.text = text
        self.color = color
        self.fontSize = fontSize
        self.textFont = pygame.font.SysFont(fontName, self.fontSize)
        self.image = self.textFont.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        if align is TEXT_CENTER:
            self.rect.center = (self.x, self.y)

        elif align is TEXT_RIGHT:
            self.rect.midright = (self.x, self.y)

        else:
            self.rect.x = self.x
            self.rect.y = self.y


class Numbers(pygame.sprite.Sprite):
    def __init__(self, parent, attribute, x, y, color, fontSize, group=None, align=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.color = color
        self.parent = parent
        self.attribute = attribute
        self.text = str(getattr(self.parent, self.attribute))
        self.fontSize = fontSize
        self.align = align
        self.textFont = pygame.font.SysFont(fontName, self.fontSize)
        self.image = self.textFont.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # Default alignment = right
        if self.align is TEXT_CENTER:
            self.rect.center = (self.x, self.y)
        elif self.align is TEXT_LEFT:
            self.rect.midleft = (self.x, self.y)
        else:
            self.rect.midright = (self.x, self.y)

    def Update(self):
        self.text = str(getattr(self.parent, self.attribute))
        self.image = self.textFont.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        if self.align is TEXT_CENTER:
            self.rect.center = (self.x, self.y)
        elif self.align is TEXT_LEFT:
            self.rect.midleft = (self.x, self.y)
        else:
            self.rect.midright = (self.x, self.y)


class Tooltip(pygame.sprite.Sprite):
    def __init__(self, text, pos, evManager, group=None):
        self.evManager = evManager
        self.group = group
        pygame.sprite.Sprite.__init__(self, self.group)

        (x,y) = pos

        self.text = Text(text, x + 2, y + 2, WHITE, 23, self.group)

        self.image = pygame.Surface((self.text.rect.w + 4, self.text.rect.h + 4))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class MainWindow(pygame.sprite.Sprite):
    def __init__(self, color, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager

        self.group = group
        self.color = color
        self.image = pygame.Surface((800, 380))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.75)

        x = SCREEN_WIDTH / 1.25
        y = SCREEN_HEIGHT / 8

        self.closeButton = CloseButton(x, y, self.evManager, self.group)


class CloseButton(pygame.sprite.Sprite):
    def __init__(self, x, y, evManager, group=None, window=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.window = window
        self.x = x
        self.y = y

        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        ev = GUICloseWindowEvent(self.group)
        self.evManager.Post(ev)



class ArrowLeft(pygame.sprite.Sprite):
    def __init__(self, x, y, parent, attribute, group=None, multiply=None, override=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.image = pygame.Surface((20,20))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.parent = parent
        self.attribute = attribute
        self.multiply = multiply
        self.override = override

    def Clicked(self):
        value = getattr(self.parent, self.attribute)
        if self.multiply:
            value -= 1 * self.multiply
        else:
            value -= 1

        if value < 0 and not self.override:
            value = 0
        setattr(self.parent, self.attribute, value)
        self.parent.Update()

    def ShiftClicked(self):
        value = getattr(self.parent, self.attribute)
        if self.multiply:
            value -= 10 * self.multiply
        else:
            value -= 10

        if value < 0 and not self.override:
            value = 0
        setattr(self.parent, self.attribute, value)
        self.parent.Update()


    def CtrlClicked(self):
        value = getattr(self.parent, self.attribute)
        if self.multiply:
            value -= 100 * self.multiply
        else:
            value -= 100

        if value < 0 and not self.override:
            value = 0
        setattr(self.parent, self.attribute, value)
        self.parent.Update()



class ArrowRight(pygame.sprite.Sprite):
    def __init__(self, x, y, parent, attribute, group=None, multiply=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.image = pygame.Surface((20,20))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.parent = parent
        self.attribute = attribute
        self.multiply = multiply

    def Clicked(self):
        value = getattr(self.parent, self.attribute)
        if self.multiply:
            value += 1 * self.multiply
        else:
            value += 1
        setattr(self.parent, self.attribute, value)
        self.parent.Update()

    def ShiftClicked(self):
        value = getattr(self.parent, self.attribute)
        if self.multiply:
            value += 10 * self.multiply
        else:
            value += 10
        setattr(self.parent, self.attribute, value)
        self.parent.Update()

    def CtrlClicked(self):
        value = getattr(self.parent, self.attribute)
        if self.multiply:
            value += 100 * self.multiply
        else:
            value += 100
        setattr(self.parent, self.attribute, value)
        self.parent.Update()


class PrevPage(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, window, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.window = window

    def Clicked(self):
        if self.window.page > 1:
            self.window.page -= 1
            self.window.Update()


class NextPage(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, window, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.window = window

    def Clicked(self):
        if self.window.page < self.window.maxPage:
            self.window.page += 1
            self.window.Update()