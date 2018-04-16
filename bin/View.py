import pygame
from pygame.locals import *
import os
from .Events import *

WIDTH = 1280
HEIGHT = 720
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

fontName = 'Comic Sans MS'
fontSize = 18

imgFolder = os.path.join("asset")


class StaffTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "StaffTab.png")).convert()  # 384 x 216
        self.rect = self.image.get_rect()
        self.rect.bottomright = (WIDTH * 26.5 // 100, HEIGHT)

    def update(self):
        pass


class MenuTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "MenuTab.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH * 45 // 100, HEIGHT)

    def update(self):
        pass


class InventoryTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "InventoryTab.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (WIDTH * 63.5 // 100, HEIGHT)

    def update(self):
        pass


class FinanceTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "FinanceTab1.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH * 10 // 100, 0)

        self.text = "-1234567890"
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.textSurface = self.font.render(self.text, False, (0, 0, 0))

        self.image.blit(self.textSurface, (80, 15))

    def update(self):
        pass


class CustomersTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "CustomerTab.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.midtop = (WIDTH * 40 // 100, 0)

        self.text = "50"
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.textSurface = self.font.render(self.text, False, (0, 0, 0))

        self.image.blit(self.textSurface, (90, 18))

    def update(self):
        pass


class SatisfactionTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "SatisfactionTab.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.topright = (WIDTH * 70 // 100, 0)

        self.text = "Happy"
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.textSurface = self.font.render(self.text, False, (0, 0, 0))

        self.image.blit(self.textSurface, (110, 15))


class DateTime(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((WIDTH * 20 // 100, HEIGHT * 10 // 100))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topright = (WIDTH * 95 // 100, 0)


class View:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Restaurant Simulator")
        self.clock = pygame.time.Clock()

        self.allSprites = pygame.sprite.LayeredUpdates()

        self.staffTab = StaffTab(self.allSprites)
        self.menuTab = MenuTab(self.allSprites)
        self.inventoryTab = InventoryTab(self.allSprites)
        self.financeTab = FinanceTab(self.allSprites)
        self.customersTab = CustomersTab(self.allSprites)
        self.satisfactionTab = SatisfactionTab(self.allSprites)
        self.datetime = DateTime(self.allSprites)

    def Notify(self, event):
        if isinstance(event, TickEvent):
            self.allSprites.update()

            self.screen.fill(BLACK)
            self.allSprites.draw(self.screen)

            pygame.display.flip()
