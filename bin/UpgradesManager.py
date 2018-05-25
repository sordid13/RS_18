from bin import *

class UpgradesManager:
    def __init__(self, evManager):
        self.evManager = evManager

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.evManager = Main.evManager
        print(self.evManager)

    def UpgradeLevel(self, player):  # initial LEVEL is 1
        player.restaurantLvl = self.NextLevel(player)

    def UpgradeLevelCost(self, player):
        cost = 1000000 * player.restaurantLvl**2 *(player.restaurantCapacity/100)
        return int(cost)

    def UpgradeCapacity(self, player):
        player.restaurantCapacity = self.NextCapacity(player)

    def UpgradeCapacityCost(self, player):
        cost = 1000000 * player.restaurantLvl**2 *(player.restaurantCapacity/100)
        return int(cost)

    def NextLevel(self, player):
        if player.restaurantLvl < 5:
            level = player.restaurantLvl + 1
        else:
            level = 5

        return level

    def NextCapacity(self, player):
        capacity = player.restaurantCapacity * 2
        return capacity

    def OperatingCost(self, level, capacity):
        cost = 70000 * (level**2) *(capacity/100)
        return int(cost)
