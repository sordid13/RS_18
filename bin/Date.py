from bin import *

class Date:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.day = 28
        self.month = 4
        self.year = 2016

        self.dayNumber = 0

    def NewMonth(self):
        self.day = 1
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1

            ev = NewYearEvent()
            self.evManager.Post(ev)

        ev = NewMonthEvent()
        self.evManager.Post(ev)

    def LeapYear(self):
        if self.year % 4 == 0:
            return True

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.day += 1
            self.dayNumber += 1

            if self.day == 29:
                if self.month == 2 and not self.LeapYear():
                    self.NewMonth()
            elif self.day == 30:
                if self.month == 2:
                    self.NewMonth()
            elif self.day == 31:
                if self.month in [4, 6, 9, 11]:
                    self.NewMonth()
            elif self.day == 32:
                self.NewMonth()

            print(self.day, self.month, self.year)
