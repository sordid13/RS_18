from bin import *


class DishManager:
    def __init__(self, player, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener()