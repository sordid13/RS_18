from bin import *
import math
import random


class CustomerManager:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.totalCustomers = None
        self.prevCustomers = STARTING_CUSTOMERS
        self.totalImpression = 100

    def TotalImpression(self, player, rival):
        impression = player.ImpressionPoints() + rival.ImpressionPoints()
        self.totalImpression = impression
        print(player.ImpressionPoints())
        print(rival.ImpressionPoints())

    def TotalCustomers(self):
        # TODO: Implement BETTER system to generate number of customers incorporating random events
        customers = None
        r = random.randint(0, 1) # 50% chance
        if not r:
            customers = self.prevCustomers * 1.01 # Simple growth equation
            self.prevCustomers = customers
        else:
            customers = self.prevCustomers

        self.totalCustomers = math.floor(customers)

    def CalculateCustomerSplit(self, impression):
        # TODO: Implement system to calculate customer split
        customers = math.floor(self.totalCustomers * (impression / self.totalImpression))

        if customers < 0:
            customers = 0

        return customers

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.TotalCustomers()