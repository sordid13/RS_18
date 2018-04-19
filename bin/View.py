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
GREEN = (0, 230, 0)
BLUE = (0, 0, 255)
YELLOW = (250, 250, 0)

fontName = 'Comic Sans MS'
fontSize = 18

imgFolder = os.path.join("asset")


#When instantiated, it will have group value from FinanceWindow, where it instantiate.
class CloseButton(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 1.25, HEIGHT / 6.75)
        self.group = group

    def Clicked(self):
        self.group.empty() #The button will empty/remove all sprite in its group which is "windowGroup".



class StaffTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "StaffTab.png")).convert()  # 384 x 216
        self.rect = self.image.get_rect()
        self.rect.bottomright = (WIDTH * 26.5 // 100, HEIGHT)

    def Clicked(self):
        pass

class MenuTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "MenuTab.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH * 45 // 100, HEIGHT)

    def Clicked(self):
        pass

class InventoryTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "InventoryTab.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (WIDTH * 63.5 // 100, HEIGHT)

    def Clicked(self):
        pass


class FinanceTab(pygame.sprite.Sprite):
    def __init__(self, group=None, windowGroup=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "FinanceTab1.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH * 10// 100, 0)

        self.text = "-1234567890"
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.textSurface = self.font.render(self.text, False, (0, 0, 0))

        self.image.blit(self.textSurface, (80, 15))

        #This attribute is needed to pass the value to windowGroup
        self.windowGroup = windowGroup

    def Clicked(self):
        self.windowGroup.empty()
        FinanceWindow(self.windowGroup) #The value passed here, the FinanceWindow will instantiate under windowGroup.

#When instantiated, it will have group value from FinanceTab, where it instantiate.
class FinanceWindow(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((800, 400))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2.5)

        #The CloseButton is instantiate under FinanceWindow's group, which is "windowGroup".
        CloseButton(group)

    def Clicked(self):
        pass


class CustomersTab(pygame.sprite.Sprite):
    def __init__(self, group=None, windowGroup = None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "CustomerTab.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.midtop = (WIDTH * 40 // 100, 0)

        self.text = "50"
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.textSurface = self.font.render(self.text, False, (0, 0, 0))

        self.image.blit(self.textSurface, (90, 18))

        self.windowGroup = windowGroup

    def Clicked(self):
        self.windowGroup.empty()
        CustomersWindow(self.windowGroup)


class CustomersWindow(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((800, 400))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2.5)

        CloseButton(group)

    def Clicked(self):
        pass


class SatisfactionTab(pygame.sprite.Sprite):
    def __init__(self, group=None, windowGroup = None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load(os.path.join(imgFolder, "SatisfactionTab.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.topright = (WIDTH * 70 // 100, 0)
        self.image.set_colorkey(WHITE)

        self.text = "Happy"
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.textSurface = self.font.render(self.text, False, (0, 0, 0))

        self.image.blit(self.textSurface, (110, 15))

        self.windowGroup = windowGroup

    def Clicked(self):
        SatisfactionWindow(self.windowGroup)


class SatisfactionWindow(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((800, 400))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2.5)

        CloseButton(group)

    def Clicked(self):
        pass


class DateTime(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((WIDTH * 20 // 100, HEIGHT * 10 // 100))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topright = (WIDTH * 95 // 100, 0)

    def Clicked(self):
        pass


class View:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Restaurant Simulator")

        #Sprite Layers and Groups
        self.mainUI = pygame.sprite.LayeredUpdates()
        self.clickUI = pygame.sprite.Group()
        self.windows = pygame.sprite.Group()

        #All sprite start from here.
        #Sprite will carry it group from here.
        self.staffTab = StaffTab(self.mainUI)
        self.menuTab = MenuTab(self.mainUI)
        self.inventoryTab = InventoryTab(self.mainUI)
        self.financeTab = FinanceTab(self.clickUI, self.windows)
        self.customersTab = CustomersTab(self.clickUI, self.windows)
        self.satisfactionTab = SatisfactionTab(self.clickUI, self.windows)
        self.datetime = DateTime(self.mainUI)




    def Notify(self, event):
        if isinstance(event, TickEvent):
            self.mainUI.update()
            self.windows.update()

            self.screen.fill(WHITE)
            self.mainUI.draw(self.screen)
            self.clickUI.draw(self.screen)
            self.windows.draw(self.screen)

            pygame.display.flip()

        elif isinstance(event, LeftClickEvent):
            for sprite in self.clickUI:
                if sprite.rect.collidepoint(event.pos):
                    sprite.Clicked()
            for sprite in self.windows:
                if sprite.rect.collidepoint(event.pos):
                    sprite.Clicked()

