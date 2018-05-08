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

fontName = ''

imgFolder = os.path.join("asset")

# --------------------------------------------------------------------------------------------------------------


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

        if align is CENTER:
            self.rect.center = (self.x, self.y)
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
        if self.align is CENTER:
            self.rect.center = (self.x, self.y)
        elif self.align is LEFT:
            self.rect.midleft = (self.x, self.y)
        else:
            self.rect.midright = (self.x, self.y)

    def Update(self):
        self.text = str(getattr(self.parent, self.attribute))
        self.image = self.textFont.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        if self.align is CENTER:
            self.rect.center = (self.x, self.y)
        elif self.align is LEFT:
            self.rect.midleft = (self.x, self.y)
        else:
            self.rect.midright = (self.x, self.y)


class MainWindow(pygame.sprite.Sprite):
    def __init__(self, color, group=None):
        pygame.sprite.Sprite.__init__(self, group)

        self.group = group
        self.color = color
        self.image = pygame.Surface((800, 380))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2.75)

        x = WIDTH / 1.25
        y = HEIGHT / 8

        self.closeButton = CloseButton(x, y, group)

    def Clicked(self):
        pass


class OpenWindowButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color, evManager, group=None, windowGroup=None, windowName=None, popUp=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.windowGroup = windowGroup
        self.windowName = windowName
        self.popUp = popUp

    def Clicked(self):
        self.windowGroup.empty()
        self.windowName(self.evManager, self.popUp, self.windowGroup)


class CloseButton(pygame.sprite.Sprite):
    def __init__(self, x, y, group=None, window=None):
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
        self.group.empty()
        try:
            self.window.RemoveContents()
        except AttributeError:
            pass


