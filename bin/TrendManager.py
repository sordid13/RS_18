from bin import *
import random


class TrendManager:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.trends = [self.DishTrend(), self.FoodTypeTrend(), self.CuisineTypeTrend()]
        self.currentTrend = None
        self.pastTrend = []

        if len(self.pastTrend) == 10:
            self.pastTrend = []

    def SetTrend(self):
        random.seed()
        self.pastTrend.append(self.currentTrend)
        self.currentTrend = random.choice(self.trends)

        for dish in DISHES_LIST:
            if dish == self.currentTrend:
                dish.trendModifier = 2

            elif dish.type == self.currentTrend:
                dish.trendModifier = 2

            elif dish.cuisine == self.currentTrend:
                dish.trendModifier = 2

        ev = SetTrendEvent(self.currentTrend)
        print(self.currentTrend)
        self.evManager.Post(ev)


    def DishTrend(self):
        random.seed()
        trendItem = random.choice(DISHES_LIST)

        return trendItem

    def FoodTypeTrend(self):
        random.seed()
        trendItem = random.choice(FOOD_TYPE_LIST)

        return trendItem

    def CuisineTypeTrend(self):
        random.seed()
        trendItem = random.choice(CUISINES_LIST)

        return trendItem

    def Notify(self, event):
        if isinstance(event, NewWeekEvent):
            self.SetTrend()