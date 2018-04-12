from bin import *


class CustomerManager:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.startingCustomers = STARTING_CUSTOMERS

    def TotalCustomers(self):
        # TODO: Implement system to generate number of customers for the day
        pass

    def CalculateCustomerSplit(self):
        # TODO: Implement system to calculate customer split
        pass

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.CalculateCustomerSplit()