class ArrowLeft(pygame.sprite.Sprite):
    def __init__(self, x, y, parent, attribute, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.image = pygame.Surface((20,20))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.parent = parent
        self.attribute = attribute

    def Clicked(self):
        value = getattr(self.parent, self.attribute)
        if value > 0 and value != 0:
            value -= 1
            setattr(self.parent, self.attribute, value)
            self.parent.Update()

    def ShiftClicked(self):
        value = getattr(self.parent, self.attribute)
        if value > 0 and value != 0:
            value -= 10
            setattr(self.parent, self.attribute, value)
            self.parent.Update()

    def CtrlClicked(self):
        value = getattr(self.parent, self.attribute)
        if value > 0 and value != 0:
            value -= 100
            setattr(self.parent, self.attribute, value)
            self.parent.Update()


class ArrowRight(pygame.sprite.Sprite):
    def __init__(self, x, y, parent, attribute, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.image = pygame.Surface((20,20))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.parent = parent
        self.attribute = attribute

    def Clicked(self):
        value = getattr(self.parent, self.attribute)
        value += 1
        setattr(self.parent, self.attribute, value)
        self.parent.Update()

    def ShiftClicked(self):
        value = getattr(self.parent, self.attribute)
        value += 10
        setattr(self.parent, self.attribute, value)
        self.parent.Update()

    def CtrlClicked(self):
        value = getattr(self.parent, self.attribute)
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

# --------------------------------------------------------------------------------------------------------------


class DateTime(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.image = pygame.Surface((230, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 90 / 100, HEIGHT * 4 / 100)

        self.date = str(Date.day) + " / " + str(Date.month) + " / " + str(Date.year)
        self.display = Numbers(self, "date", self.rect.right - 10, self.rect.centery, WHITE, 24, self.group)

    def Clicked(self):
        pass

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.date = str(Date.day) + " / " + str(Date.month) + " / " + str(Date.year)
            self.display.Update()

# FINANCE----------------------------------------------------------------------------------------------


class FinanceTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None, windowGroup=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((230,50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 17 / 100, HEIGHT * 4/100)

        self.windowGroup = windowGroup

    def Clicked(self):
        self.windowGroup.empty()
        FinanceWindow(self.evManager, self.windowGroup)  # The value passed here, the FinanceWindow will instantiate under windowGroup.


class FinanceWindow:
    def __init__(self, evManager, group=None):
        self.evManager = evManager
        self.group = group
        self.window = MainWindow(GREEN, self.group)
        self.screen = None

        x = WIDTH/2
        y = HEIGHT/2
        #Button
        self.dayButton = FinanceButton(x - 300, y - 260, 140, 30, self, "Day", YELLOW, self.evManager, self.group)
        self.weekButton = FinanceButton(x - 150, y - 260, 140, 30, self, "Week", PURPLE, self.evManager, self.group)
        self.monthButton = FinanceButton(x , y - 260, 140, 30, self, "Month", BLUE, self.evManager, self.group)
        self.yearButton = FinanceButton(x + 150, y - 260, 140, 30, self, "Year", RED, self.evManager, self.group)
        self.statementButton = FinanceButton(x + 250, y - 260, 30, 40, self, "Statement", BLACK, self.evManager, self.group)
        self.graphButton = FinanceButton(x + 285, y - 260, 30, 40, self, "Graph", BLACK, self.evManager, self.group)

        #Text
        Text("Income:", x - 350, y - 200, BLACK, 25, self.group)
        Text("Sales", x - 330, y - 180, BLACK, 25, self.group)
        Text("Expense:", x - 350, y - 155, BLACK, 25, self.group)
        Text("Inventory", x - 330, y - 130, BLACK, 25, self.group)
        Text("Marketing", x - 330, y - 100, BLACK, 25, self.group)
        Text("Renovation", x - 330, y - 70, BLACK, 25, self.group)
        Text("Salary", x - 330, y - 40, BLACK, 25, self.group)
        Text("Misc.", x - 330, y - 10, BLACK, 25, self.group)
        Text("Profit/Loss", x - 350, y + 20, BLACK, 25, self.group)

        self.firstScreen = StatementScreen(x - 120, y - 80, self, self.evManager, self.group)
        self.secondScreen = StatementScreen(x + 80, y - 80, self, self.evManager, self.group)
        self.thirdScreen = StatementScreen(x + 280, y - 80, self, self.evManager, self.group)



class StatementScreen(pygame.sprite.Sprite):
    def __init__(self, x, y, parent, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group
        self.parent = parent
        self.x = x
        self.y = y

        self.image = pygame.Surface((190, 270))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)



class FinanceButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, parent, name, color, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group
        self.parent = parent
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


# CUSTOMERS-------------------------------------------------------------------------------------------------


class CustomersTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None, windowGroup=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((230, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 35 / 100, HEIGHT * 4 / 100)

        self.windowGroup = windowGroup

    def Clicked(self):
        self.windowGroup.empty()
        CustomersWindow(self.evManager, self.windowGroup)


class CustomersWindow:
    def __init__(self, evManager, group=None):
        self.evManager = evManager
        self.group = group
        self.window = MainWindow(BLUE, self.group)
        self.previousTodayCustomer = PreviousTodayCustomer( WIDTH * 50/100, HEIGHT * 18/100, self.evManager, self.group)
        self.dishPercentage = DishPercentage(WIDTH * 50/100, HEIGHT * 43/100, self.evManager, self.group)

class PreviousTodayCustomer(pygame.sprite.Sprite):
    def __init__(self, x, y, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group
        self.x = x
        self.y = y
        self.image = pygame.Surface((600, 90))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,  self.y)

        self.contents = []
        self.contents.append(Text("No. Customers", self.x - 150, self.y - 30, BLACK, 20, self.group))
        self.contents.append(Text("Unserved Customer", self.x, self.y - 30, BLACK, 20, self.group))
        self.contents.append(Text("Satisfaction", self.x + 170, self.y - 30, BLACK, 20, self.group))
        self.contents.append(Text("Today", self.x - 270, self.y - 10, BLACK, 20, self.group))
        self.contents.append(Text("Previous Day", self.x - 270, self.y + 20, BLACK, 20, self.group))


class DishPercentage(pygame.sprite.Sprite):
    def __init__(self, x, y, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.evManager = evManager
        self.x = x
        self.y = y
        self.image = pygame.Surface((650, 250))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


# RIVAL--------------------------------------------------------------------------------------------------


class RivalTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None, windowGroup=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((230, 50))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 53 / 100, HEIGHT * 4 / 100)

        self.windowGroup = windowGroup

    def Clicked(self):
        self.windowGroup.empty()
        RivalWindow(self.evManager, self.windowGroup)


class RivalWindow:
    def __init__(self, evManager, group=None):
        self.evManager = evManager
        self.group = group
        self.window = MainWindow(YELLOW, self.group)

        x = WIDTH/2
        y = HEIGHT/2
        self.customersNumber = 100

        Text("Rival's Restaurant", x, y - 270, BLACK, 35, self.group, CENTER)
        Text("Today Customers:", x - 220, y - 240, BLACK, 25, self.group)
        self.customersDisplay = Numbers(self, "customersNumber", x + 20, y - 230, BLACK, 38, self.group)

        Text("MENU", x, y - 190,  BLACK, 35, self.group, CENTER)
        self.menuScreen = RivalMenuScreen(x, y, self.evManager, self.group)


class RivalMenuScreen(pygame.sprite.Sprite):
    def __init__(self, x, y, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group
        self.x = x
        self.y = y

        self.image = pygame.Surface((780, 250))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y - 50)


# STAFFs/WORKERs--------------------------------------------------------------------------------------------------


class StaffTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None, windowGroup=None, popUp=None):
        self.evManager = evManager

        self.name = "Staff Window"

        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((270,50))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 36/100, HEIGHT * 67/100)

        self.windowGroup = windowGroup
        self.popUp = popUp

    def Draw(self):
        self.windowGroup.empty()
        StaffWindow(self.evManager, self.windowGroup, self.popUp)

    def Clicked(self):
        ev = GUIRequestWindowEvent(self.name, self.Draw)
        self.evManager.Post(ev)


class StaffWindow(MainWindow):
    def __init__(self, evManager, group=None, popUp=None):
        super().__init__(YELLOW, group)

        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.popUp = popUp


        MyStaffsTab(self.evManager, self.group)
        HireStaffsTab(self.evManager, self.group)

        self.screen = None

        ev = GUIOpenMyStaffEvent()
        self.evManager.Post(ev)

    def RemoveContents(self):
        try:
            for content in self.screen.contents:
                content.kill()
            self.screen.kill()
        except AttributeError:
            pass

        try:
            for container in self.screen.container:
                for content in container.contents:
                    content.kill()
                container.kill()
            self.screen.RemoveContents()
            self.screen.kill()
        except AttributeError:
            pass

        try:
            for tab in self.screen.staffTab:
                tab.kill()
            self.screen.kill()
        except AttributeError:
            pass

    def Notify(self, event):
        if isinstance(event, GUIOpenHireStaffEvent):
            self.RemoveContents()
            self.screen = None
            self.screen = HireStaffScreen(self.evManager, self.group)

        elif isinstance(event, GUIOpenMyStaffEvent):
            self.RemoveContents()
            self.screen = None
            self.screen = MyStaffScreen(self.evManager, self.group, self.popUp)


class StaffSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, evManager, group=None, type=None, cuisine=None, level=None): #TODO: type, cuisine, and level: use to find sprite
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        if type == "Chef":
            self.color = WHITE
        elif type == "Waiter":
            self.color = BLACK
        else:
            self.color = GREEN

        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class MyStaffsTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group

        self.image = pygame.Surface((110, 35))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 45/100, HEIGHT * 15/100)


    def Clicked(self):
        ev = GUIOpenMyStaffEvent()
        self.evManager.Post(ev)


class HireStaffsTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group

        self.image = pygame.Surface((110, 35))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 55/100, HEIGHT * 15/100)

    def Clicked(self):
        ev = GUIOpenHireStaffEvent()
        self.evManager.Post(ev)


class MyStaffScreen(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None, popUp=None):
        pygame.sprite.Sprite.__init__(self, group)

        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.group = group
        self.x = WIDTH * 50/100
        self.y = HEIGHT * 40/100
        self.popUp = popUp

        self.image = pygame.Surface((780, 300))
        self.image.fill(BLUE)
        self.image.set_colorkey(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.contents = []
        self.container = []
        self.page = 1

        self.contents.append(Text("Restaurant's Staff", self.x, self.y - 130, BLACK, 30, self.group, CENTER))

        ev = StaffUpdateRequestEvent()
        self.evManager.Post(ev)

    def LoadStaff(self, chefs, waiters):
        x = self.x - 350
        y = self.y - 75
        i = 0

        for chef in chefs:
            self.container.append(MyChefContainer(x, y, chef, self.evManager, self.group, self.popUp))
            x += 65
            i += 1
            if i % 10 == 0:
                x = self.x - 350
                y += 75
        for waiter in waiters:
            self.container.append(MyWaiterContainer(x, y, waiter, self.evManager, self.group, self.popUp))
            x += 65
            i += 1
            if i % 10 == 0:
                x = self.x - 350
                y += 75

    def RemoveContents(self):
        for container in self.container:
            for contents in container.contents:
                contents.kill()
            container.kill()
        self.container = []
        for content in self.contents:
            content.kill()
        self.contents = []


    def Notify(self, event):
        if isinstance(event, StaffUpdateEvent):
            self.LoadStaff(event.chefs, event.waiters)


class HireStaffScreen(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)

        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.group = group

        self.image = pygame.Surface((780, 300))
        self.image.fill(PURPLE)
        self.image.set_colorkey(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 50/100, HEIGHT * 40/100)

        self.staffType = "Chef"
        self.cuisine = "Western"

        self.staffTab = []
        self.cuisineTabs = []
        self.container = []


        self.staffTab.append(ChefTab(self.evManager, self.group))
        self.staffTab.append(WaiterTab(self.evManager, self.group))

        if self.staffType == "Chef":
            self.LoadHireChefContents()
        elif self.staffType == "Waiter":
            self.LoadHireWaiterContents()


    def LoadHireChefContents(self):
        tab_x = WIDTH * 31.5 / 100
        tab_y = HEIGHT * 23 / 100
        container_x = WIDTH * 38 / 100
        container_y = HEIGHT * 25.5 / 100
        level = 3

        for cuisine in CUISINES_LIST:
            self.cuisineTabs.append(ChefCuisine(tab_x, tab_y, cuisine, self.evManager, self.group))
            tab_y += 50

        while level >= 0:
            self.container.append(HireChefContainer(container_x, container_y, 500, 60, self.cuisine, level,
                                                   self.evManager, self.group))
            level -= 1
            container_y += 70


    def LoadHireWaiterContents(self):
        x = WIDTH * 26.5/100
        y = HEIGHT * 30/100
        level = 3

        while level >= 0:
            self.container.append(HireWaiterContainer(x, y, 330, 130, level, self.evManager, self.group))
            x += 340
            level -= 1
            if level == 1:
                x = WIDTH * 26.5 / 100
                y += 145

    def RemoveContents(self):
        for container in self.container:
            for content in container.contents:
                content.kill()
            container.kill()
        for tab in self.cuisineTabs:
            tab.kill()
        self.cuisineTabs = []
        self.container = []


    def Notify(self, event):
        if isinstance(event, GUISelectStaffEvent):
            self.RemoveContents()
            self.staffType = event.staffType
            if self.staffType == "Chef":
                self.LoadHireChefContents()
            elif self.staffType == "Waiter":
                self.LoadHireWaiterContents()

        elif isinstance(event, GUISelectCuisineEvent):
            self.cuisine = event.cuisine
            self.RemoveContents()
            self.LoadHireChefContents()


class ChefTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group

        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 22/100, HEIGHT * 25/100)

    def Clicked(self):
        staffType = "Chef"
        ev = GUISelectStaffEvent(staffType)
        self.evManager.Post(ev)


class WaiterTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group

        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 22/100, HEIGHT * 32 / 100)

    def Clicked(self):
        staffType = "Waiter"
        ev = GUISelectStaffEvent(staffType)
        self.evManager.Post(ev)


