from bin import *
import random


class TrendManager:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.trends = [self.DishTrend, self.FoodTypeTrend, self.CuisineTypeTrend]
        self.currentTrend = None
        self.pastTrend = []

        if len(self.pastTrend) == 10:
            self.pastTrend = []

    def SetTrend(self):
        self.pastTrend.append(self.currentTrend)
        self.currentTrend = random.choices(self.trends, weights=[10, 3, 2], k=1)[0]()

        for dish in DISHES_LIST:
            if dish == self.currentTrend:
                dish.trendModifier = 2

            elif dish.type == self.currentTrend:
                dish.trendModifier = 2

            elif dish.cuisine == self.currentTrend:
                dish.trendModifier = 2

            else:
                dish.trendModifier -= 0.2
                if float(dish.trendModifier) < 0.4:
                    dish.trendModifier = 0.4

        ev = SetTrendEvent(self.currentTrend)
        print(self.currentTrend)
        self.evManager.Post(ev)


    def DishTrend(self):
        trendItem = random.choice(DISHES_LIST)

        return trendItem

    def FoodTypeTrend(self):
        trendItem = random.choice(FOOD_TYPE_LIST)

        return trendItem

    def CuisineTypeTrend(self):
        trendItem = random.choice(CUISINES_LIST)

        return trendItem

    def Notify(self, event):
        if isinstance(event, NewWeekEvent):
            self.SetTrend()