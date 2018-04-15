from bin import *
import math


class CustomerManager:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.totalCustomers = None
        self.prevCustomers = STARTING_CUSTOMERS
        self.totalImpression = 100

    def TotalCustomers(self):
        # TODO: Implement BETTER system to generate number of customers for the day
        customers = None
        customers = self.prevCustomers * 1.005 # Temporary growth equation
        self.prevCustomers = customers

        self.totalCustomers = math.floor(customers)

    def CalculateCustomerSplit(self, impression):
        # TODO: Implement system to calculate customer split
        customers = math.floor(self.totalCustomers * (impression / self.totalImpression))

        return customers

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.TotalCustomers()