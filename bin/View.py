import pygame
from pygame.locals import *
from .Events import *

class PygameView:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.init()

        # Set display
        self.window = pygame.display.set_mode((1280, 720), DOUBLEBUF)
        pygame.display.set_caption('Restaurant Simulator 2018')
        self.background = pygame.Surface(self.window.get_size())
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

    def Notify(self, event):
        if isinstance(event, TickEvent):
            pass