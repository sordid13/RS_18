from pygame.locals import *
import pygame

from .Events import *

class Controller:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.keepGoing = True

        self.ingredientsList = None

    def Run(self):
        while self.keepGoing:
            ev = TickEvent()
            self.evManager.Post(ev)

            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = QuitEvent()

                # Temporary Test Events
                elif event.type == KEYDOWN and event.key == K_q:
                    ev = BuyIngredientEvent(self.ingredientsList[0], 5, 100)

                elif event.type == KEYDOWN and event.key == K_w:
                    ev = BuyIngredientEvent(self.ingredientsList[0], 4, 100)

                elif event.type == KEYDOWN and event.key == K_e:
                    ev = NewDayEvent()

                if ev:
                    self.evManager.Post(ev)

    def Notify(self, event):
        if isinstance(event, QuitEvent):
            self.keepGoing = False

        elif isinstance(event, GameStartedEvent):
            self.ingredientsList = event.ingredientsList