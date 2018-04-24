import pygame
from pygame.locals import *
from bin import *
import os
import math
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
PURPLE = (128, 0, 128)

cuisineType = ["Western", "Chinese", "Japanese", "Korean", "Indian"]



fontName = 'Comic Sans MS'
fontSize = 18

imgFolder = os.path.join("asset")

class Text(pygame.sprite.Sprite):
    def __init__(self, text, x, y, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.text = text
        self.textFont = pygame.font.SysFont(fontName, 14)
        self.image = self.textFont.render(self.text, True, WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y


class Numbers(pygame.sprite.Sprite):
    def __init__(self, parent, attribute, x, y, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.parent = parent
        self.attribute = attribute
        self.text = str(getattr(self.parent, self.attribute))
        self.textFont = pygame.font.SysFont(fontName, 16)
        self.image = self.textFont.render(self.text, True, WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.midright = (self.x, self.y)

    def Update(self):
        self.text = str(getattr(self.parent, self.attribute))
        self.image = self.textFont.render(self.text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.midright = (self.x, self.y)


class MainWindow(pygame.sprite.Sprite):
    def __init__(self, group, color):
        pygame.sprite.Sprite.__init__(self, group)

        self.color = color
        self.image = pygame.Surface((800, 380))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2.75)

        CloseButton(group)

    def Clicked(self):
        pass

class OpenWindowButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color, group=None, windowGroup=None, windowName=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.windowGroup = windowGroup
        self.windowName = windowName

    def Clicked(self):
        self.windowGroup.empty()
        self.windowName(self.windowGroup)

#When instantiated, it will have group value from FinanceWindow, where it instantiate.
class CloseButton(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 1.25, HEIGHT / 8)
        self.group = group

    def Clicked(self):
        self.group.empty() #The button will empty/remove all sprite in its group which is "windowGroup".

class FinanceTab(pygame.sprite.Sprite):
    def __init__(self, group=None, windowGroup=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((230,50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 17 / 100, HEIGHT * 4/100)

        self.windowGroup = windowGroup

    def Clicked(self):
        self.windowGroup.empty()
        FinanceWindow(self.windowGroup)  # The value passed here, the FinanceWindow will instantiate under windowGroup.

# When instantiated, it will have group value from FinanceTab, where it instantiate.
class FinanceWindow():
    def __init__(self, group=None):
        self.window = MainWindow(group, GREEN)


class CustomersTab(pygame.sprite.Sprite):
    def __init__(self, group=None, windowGroup=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((230, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 35 / 100, HEIGHT * 4 / 100)

        self.windowGroup = windowGroup

    def Clicked(self):
        self.windowGroup.empty()
        CustomersWindow(self.windowGroup)

class CustomersWindow():
    def __init__(self, group=None):
        self.window = MainWindow(group, BLUE)

class SatisfactionTab(pygame.sprite.Sprite):
    def __init__(self, group=None, windowGroup=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((230, 50))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 53 / 100, HEIGHT * 4 / 100)

        self.windowGroup = windowGroup

    def Clicked(self):
        self.windowGroup.empty()
        SatisfactionWindow(self.windowGroup)

class SatisfactionWindow():
    def __init__(self, group=None):
        self.window = MainWindow(group, YELLOW)

class DateTime(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((230, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 90 / 100, HEIGHT * 4 / 100)

    def Clicked(self):
        pass


class StaffTab(pygame.sprite.Sprite):
    def __init__(self, group=None, windowGroup=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((270,50))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 50/100, HEIGHT * 67/100)

        self.windowName = StaffWindow
        self.windowGroup = windowGroup
        #self.clickUI = clickUI
        #self.button = OpenWindowButton(WIDTH * 50/100, HEIGHT * 62.5/100, self.clickUI, self.windowGroup, self.windowName)

    def Clicked(self):
        StaffWindow(self.windowGroup)

class StaffWindow():
    def __init__(self, group=None):
        self.window = MainWindow(group, BLUE)

class MenuTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((500, 200))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 27 / 100, HEIGHT * 85/100)

    def Clicked(self):
        pass


class InventoryTab(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((500, 200))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 73/100, HEIGHT * 85/100)

    def Clicked(self):
        pass

class MidTab(pygame.sprite.Sprite):
    def __init__(self, group=None, clickUI=None, windowGroup=None, windowsGUI=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((70, 200))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 50/100, HEIGHT * 85/100)

        self.clickUI = clickUI
        self.windowGroup = windowGroup
        self.windowsGUI = windowsGUI

        self.addDishButton = AddDishButton(self.clickUI, self.windowGroup)
        self.marketButton = MarketButton(self.clickUI, self.windowGroup)

class AddDishButton():
    def __init__(self, group=None, windowGroup=None):
        self.x = WIDTH * 50/100
        self.y = HEIGHT * 80/100
        self.windowName = AddDishWindow
        self.windowGroup = windowGroup
        self.button = OpenWindowButton(self.x, self.y, 40, 40, BLUE, group, self.windowGroup, self.windowName)



class MarketButton():
    def __init__(self, group=None, windowGroup=None):
        self.x = WIDTH * 50/100
        self.y = HEIGHT * 90/100
        self.windowName = MarketWindow
        self.windowGroup = windowGroup
        self.button = OpenWindowButton(self.x, self.y, 40, 40, GREEN, group, self.windowGroup, self.windowName)


class AddDishWindow():
    def __init__(self, group=None):
        self.group = group
        self.window = MainWindow(group, BLUE)
        self.tab = range(5)

        self.cuisine = "Western"
        self.page = 0
        self.maxPage = math.ceil(len(DISHES_LIST) / 12) - 1

        ArrowUp(WIDTH * 78 / 100, HEIGHT * 30 / 100, self, group)
        ArrowDown(WIDTH * 78 / 100, HEIGHT * 38 / 100, self, group)

        self.dishScreen = DishScreen(self.page, self.cuisine, self, group)

        x = WIDTH * 25 / 100
        y = HEIGHT * 17 / 100
        c = 0

        for cuisine in cuisineType:
            self.cuisine = cuisineType[c]
            CuisineTab(x, y, self.cuisine, self, group)
            y += 50
            c += 1

    def Update(self):
        self.dishScreen.kill()
        for container in self.dishScreen.dishContainers:
            self.group.remove(contents for contents in container.contents)
            container.kill()

        self.dishScreen.dishContainers = []
        self.dishScreen = None
        self.dishScreen = DishScreen(self.page, self.cuisine, self, self.group)




class CuisineTab(pygame.sprite.Sprite):
    def __init__(self, x, y, cuisine, window, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.cuisine = cuisine
        self.window = window
        self.group = group
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join(imgFolder, cuisine + "Cuisine.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        self.window.cuisine = self.cuisine
        self.window.Update()




class DishScreen(pygame.sprite.Sprite):
    def __init__(self, page, cuisine, window, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.image = pygame.Surface((570, 350))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 53 / 100, HEIGHT * 36 / 100)

        self.cuisine = cuisine
        self.dishContainers = []

        self.window = window
        self.page = page

        x = WIDTH * 42 / 100
        y = HEIGHT * 17 / 100
        baseIndex = self.page * 12
        for i in range(12):
            try:
                dish = DISHES_LIST[i + baseIndex]
                if self.cuisine == dish.cuisine:
                    self.dishContainers.append(DishContainer(x, y, dish, self.cuisine, self.window, group))
                    y += 55
                    if i == 5:
                        x += 280
                        y = HEIGHT * 17 / 100

            except IndexError:
                break



class DishContainer(pygame.sprite.Sprite):
    def __init__(self, x, y, dish, cuisine, window, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.image = pygame.Surface((265, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.cuisine = cuisine
        self.dish = dish
        self.window = window
        self.contents = []

        self.contents.append(Text(self.dish.name, self.x - 75, self.y - 20, group))
        self.contents.append(DishSprite(self.x - 100, self.y, dish, group))


class DishSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, dish, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.dish = dish
        self.x = x
        self.y = y
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLACK)
        #self.image = pygame.image.load(os.path.join(imgFolder, self.ingredient.name + ".png")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        return


class MarketWindow():
    def __init__(self, group=None):
        self.group = group
        self.window = MainWindow(group, GREEN)
        self.tab = range(6)

        x = WIDTH * 25/100
        y = HEIGHT * 15/100
        qualityNumber = 0

        self.page = 0
        self.quality = 0
        self.maxPage = math.ceil(len(INGREDIENTS_LIST) / 10) - 1

    #Instantiate Sprite in the window.
        self.ingredientScreen = IngredientScreen(self.page, self, group)
        ArrowUp(WIDTH * 75/100, HEIGHT * 30/100, self, group)
        ArrowDown(WIDTH * 75/100, HEIGHT * 38/100, self, group)
        MarketCart(group)

        for tab in self.tab:
            imageName = str(qualityNumber) + "quality.png"
            image = pygame.image.load(os.path.join(imgFolder, imageName)).convert()
            QualityTab(x, y, image, qualityNumber, self, group)
            x += 110
            qualityNumber += 1

    def UpdateQuality(self):
        for container in self.ingredientScreen.ingredientContainers:
            container.Update()

    def Update(self):
        self.ingredientScreen.kill()
        for container in self.ingredientScreen.ingredientContainers:
            self.group.remove(contents for contents in container.contents)
            container.kill()

        self.ingredientScreen.ingredientContainers = []
        self.ingredientScreen = None
        self.ingredientScreen = IngredientScreen(self.page, self, self.group)


class QualityTab(pygame.sprite.Sprite):
    def __init__(self, x, y, image, quality, window, group=None):
        pygame.sprite.Sprite. __init__(self, group)
        self.parent = window
        self.group = group
        self.x = x
        self.y = y
        self.image = image
        self.quality = quality
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        self.parent.quality = self.quality
        self.parent.UpdateQuality()


class IngredientScreen(pygame.sprite.Sprite):
    def __init__(self, page, window, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.imageName = "Container.png"
        self.image = pygame.image.load(os.path.join(imgFolder, self.imageName)).convert()
        self.group = group
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 46.5 / 100, HEIGHT * 38 / 100)
        self.ingredientContainers = []

        self.window = window
        self.page = page

        x = WIDTH * 34 / 100
        y = HEIGHT * 22.5 / 100
        baseIndex = self.page * 10
        for i in range(10):
            try:
                ingredient = INGREDIENTS_LIST[i + baseIndex]
                self.ingredientContainers.append(IngredientContainer(x, y, ingredient, self.window, group))
                y += 55
                if i == 4:
                    x += 315
                    y = HEIGHT * 22.5 / 100
            except IndexError:
                break

    def Clicked(self):
        return


class IngredientContainer(pygame.sprite.Sprite):
    def __init__(self, x, y, ingredient, window, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.ingredient = ingredient
        self.x = x
        self.y = y
        self.image = pygame.Surface((300, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.window = window
        self.contents = []
        self.quantity = 0
        self.quality = self.window.quality
        self.ingredientQuantity = Numbers(self, "quantity", self.x + 120, self.y - 13, group)
        self.ingredientQuality = Numbers(self, "quality", self.x - 85, self.y + 5 , group)

        self.contents.append(Text(self.ingredient.name, self.x - 100, self.y - 20, group))
        self.contents.append(IngredientSprite(self.x - 120, self.y, ingredient, group))

        self.contents.append(self.ingredientQuantity)
        self.contents.append(self.ingredientQuality)
        self.contents.append(ArrowLeft(self.x + 85, self.y - 10,  self, group))
        self.contents.append(ArrowRight(self.x + 135, self.y - 10,  self, group))
        self.contents.append(AddToCart(self.x + 110, self.y + 10, self, group))

    def Update(self):
        self.quality = self.window.quality

        if self.quantity < 0:
            self.quantity = 0

        self.quantityDisplay = str(self.quantity)
        self.ingredientQuantity.Update()

        self.qualityDisplay = str(self.quality)
        self.ingredientQuality.Update()

    def Clicked(self):
        return

class IngredientSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, ingredient, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.ingredient = ingredient
        self.x = x
        self.y = y
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLACK)
        #self.image = pygame.image.load(os.path.join(imgFolder, self.ingredient.name + ".png")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        return



class AddToCart(pygame.sprite.Sprite):
    def __init__(self, x, y, container, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.container = container
        self.group = group
        self.image = pygame.Surface((65,17))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class MarketCart(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((170, 300))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 87/100, HEIGHT * 38/100)



class ArrowLeft(pygame.sprite.Sprite):
    def __init__(self, x, y, container, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.image = pygame.Surface((20,20))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.container = container

    def Clicked(self):
        if self.container.quantity > 0 and self.container.quantity != 0:
            self.container.quantity -= 1
            self.container.Update()

    def ShiftClicked(self):
        if self.container.quantity > 0 and self.container.quantity != 0:
            self.container.quantity -= 10
            self.container.Update()

    def CtrlClicked(self):
        if self.container.quantity > 0 and self.container.quantity != 0:
            self.container.quantity -= 100
            self.container.Update()

class ArrowRight(pygame.sprite.Sprite):
    def __init__(self, x, y, container, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.image = pygame.Surface((20,20))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.container = container

    def Clicked(self):
        if self.container.quantity >= 0:
            self.container.quantity += 1
            self.container.Update()

    def ShiftClicked(self):
        self.container.quantity += 10
        self.container.Update()

    def CtrlClicked(self):
        self.container.quantity += 100
        self.container.Update()



class ArrowUp(pygame.sprite.Sprite):
    def __init__(self, x, y, window, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.image = pygame.Surface((50,50))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.window = window

    def Clicked(self):
        if self.window.page > 0:
            self.window.page -= 1
            self.window.Update()

class ArrowDown(pygame.sprite.Sprite):
    def __init__(self, x, y, window, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.image = pygame.Surface((50,50))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.window = window

    def Clicked(self):
        if self.window.page < self.window.maxPage:
            self.window.page += 1
            self.window.Update()





class View:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(WHITE)
        self.screen.blit(self.background, (0, 0))
        pygame.display.set_caption("Restaurant Simulator")
        pygame.display.flip()


        #Sprite Layers and Groups
        self.mainUI = pygame.sprite.RenderUpdates()
        self.clickUI = pygame.sprite.RenderUpdates()
        self.windows = pygame.sprite.RenderUpdates()

        #All sprite start from here.
        #Sprite will carry it group from here.
        self.staffTab = StaffTab(self.clickUI, self.windows)
        self.menuTab = MenuTab(self.mainUI)
        self.inventoryTab = InventoryTab(self.mainUI)
        self.midTab = MidTab(self.mainUI, self.clickUI, self.windows)
        self.financeTab = FinanceTab(self.clickUI, self.windows)
        self.customersTab = CustomersTab(self.clickUI, self.windows)
        self.satisfactionTab = SatisfactionTab(self.clickUI, self.windows)
        self.datetime = DateTime(self.mainUI)


    def Notify(self, event):
        if isinstance(event, TickEvent):

            self.mainUI.clear(self.screen, self.background)
            self.windows.clear(self.screen, self.background)
            self.clickUI.clear(self.screen, self.background)


            self.mainUI.update()
            self.windows.update()
            self.clickUI.update()

            dirtyRects = self.mainUI.draw(self.screen)
            dirtyRects += self.windows.draw(self.screen)
            dirtyRects += self.clickUI.draw(self.screen)

            pygame.display.update(dirtyRects)

        elif isinstance(event, LeftClickEvent):
            for sprite in self.clickUI:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.Clicked()
                    except AttributeError:
                        continue
            for sprite in self.windows:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.Clicked()
                    except AttributeError:
                        continue

        elif isinstance(event, ShiftLeftClickEvent):
            for sprite in self.clickUI:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.ShiftClicked()
                    except AttributeError:
                        sprite.Clicked()
            for sprite in self.windows:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.ShiftClicked()
                    except AttributeError:
                        sprite.Clicked()

        elif isinstance(event, CtrlLeftClickEvent):
            for sprite in self.clickUI:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.CtrlClicked()
                    except AttributeError:
                        sprite.Clicked()
            for sprite in self.windows:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.CtrlClicked()
                    except AttributeError:
                        sprite.Clicked()






