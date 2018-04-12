from bin import *
import configparser
import copy


class Game:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.state = STATE_PREPARING

        self.player = Player(self.evManager)

        self.date = Date(self.evManager)
        self.customerManager = CustomerManager(self.evManager)

    def Start(self):
        self.state = STATE_STARTED
        self.LoadAssets()

    def LoadAssets(self):
        # Load list of ingredients
        config = configparser.ConfigParser()
        config.read("data/ingredients.rs")
        for section in config.sections():
            name = str(config.get(section, "name"))
            type = str(config.get(section, "type"))
            baseCost = config.getint(section, "cost")
            INGREDIENTS_LIST.append(Ingredient(name, type, baseCost, self.evManager))

        # Load list of dishes
        config = configparser.ConfigParser()  # Reinitiate for new file
        config.read("data/dishes.rs")
        for section in config.sections():
            name = str(config.get(section, "name"))
            foodType = str(config.get(section, "foodType"))
            cuisine = str(config.get(section, "cuisine"))
            rawIngre = str(config.get(section, "ingredients")).strip()

            ingredients = []
            for ingredient in rawIngre.split(','):
                for i in INGREDIENTS_LIST:
                    if ingredient == i.name:
                        ingredients.append(i)

            DISHES_LIST.append(Dish(name, foodType, cuisine, ingredients, self.evManager))

        ev = GameStartedEvent()
        self.evManager.Post(ev)

    def Notify(self, event):
        if isinstance(event, TickEvent):
            if self.state is STATE_PREPARING:
                self.Start()


class Player:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.inventory = Inventory(self.evManager)
        self.chefs = [Chef(CUISINE_WESTERN, self.evManager)]
        self.waiters = [Waiter(self.evManager)]

    def Notify(self, event):
        if isinstance(event, BuyIngredientEvent):
            new = True
            for batch in self.inventory.batches:
                if batch.age == 0:
                    batch.AddIngredients(event.ingredient, event.quality, event.amount)
                    new = False
            if new:
                newBatch = Batch(self.evManager)
                newBatch.AddIngredients(event.ingredient, event.quality, event.amount)
                self.inventory.batches.append(newBatch)

        elif isinstance(event, HireChefEvent):
            self.chefs.append(Chef(event.cuisine, self.evManager))

        elif isinstance(event, HireWaiterEvent):
            self.waiters.append(Waiter(self.evManager))


class Chef:
    def __init__(self, cuisine, evManager):
        self.evManager = evManager
        self.cuisine = cuisine
        # TODO: Possible features - chef experience


class Waiter:
    def __init__(self, evManager):
        self.evManager = evManager
        # TODO: Possible features - waiter experience


class Menu:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.dishes = []

    def AddDish(self, dish):
        self.dishes.append(dish)

    @property
    def AttractionPoints(self):
        points = 0
        for dish in self.dishes:
            points += dish.AttractionPoints

        return points

    def Notify(self, event):
        if isinstance(event, AddDishEvent):
            self.AddDish(event.dish)


class Dish:
    def __init__(self, name, foodType, cuisine, ingredients, evManager):
        self.evManager = evManager

        self.name = name
        self.foodType = foodType
        self.cuisine = cuisine
        self.ingredients = ingredients

        self.trendModifier = 1

    @property
    def AttractionPoints(self):
        points = DISH_POINTS * self.trendModifier
        return points

    def SatisfactionPoints(self):
        pass


class Ingredient:
    def __init__(self, name, ingreType, baseCost, evManager):
        self.evManager = evManager

        self.name = name
        self.type = ingreType
        self.baseCost = baseCost

        self.quality = None
        self.amount = None

    @property
    def Price(self, quality):
        # TODO: Price-quality algo
        return


class Inventory:
    def __init__ (self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.batches = []

    def RemoveBatch(self, batch):
        for b in self.batches:
            if b is batch:
                self.batches.remove(b)

    def Notify(self, event):
        if isinstance(event, BatchExpiredEvent):
            self.RemoveBatch(event.batch)


class Batch:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.batch = []
        self.age = 0

    def AddIngredients(self, ingredient, quality, amount):
        new = True
        for i in self.batch:
            if i.name == ingredient.name and i.quality == quality:
                i.amount += amount
                new = False
        if new:
            ing = copy.copy(ingredient)
            ing.quality = quality
            ing.amount = amount

            self.batch.append(ing)

    def RemoveIngredients(self, ingredient, quality, amount):
        for ing in self.batch:
            if ing.name == ingredient.name \
                    and ing.quality == quality:
                ing.amount -= amount

                if ing.amount == 0:
                    for i in self.batch:
                        if i is ing:
                            self.batch.remove(ing)

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.age += 1
            if self.age > 6:
                ev = BatchExpiredEvent(self)
                self.evManager.Post(ev)


def main():
    evManager = EventManager()
    game = Game(evManager)
    view = PygameView(evManager)
    control = Controller(evManager)

    control.Run()

if __name__ == '__main__':
    main()
