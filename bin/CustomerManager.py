from bin import *
import math
import random


class CustomerManager:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.totalCustomers = None
        self.prevCustomers = STARTING_CUSTOMERS

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

    def CalculateCustomerSplit(self, players):
        self.TotalCustomers()

        totalImpression = 0
        for player in players:
            player.impression = player.CalculateImpression()
            if player.impression > 0:
                totalImpression += player.impression
            else:
                player.impression = 0

        # TODO: Capacity overflow

        leftoverCustomers = 0
        for player in players:
            print(player.name + " " + str(player.impression))
            customers = math.floor(self.totalCustomers * (player.impression / totalImpression))

            if customers > player.restaurantCapacity:
                leftoverCustomers = customers - player.restaurantCapacity
                customers = player.restaurantCapacity

            player.ProcessSales(customers)

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.TotalCustomers()