class ChefCuisine(pygame.sprite.Sprite):
    def __init__(self, x, y, cuisine, evManager, group=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.cuisine = cuisine
        self.group = group
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join(imgFolder, cuisine + "Cuisine.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        ev = GUISelectCuisineEvent(self.cuisine)
        self.evManager.Post(ev)


class ChefDetail(pygame.sprite.Sprite):
    def __init__(self, chef, evManager, group=None):
        self.evManager = evManager
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group

        self.x = WIDTH * 9 / 100
        self.y = HEIGHT * 40 / 100
        self.w = 230
        self.h = 300
        self.chef = chef
        self.level = self.chef.level
        self.cuisine = self.chef.cuisine
        self.name = None
        self.wage = None

        if self.level == 3:
            self.name = "Chef de Cuisine"
            self.wage = 5000
        elif self.level == 2:
            self.name = "Sous Chef"
            self.wage = 3500
        elif self.level == 1:
            self.name = "Chef de Partie"
            self.wage = 2000
        elif self.level == 0:
            self.name = "Commis Chef"
            self.wage = 1000

        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.contents = []

        x = self.rect.right - 20
        y = self.rect.top + 20
        self.closeButton = CloseButton(x, y, self.group)

        self.contents.append(Text("CHEF", self.x, self.y - 130, BLACK, 35, self.group, CENTER))
        self.contents.append(StaffSprite(self.x, self.y - 80, 40, 40, self.evManager, self.group, "Chef"))
        self.contents.append(Text(self.name, self.x, self.y - 35, BLACK, 20, self.group, CENTER))
        self.contents.append(Text(self.cuisine, self.x, self.y - 20, BLACK, 20, self.group, CENTER))
        self.contents.append(Text("Wage/Day:", self.x - 100, self.y, BLACK, 20, self.group))
        self.contents.append(Text(str(self.wage), self.x - 20, self.y, BLACK, 20, self.group))
        self.contents.append(FireStaffButton(self.x, self.y + 100, self, self.evManager, self.group))


class WaiterDetail(pygame.sprite.Sprite):
    def __init__(self, waiter, evManager, group=None):
        self.evManager = evManager
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group

        self.x = WIDTH * 9 / 100
        self.y = HEIGHT * 40 / 100
        self.w = 230
        self.h = 300
        self.waiter = waiter
        self.level = self.waiter.level
        self.name = None
        self.wage = None

        if self.level == 3:
            self.name = "Highly-Trained"
            self.wage = 2500
        elif self.level == 2:
            self.name = "Well-Trained"
            self.wage = 2000
        elif self.level == 1:
            self.name = "Basic-Trained"
            self.wage = 1500
        elif self.level == 0:
            self.name = "Untrained"
            self.wage = 1000

        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.contents = []

        x = self.rect.right - 20
        y = self.rect.top + 20
        self.closeButton = CloseButton(x, y, self.group)

        self.contents.append(Text("WAITER", self.x, self.y - 130, BLACK, 35, self.group, CENTER))
        self.contents.append(StaffSprite(self.x, self.y - 80, 40, 40, self.evManager, self.group, "Waiter"))
        self.contents.append(Text(self.name, self.x, self.y - 35, BLACK, 20, self.group, CENTER))
        self.contents.append(Text("Wage/Day:", self.x - 100, self.y, BLACK, 20, self.group))
        self.contents.append(Text(str(self.wage), self.x - 20, self.y, BLACK, 20, self.group))
        self.contents.append(FireStaffButton(self.x, self.y + 100, self, self.evManager, self.group))


class FireStaffButton(pygame.sprite.Sprite):
    def __init__(self, x, y, staff, evManager, group=None):
        self.evManager = evManager
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.staff = staff
        self.x = x
        self.y = y

        self.image = pygame.Surface((150, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        Text("FIRE!!!", self.x, self.y, BLACK, 30, self.group, CENTER)

    def Clicked(self):
        pass



class MyChefContainer(pygame.sprite.Sprite):
    def __init__(self, x, y, chef, evManager, group=None, popUp=None):
        self.evManager = evManager
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.chef = chef
        self.level = chef.level
        self.cuisine = chef.cuisine
        self.popUp = popUp
        self.type = "Chef"

        self.image = pygame.Surface((55, 70))
        self.image.fill(RED)

        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.contents = []

        self.contents.append(StaffSprite(self.x, self.y - 8, 50, 50, self.evManager, self.group, "Chef"))
        self.contents.append(Text(str(self.chef.level), self.x, self.y + 30, BLACK, 20, self.group, CENTER))

    def Clicked(self):
        self.popUp.empty()
        ChefDetail(self, self.evManager, self.popUp)


class HireChefContainer(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, cuisine, level, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group
        self.staffType = "Chef"

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cuisine = cuisine
        self.level = level
        self.name = None
        self.wage = None
        self.cost = None

        if self.level == 3:
            self.name = "Chef de Cuisine"
            self.wage = 5000
            self.cost = 10000
        elif self.level == 2:
            self.name = "Sous Chef"
            self.wage = 3500
            self.cost = 7000
        elif self.level == 1:
            self.name = "Chef de Partie"
            self.wage = 2000
            self.cost = 4000
        elif self.level == 0:
            self.name = "Commis Chef"
            self.wage = 1000
            self.cost = 2000

        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.midleft = (self.x, self.y)
        self.contents = []

        self.contents.append(StaffSprite(self.x + 30, self.y, 40, 40, self.evManager, self.group))

        self.contents.append(Text(self.name, self.x + 60, self.y - 25, WHITE, 18, self.group))
        self.contents.append(Text(self.cuisine, self.x + 60, self.y, WHITE, 18, self.group))
        self.contents.append(Text("Wage/Day:", self.x + 200, self.y - 25, WHITE, 20, self.group))
        self.contents.append(Text(str(self.wage), self.x + 270, self.y - 23, WHITE, 20, self.group))
        self.contents.append(Text("Hire Cost:", self.x + 200, self.y, WHITE, 20, self.group))
        self.contents.append(Text(str(self.cost), self.x + 270, self.y, WHITE, 20, self.group))

        self.contents.append(HireButton(self.x + 450, self.y, 50, 20, self, self.evManager, self.group))


class MyWaiterContainer(pygame.sprite.Sprite):
    def __init__(self, x, y, waiter, evManager, group=None, popUp=None):
        self.evManager = evManager
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.waiter = waiter
        self.level = waiter.level
        self.popUp = popUp
        self.type = "Waiter"

        self.image = pygame.Surface((55, 70))
        self.image.fill(BLUE)

        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.contents = []

        self.sprite = StaffSprite(self.x, self.y - 8, 50, 50, self.evManager, self.group, "Waiter")
        self.contents.append(self.sprite)
        self.contents.append(Text(str(self.waiter.level), self.x, self.y + 30, BLACK, 20, self.group, CENTER))


    def Clicked(self):
        self.popUp.empty()
        WaiterDetail(self, self.evManager, self.popUp)


class HireWaiterContainer(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, level, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group
        self.staffType = "Waiter"

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.level = level
        self.name = None
        self.wage = None
        self.cost = None

        if self.level == 3:
            self.name = "Highly-Trained"
            self.wage = 2500
            self.cost = 5000
        elif self.level == 2:
            self.name = "Well-Trained"
            self.wage = 2000
            self.cost = 4000
        elif self.level == 1:
            self.name = "Basic-Trained"
            self.wage = 1500
            self.cost = 3000
        elif self.level == 0:
            self.name = "Untrained"
            self.wage = 1000
            self.cost = 2000

        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.midleft = (self.x, self.y)
        self.contents = []

        self.contents.append(StaffSprite(self.x + 30, self.y - 30, 40, 40, self.evManager, self.group))

        self.contents.append(Text(self.name, self.x + 60, self.y - 45, WHITE, 18, self.group))
        self.contents.append(Text("Wage/Day:", self.x + 60, self.y - 25, WHITE, 20, self.group))
        self.contents.append(Text(str(self.wage), self.x + 130, self.y - 23, WHITE, 20, self.group))
        self.contents.append(Text("Hire Cost:", self.x + 60, self.y, WHITE, 20, self.group))
        self.contents.append(Text(str(self.cost), self.x + 130, self.y, WHITE, 20, self.group))

        self.contents.append(HireButton(self.x + 290, self.y + 25, 50, 50, self, self.evManager, self.group))


class HireButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, container, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group
        self.container = container

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        print("Clicked")
        if self.container.staffType == "Chef":
            print(self.container.level)
            ev = HireChefEvent(self.container.level, self.container.cuisine)
            self.evManager.Post(ev)

        elif self.container.staffType == "Waiter":
            ev = HireWaiterEvent(self.container.level)
            self.evManager.Post(ev)



# RESTAURANT LEVEL & UPGRADE -----------------------------------------------------------------------------------------


class RestaurantTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None, popUp=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((270,50))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 64/100, HEIGHT * 67/100)

        self.popUp = popUp

    def Clicked(self):
        RestaurantDetail(self.evManager, self.popUp)


class RestaurantDetail(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.group = group

        self.image = pygame.Surface((230, 380))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 9 / 100, HEIGHT * 36.5 / 100)

        self.level = 1
        self.capacity = 100
        self.operatingCost = self.level * self.capacity

        Text("Level:", self.rect.left + 30, self.rect.top + 60, BLACK, 25, self.group)
        self.levelDisplay = Numbers(self, "level", self.rect.left + 50, self.rect.top + 90, BLACK, 25,
                                    self.group, CENTER)
        Text("Capacity:", self.rect.left + 120, self.rect.top + 60, BLACK, 25, self.group)
        self.capacityDisplay = Numbers(self, "capacity", self.rect.left + 160, self.rect.top + 90, BLACK, 25,
                                       self.group, CENTER)
        Text("Operating Cost:", WIDTH * 8.5/100, self.rect.top + 120, BLACK, 25, self.group, CENTER)
        self.operatingCostDisplay = Numbers(self, "operatingCost", WIDTH * 8.5/100, self.rect.top + 140, BLACK, 25,
                                            self.group, CENTER)

        Text("UPGRADE", WIDTH * 8.5/100, self.rect.top + 165, BLACK, 27, self.group, CENTER)

        self.upgradeDetail = UpgradeDetail(self, self.evManager, self.group)


        x = self.rect.right - 20
        y = self.rect.top + 20
        self.closeButton = CloseButton(x, y, self.group)

    def Remove(self):
        self.levelDisplay.kill()
        self.capacityDisplay.kill()
        self.operatingCostDisplay.kill()
        self.group.remove(contents for contents in self.upgradeDetail.contents)



    def Update(self):
        self.operatingCost = self.level * self.capacity
        self.levelDisplay = Numbers(self, "level", self.rect.left + 50, self.rect.top + 90, BLACK, 25,
                                    self.group, CENTER)
        self.capacityDisplay = Numbers(self, "capacity", self.rect.left + 160, self.rect.top + 90, BLACK, 25,
                                       self.group, CENTER)
        self.operatingCostDisplay = Numbers(self, "operatingCost", WIDTH * 8.5 / 100, self.rect.top + 140, BLACK,
                                            25, self.group, CENTER)
        self.upgradeDetail = UpgradeDetail(self, self.evManager, self.group)


    def Notify(self, event):
        if isinstance(event, UpgradeLevelEvent):
            self.Remove()
            self.level = event.level
            self.Update()


        elif isinstance(event, UpgradeCapacityEvent):
            self.Remove()
            self.capacity = event.capacity
            self.Update()


class UpgradeDetail(pygame.sprite.Sprite):
    def __init__(self, parent, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager
        self.group = group
        self.parent = parent

        self.image = pygame.Surface((200, 190))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 9 / 100, HEIGHT * 48 / 100)
        self.contents = []

        #UPGRADE LEVEL
        self.currentLevel = self.parent.level
        self.nextLevel = self.currentLevel + 1
        self.newLevelCost = self.nextLevel * self.parent.capacity
        self.costLevelDifference = self.newLevelCost - self.parent.operatingCost
        self.upLevelCost = 1000 * (self.nextLevel ** 2)

        self.contents.append(Text("Level:", self.rect.left + 40, self.rect.top + 10, BLACK, 23, self.group))
        self.contents.append(Numbers(self, "currentLevel", self.rect.left + 100, self.rect.top + 17, BLACK, 25,
                                     self.group))
        self.contents.append(Text("-->", self.rect.left + 120, self.rect.top + 17, BLACK, 25, self.group, CENTER)) #TODO: Replace with Arrow Sprite
        self.contents.append(Numbers(self, "nextLevel", self.rect.left + 145, self.rect.top + 17, BLACK, 25,
                                     self.group))
        self.contents.append(Text("+$" + str(self.costLevelDifference), self.rect.left + 50, self.rect.top + 45, BLACK,
                                  25, self.group, CENTER))
        self.contents.append(Text("$" + str(self.upLevelCost), self.rect.left + 130, self.rect.top + 45, BLACK, 25,
                                  self.group, CENTER))
        self.contents.append(UpgradeButton(WIDTH * 9/100, self.rect.top + 70, self, "level", self.evManager,
                                           self.group))

        #UPGRADE CAPACITY
        self.currentCapacity = self.parent.capacity
        self.nextCapacity = self.currentCapacity + 100
        self.newCapacityCost = self.parent.level * self.nextCapacity
        self.costCapacityDifference = self.newCapacityCost - self.parent.operatingCost
        self.upCapacityCost = 2 * self.nextCapacity

        self.contents.append(Text("Capacity:", self.rect.left + 10, self.rect.top + 100, BLACK, 23, self.group))

        self.contents.append(Numbers(self, "currentCapacity", self.rect.left + 120, self.rect.top + 108, BLACK, 23,
                                     self.group))

        self.contents.append(Text("-->", self.rect.left + 140, self.rect.top + 107, BLACK, 25, self.group, CENTER)) # TODO: Replace with Arrow Sprite

        self.contents.append(Numbers(self, "nextCapacity", self.rect.left + 190, self.rect.top + 108, BLACK, 23,
                                     self.group))

        self.contents.append(Text("+$" + str(self.costCapacityDifference), self.rect.left + 50, self.rect.top + 135,
                                  BLACK, 25,self.group, CENTER))
        self.contents.append(Text("$" + str(self.upCapacityCost), self.rect.left + 130, self.rect.top + 135, BLACK, 25,
                                  self.group, CENTER))
        self.contents.append(UpgradeButton(WIDTH * 9/100, self.rect.bottom - 25, self, "capacity", self.evManager,
                                           self.group))


class UpgradeButton(pygame.sprite.Sprite):
    def __init__(self, x, y, parent, type, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.evManager = evManager
        self.type = type
        self.x = x
        self.y = y
        self.parent = parent

        self.image = pygame.Surface((90, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        if self.type == "level":
            ev = UpgradeLevelEvent(self.parent.nextLevel, self.parent.upLevelCost)
            self.evManager.Post(ev)

        elif self.type == "capacity":
            ev = UpgradeCapacityEvent(self.parent.nextCapacity, self.parent.upCapacityCost)
            self.evManager.Post(ev)



# MAIN UI: Menu, Inventory ---------------------------------------------------------------------------------------------


class MenuTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None, popUp=None):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.group = group
        self.popUp = popUp

        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((500, 200))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 27 / 100, HEIGHT * 85/100)

        self.contents = []

    def UpdateDishes(self, dishes):
        x = self.rect.left + 33
        y = self.rect.top + 30
        i = 0
        for dish in dishes:
            self.contents.append(MenuDishContainer(x, y + 8, dish, self, self.evManager, self.group, self.popUp))
            x += 48

            i += 1
            if i >= 10:
                x = self.rect.left + 33
                y += 70
                i = 0


    def Notify(self, event):
        if isinstance(event, MenuUpdateEvent):
            for sprite in self.contents:
                try:
                    for s in sprite.contents:
                        s.kill()
                except AttributeError:
                    pass
                sprite.kill()
            self.contents = []
            self.UpdateDishes(event.dishes)


class MenuDishContainer(pygame.sprite.Sprite):
    def __init__(self, x, y, dish, window, evManager, group=None, popUp=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager

        self.x = x
        self.y = y
        self.dish = dish['dish']
        self.window = window
        self.group = group
        self.popUp = popUp
        self.price = dish['price']

        self.image = pygame.Surface((45, 60))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.contents = []

        self.contents.append(DishSprite(self.x, self.y - 7, self.dish, self.group))
        self.contents.append(Text("$" + " " + str(self.price), self.x, self.y + 23, BLACK, 20, self.group, CENTER))

    def Clicked(self):
        self.popUp.empty()
        DishDetail(self.dish, self.evManager, self.popUp)


class InventoryTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None, popUp=None):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((500, 200))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 73/100, HEIGHT * 85/100)

    def Notify(self, event):
        if isinstance(event, InventoryUpdateEvent):
            pass


# MAIN UI: Add Dish, Market, Marketing -------------------------------------------------------------------------------

class MidTab(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None, clickUI=None, popUp=None, windowGroup=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface((70, 200))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 50/100, HEIGHT * 85/100)

        self.clickUI = clickUI
        self.windowGroup = windowGroup
        self.popUp = popUp

        self.addDishButton = AddDishButton(self.evManager, self.clickUI, self.popUp, self.windowGroup)
        self.marketButton = MarketButton(self.evManager, self.clickUI, self.popUp, self.windowGroup)
        self.marketingButton = MarketingButton(self.evManager, self.clickUI, self.windowGroup)


class AddDishButton:
    def __init__(self, evManager, group=None, popUp=None, windowGroup=None):
        self.evManager = evManager

        self.x = WIDTH * 50/100
        self.y = HEIGHT * 78/100
        self.windowName = AddDishWindow
        self.windowGroup = windowGroup
        self.popUp = popUp

        self.button = OpenWindowButton(self.x, self.y, 40, 40, BLUE, self.evManager, group, self.windowGroup,
                                       self.windowName, self.popUp)


class MarketButton:
    def __init__(self, evManager, group=None, popUp=None, windowGroup=None):
        self.evManager = evManager

        self.x = WIDTH * 50/100
        self.y = HEIGHT * 85.5/100
        self.windowName = MarketWindow
        self.windowGroup = windowGroup
        self.popUp = popUp
        self.button = OpenWindowButton(self.x, self.y, 40, 40, GREEN, self.evManager, group, self.windowGroup,
                                       self.windowName, self.popUp)


class MarketingButton:
    def __init__(self, evManager, group=None, windowGroup=None):
        self.evManager = evManager

        self.x = WIDTH * 50 / 100
        self.y = HEIGHT * 93 / 100
        self.windowName = MarketingWindow
        self.windowGroup = windowGroup
        self.button = OpenWindowButton(self.x, self.y, 40, 40, PURPLE, self.evManager, group, self.windowGroup,
                                       self.windowName)

# MARKETING ------------------------------------------------------------------------------------------------


class MarketingWindow:
    def __init__(self, evManager, popUp=None, group=None):
        self.evManager = evManager

        self.group = group
        self.window = MainWindow(PURPLE, self.group)
        self.popUp = popUp

# MENU CATALOGUE & ADD DISH TO PLAYER's MENUS ----------------------------------------------------------------


class AddDishWindow:
    def __init__(self, evManager, popUp=None, group=None):
        self.evManager = evManager

        self.group = group
        self.window = MainWindow(BLUE, self.group)
        self.popUp = popUp
        self.tab = range(5)

        self.cuisine = "Western"
        self.page = 1
        self.maxPage = math.ceil(len(WESTERN_DISHES) / 12)

        PrevPage(WIDTH * 78 / 100, HEIGHT * 30 / 100, 50, 50, self, group)
        self.pageDisplay = Numbers(self, "page", WIDTH * 77/100, HEIGHT * 38/100, WHITE, 24, self.group)
        Text("/", WIDTH * 78/100, HEIGHT * 38/100, WHITE, 32, self.group, CENTER)
        self.maxPageDisplay = Numbers(self, "maxPage", WIDTH * 79/100, HEIGHT * 38 / 100, WHITE, 24, self.group, LEFT)
        NextPage(WIDTH * 78 / 100, HEIGHT * 46 / 100, 50, 50, self, group)

        self.dishScreen = DishScreen(self.page, self.cuisine, self, self.evManager, self.popUp, group)

        x = WIDTH * 25 / 100
        y = HEIGHT * 17 / 100

        for cuisine in CUISINES_LIST:
            CuisineTab(x, y, cuisine, self, self.evManager, group)
            y += 50

    def Update(self):
        self.pageDisplay.Update()

        self.dishScreen.kill()
        for container in self.dishScreen.dishContainers:
            self.group.remove(contents for contents in container.contents)
            container.kill()

        self.dishScreen.dishContainers = []
        self.dishScreen = None
        self.dishScreen = DishScreen(self.page, self.cuisine, self, self.evManager, self.popUp, self.group)


class CuisineTab(pygame.sprite.Sprite):
    def __init__(self, x, y, cuisine, window, evManager, group=None):
        self.evManager = evManager

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
        self.window.page = 1
        self.window.cuisine = self.cuisine
        self.window.Update()


class DishScreen(pygame.sprite.Sprite):
    def __init__(self, page, cuisine, window, evManager, popUp=None, group=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.popUp = popUp
        self.image = pygame.Surface((570, 350))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 53 / 100, HEIGHT * 36 / 100)

        self.cuisine = cuisine
        if self.cuisine == "Western":
            self.dishList = WESTERN_DISHES
        elif self.cuisine == "Chinese":
            self.dishList = CHINESE_DISHES
        elif self.cuisine == "Japanese":
            self.dishList = JAPANESE_DISHES
        elif self.cuisine == "Korean":
            self.dishList = KOREAN_DISHES
        elif self.cuisine == "Indian":
            self.dishList = INDIAN_DISHES

        self.dishContainers = []

        self.window = window
        self.page = page
        self.window.maxPage = math.ceil(len(self.dishList) / 12)
        self.window.maxPageDisplay.Update()

        x = WIDTH * 42 / 100
        y = HEIGHT * 17 / 100
        baseIndex = (self.page - 1) * 12
        for i in range(12):
            try:
                dish = self.dishList[i + baseIndex]
                if self.cuisine == dish.cuisine:
                    self.dishContainers.append(DishContainer(x, y, dish, self.cuisine, self.window, self.evManager,
                                                             self.popUp, group))
                    y += 55
                    if i == 5:
                        x += 280
                        y = HEIGHT * 17 / 100

            except IndexError:
                break


class DishSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, dish, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.dish = dish
        self.x = x
        self.y = y
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        #self.image = pygame.image.load(os.path.join(imgFolder, self.ingredient.name + ".png")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class DishContainer(pygame.sprite.Sprite):
    def __init__(self, x, y, dish, cuisine, window, evManager, popUp=None, group=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.popUp = popUp
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

        self.contents.append(Text(self.dish.name, self.x - 75, self.y - 20, WHITE, 14, self.group))
        self.contents.append(DishSprite(self.x - 100, self.y, dish, self.group))

    def Clicked(self):
        self.popUp.empty()
        DishDetail(self.dish, self.evManager, self.popUp)


class DishDetail(pygame.sprite.Sprite):
    def __init__(self, dish, evManager, group=None):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.dish = dish
        self.x = WIDTH * 9 / 100
        self.y = HEIGHT * 40 / 100
        self.w = 230
        self.h = 300

        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        x = self.rect.right - 20
        y = self.rect.top + 20
        self.closeButton = CloseButton(x, y, self.group)

        self.price = 0 # For price
        self.contents = []

        DishSprite(self.x, self.y - 90, self.dish, self.group)
        Text(self.dish.name, self.x, self.y - 50, BLACK, 18, self.group, CENTER)

        Text("Type:", self.rect.left + 10, self.y - 30, BLACK, 16, self.group)
        Text(self.dish.type, self.rect.left + 17, self.y - 10, BLACK, 14, self.group)

        Text("Cuisine:", self.rect.left + 10, self.y + 20, BLACK, 16, self.group)
        Text(self.dish.cuisine, self.rect.left + 17, self.y + 40, BLACK, 14, self.group)

        Text("Ingredients:", self.x - 10, self.y - 30, BLACK, 16, self.group)
        i = 10
        for ingredients in self.dish.ingredients:
            Text(ingredients.name, self.x - 3, self.y - i, BLACK, 14, self.group)
            i -= 17

        ArrowLeft(self.x - 30, self.y + 90, self, "price", self.group)
        ArrowRight(self.x + 30, self.y + 90, self, "price", self.group)
        self.priceDisplay = Numbers(self, "price", self.x, self.y + 90, BLACK, 16, self.group, CENTER)

        ev = GUICheckDishMenuEvent(self.dish, self)
        self.evManager.Post(ev)

    def Update(self):
        self.priceDisplay.Update()

    def Notify(self, event):
        if isinstance(event, GUICheckDishMenuResponseEvent):
            for sprite in self.contents:
                sprite.kill()

            self.contents = []

            if event.container is self:
                if event.dish:
                    self.price = event.dish['price']

                    self.contents.append(UpdateDishPrice(self.x - 50, self.y + 120, self.dish,
                                                         self, self.evManager, self.group))
                    self.contents.append(Text("Update Price", self.x - 50, self.y + 120, BLACK, 20, self.group, CENTER))

                    self.contents.append(RemoveDish(self.x + 50, self.y + 120, self.dish,
                                                    self, self.evManager, self.group))
                    self.contents.append(Text("Remove Dish", self.x + 50, self.y + 120, WHITE, 20, self.group, CENTER))

                else:
                    self.contents.append(AddToMenu(self.x, self.y + 120, self.dish, self, self.evManager, self.group))
                    self.contents.append(Text("Add To Menu ($1000)", self.x, self.y + 120, WHITE, 20,
                                              self.group, CENTER))
            self.Update()



class AddToMenu(pygame.sprite.Sprite):
    def __init__(self, x, y, dish, window, evManager, group=None):
        self.evManager = evManager
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.dish = dish
        self.window = window

        self.x = x
        self.y = y
        self.image = pygame.Surface((200, 30))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        ev = AddDishEvent(self.dish, self.window.price)
        self.evManager.Post(ev)

        ev = GUICheckDishMenuEvent(self.dish, self.window)
        self.evManager.Post(ev)


class UpdateDishPrice(pygame.sprite.Sprite):
    def __init__(self, x, y, dish, window, evManager, group=None):
        self.evManager = evManager
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.dish = dish
        self.window = window

        self.x = x
        self.y = y
        self.image = pygame.Surface((95, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        ev = UpdateDishPriceEvent(self.dish, self.window.price)
        self.evManager.Post(ev)

        ev = GUICheckDishMenuEvent(self.dish, self.window)
        self.evManager.Post(ev)

        print("hi")


class RemoveDish(pygame.sprite.Sprite):
    def __init__(self, x, y, dish, window, evManager, group=None):
        self.evManager = evManager
        pygame.sprite.Sprite.__init__(self, group)
        self.group = group
        self.dish = dish
        self.window = window

        self.x = x
        self.y = y
        self.image = pygame.Surface((95, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        ev = RemoveDishEvent(self.dish)
        self.evManager.Post(ev)

        ev = GUICheckDishMenuEvent(self.dish, self.window)
        self.evManager.Post(ev)

# MARKET: BUY INGREDIENT into INVENTORY -------------------------------------------------------------------------------


class MarketWindow:
    def __init__(self, evManager, popUp=None, group=None):
        self.evManager = evManager

        self.group = group
        self.popUp = popUp
        self.window = MainWindow(GREEN, self.group)
        self.tab = range(6)

        x = WIDTH * 25/100
        y = HEIGHT * 15/100
        qualityNumber = 0

        self.page = 1
        self.quality = 0
        self.maxPage = math.ceil(len(INGREDIENTS_LIST) / 10)

    #Instantiate Sprite in the window.
        self.ingredientScreen = IngredientScreen(self.page, self, self.evManager, self.group)
        PrevPage(WIDTH * 75 / 100, HEIGHT * 30 / 100, 50, 50, self, self.group)
        self.pageDisplay = Numbers(self, "page", WIDTH * 74/100, HEIGHT * 38/100, WHITE, 24, self.group)
        Text("/", WIDTH * 75/100, HEIGHT * 38/100, WHITE, 32, self.group, CENTER)
        Numbers(self, "maxPage", WIDTH * 76/100, HEIGHT * 38 / 100, WHITE, 24, self.group, LEFT)
        NextPage(WIDTH * 75 / 100, HEIGHT * 46 / 100, 50, 50, self, self.group)
        MarketCart(self.evManager, group)

        for tab in self.tab:
            imageName = str(qualityNumber) + "quality.png"
            image = pygame.image.load(os.path.join(imgFolder, imageName)).convert()
            QualityTab(x, y, image, qualityNumber, self, self.evManager, group)
            x += 110
            qualityNumber += 1

        ev = ClearCartEvent()
        self.evManager.Post(ev)


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
        self.ingredientScreen = IngredientScreen(self.page, self, self.evManager, self.group)

        self.pageDisplay.Update()


class QualityTab(pygame.sprite.Sprite):
    def __init__(self, x, y, image, quality, window, evManager, group=None):
        self.evManager = evManager

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
    def __init__(self, page, window, evManager, group=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.imageName = "Container.png"
        self.image = pygame.image.load(os.path.join(imgFolder, self.imageName)).convert()
        self.group = group
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 46.5 / 100, HEIGHT * 38 / 100)
        self.ingredientContainers = []

        self.window = window
        self.page = page - 1

        x = WIDTH * 34 / 100
        y = HEIGHT * 22.5 / 100
        baseIndex = self.page * 10
        for i in range(10):
            try:
                ingredient = INGREDIENTS_LIST[i + baseIndex]
                self.ingredientContainers.append(IngredientContainer(x, y, ingredient, self.window, self.evManager,
                                                                     group))
                y += 55
                if i == 4:
                    x += 315
                    y = HEIGHT * 22.5 / 100
            except IndexError:
                break

    def Clicked(self):
        return


class IngredientContainer(pygame.sprite.Sprite):
    def __init__(self, x, y, ingredient, window, evManager, group=None):
        self.evManager = evManager

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
        self.price = self.ingredient.Price(self.quality)

        self.ingredientQuantity = Numbers(self, "quantity", self.x + 120, self.y - 13, WHITE, 16, group)
        self.ingredientQuality = Numbers(self, "quality", self.x - 85, self.y + 5, WHITE, 16, group)
        self.ingredientPrice = Numbers(self, "price", self.x, self.y + 5, WHITE, 16, group)

        self.contents.append(Text(self.ingredient.name, self.x - 100, self.y - 20, WHITE, 14, group))
        self.contents.append(IngredientSprite(self.x - 120, self.y, ingredient, self.evManager, group))

        self.contents.append(self.ingredientQuantity)
        self.contents.append(self.ingredientQuality)
        self.contents.append(self.ingredientPrice)

        self.contents.append(ArrowLeft(self.x + 85, self.y - 10,  self, "quantity", group))
        self.contents.append(ArrowRight(self.x + 135, self.y - 10,  self, "quantity", group))
        self.contents.append(AddToCart(self.x + 110, self.y + 10, self, self.evManager, group))

    def Update(self):
        self.quality = self.window.quality

        if self.quantity < 0:
            self.quantity = 0

        self.quantityDisplay = str(self.quantity)
        self.ingredientQuantity.Update()

        self.qualityDisplay = str(self.quality)
        self.ingredientQuality.Update()

        self.price = self.ingredient.Price(self.quality)
        self.ingredientPrice.Update()


class IngredientSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, ingredient, evManager, group=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.ingredient = ingredient
        self.x = x
        self.y = y
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLACK)
        #self.image = pygame.image.load(os.path.join(imgFolder, self.ingredient.name + ".png")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class AddToCart(pygame.sprite.Sprite):
    def __init__(self, x, y, container, evManager, group=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.container = container
        self.group = group
        self.image = pygame.Surface((65,17))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def Clicked(self):
        if self.container.quantity > 0:
            ev = AddToCartEvent(self.container.ingredient, self.container.quality, self.container.quantity)
            self.evManager.Post(ev)

            self.container.quantity = 0
            self.container.Update()


class MarketCart(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None):
        self.evManager = evManager

        pygame.sprite.Sprite.__init__(self, group)
        self.x = WIDTH * 85 / 100
        self.y = HEIGHT * 38 / 100
        self.group = group
        self.image = pygame.Surface((190, 300))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.cartScreen = CartScreen(self.x, self.y, self.evManager, group)
        PrevPage(self.rect.right - 20, self.rect.bottom - 43, 25, 25, self, group)
        NextPage(self.rect.right - 20, self.rect.bottom - 15, 25, 25, self, group)


class CartScreen(pygame.sprite.Sprite):
    def __init__(self, x, y, evManager, group=None):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.group = group
        self.image = pygame.Surface((180, 290))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.contents = []

    def Notify(self, event):
        if isinstance(event, CartUpdateEvent):
            for sprite in self.contents:
                for s in sprite.contents:
                    s.kill()
                self.contents = []
                sprite.kill()
            self.contents = []

            x = self.rect.left + 15
            y = self.rect.top + 30
            for item in event.cart:
                self.contents.append(ItemContainer(x, y, item, self, self.evManager, self.group))
                x += 30
                if len(self.contents) % 6 == 0:
                    x = self.rect.left + 15
                    y += 60
                if len(self.contents) % 24 == 0:
                    break


class ItemContainer(pygame.sprite.Sprite):
    def __init__(self, x, y, item, window, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager

        self.x = x
        self.y = y
        self.item = item
        self.window = window
        self.group = group

        self.image = pygame.Surface((50, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.contents = []

        self.contents.append(ItemSprite(self.x, self.y, self.item, self, self.evManager, self.group))
        self.contents.append(Text(str(self.item.quality), self.x - 3, self.y - 30, BLACK, 14, self.group))
        self.contents.append(Text(str(self.item.amount), self.x - 3, self.y + 10, BLACK, 14, self.group))

    def Clicked(self):
        ev = RemoveFromCartEvent(self.item)
        self.evManager.Post(ev)


class ItemSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, item, container, evManager, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.evManager = evManager

        self.x = x
        self.y = y
        self.item = item
        self.container = container
        self.group = group

        self.image = pygame.Surface((25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

# MAIN VIEW MODULE ---------------------------------------------------------------------------------------------


class View:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.init()

        self.screen = pygame.display.set_mode(DISPLAY_RESOLUTION)
        self.origin = pygame.Surface(DRAW_RESOLUTION)
        self.background = pygame.Surface(self.origin.get_size())
        self.background.fill(WHITE)
        self.screen.blit(self.background, (0, 0))
        pygame.display.set_caption("Restaurant Simulator")
        pygame.display.flip()


        #Sprite Layers and Groups
        self.mainUI = pygame.sprite.RenderUpdates()
        self.mainUI = pygame.sprite.RenderUpdates()
        self.windows = pygame.sprite.RenderUpdates()
        self.popUp = pygame.sprite.RenderUpdates()
        self.window = None

        #All sprite start from here.
        #Sprite will carry it group from here.
        self.staffTab = StaffTab(self.evManager, self.mainUI, self.windows, self.popUp)
        self.restaurantTab = RestaurantTab(self.evManager, self.mainUI, self.popUp)
        self.menuTab = MenuTab(self.evManager, self.mainUI, self.popUp)
        self.inventoryTab = InventoryTab(self.evManager, self.mainUI, self.popUp)
        self.midTab = MidTab(self.evManager, self.mainUI, self.mainUI, self.popUp, self.windows)
        self.financeTab = FinanceTab(self.evManager, self.mainUI, self.windows)
        self.customersTab = CustomersTab(self.evManager, self.mainUI, self.windows)
        self.rivalTab = RivalTab(self.evManager, self.mainUI, self.windows)
        self.datetime = DateTime(self.evManager, self.mainUI)


    def Notify(self, event):
        if isinstance(event, TickEvent):
            self.origin.fill(WHITE)

            self.mainUI.clear(self.origin, self.background)
            self.windows.clear(self.origin, self.background)
            self.popUp.clear(self.origin, self.background)

            self.mainUI.update()
            self.windows.update()
            self.popUp.update()

            dirtyRects = self.mainUI.draw(self.origin)
            dirtyRects += self.windows.draw(self.origin)
            dirtyRects += self.popUp.draw(self.origin)

            pygame.transform.scale(self.origin, DISPLAY_RESOLUTION, self.screen)

            pygame.display.flip()


        elif isinstance(event, GUIRequestWindowEvent):
            if self.window is not event.window:
                event.draw()
                self.window = event.window


        elif isinstance(event, LeftClickEvent):
            for sprite in self.mainUI:
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
            for sprite in self.popUp:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.Clicked()
                    except AttributeError:
                        continue


        elif isinstance(event, ShiftLeftClickEvent):
            for sprite in self.mainUI:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.ShiftClicked()
                    except AttributeError:
                        try:
                            sprite.Clicked()
                        except AttributeError:
                            continue
            for sprite in self.windows:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.ShiftClicked()
                    except AttributeError:
                        try:
                            sprite.Clicked()
                        except AttributeError:
                            continue
            for sprite in self.popUp:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.ShiftClicked()
                    except AttributeError:
                        try:
                            sprite.Clicked()
                        except AttributeError:
                            continue

        elif isinstance(event, CtrlLeftClickEvent):
            for sprite in self.mainUI:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.CtrlClicked()
                    except AttributeError:
                        try:
                            sprite.Clicked()
                        except AttributeError:
                            continue
            for sprite in self.windows:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.CtrlClicked()
                    except AttributeError:
                        try:
                            sprite.Clicked()
                        except AttributeError:
                            continue
            for sprite in self.popUp:
                if sprite.rect.collidepoint(event.pos):
                    try:
                        sprite.CtrlClicked()
                    except AttributeError:
                        try:
                            sprite.Clicked()
                        except AttributeError:
                            continue