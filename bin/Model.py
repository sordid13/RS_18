from bin import *
import configparser
import copy


class Game:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.state = STATE_PREPARING

        self.dateManager = DateManager(self.evManager)
        self.customerManager = CustomerManager(self.evManager)
        self.dishManager = DishManager(self.evManager)

        self.players = None

    def Start(self):
        self.LoadAssets()

        self.players = [Player(self, self.evManager)]

        self.state = STATE_STARTED
        ev = GameStartedEvent()
        self.evManager.Post(ev)

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
            foodType = str(config.get(section, "type"))
            cuisine = str(config.get(section, "cuisine"))
            rawIngre = str(config.get(section, "ingredients")).strip()

            ingredients = []
            split = rawIngre.split(', ')
            for ingredient in split:
                for i in INGREDIENTS_LIST:
                    if ingredient == i.name:
                        ingredients.append(i)
                        break
            if len(split) > len(ingredients):
                print("No Ingredient Error")

            dish = Dish(name, foodType, cuisine, ingredients, self.evManager)
            DISHES_LIST.append(dish)
            if cuisine == "Western":
                WESTERN_DISHES.append(dish)
            elif cuisine == "Chinese":
                CHINESE_DISHES.append(dish)
            elif cuisine == "Japanese":
                JAPANESE_DISHES.append(dish)
            elif cuisine == "Korean":
                KOREAN_DISHES.append(dish)
            elif cuisine == "Indian":
                INDIAN_DISHES.append(dish)

    def Notify(self, event):
        if isinstance(event, TickEvent):
            if self.state is STATE_PREPARING:
                self.Start()

        elif isinstance(event, NewDayEvent):
            self.customerManager.TotalImpression(self.players)


class Player:
    def __init__(self, game, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.game = game

        self.customerManager = self.game.customerManager
        self.dishManager = self.game.dishManager

        # Changes daily
        self.baseImpression = 80

        self.cash = 1000
        self.restaurantLvl = 0
        self.restaurantCapacity = 50
        self.menu = Menu(self.evManager)
        self.inventory = Inventory(self.evManager)
        self.chefs = [Chef(CUISINE_WESTERN, 0, self.evManager), Chef(CUISINE_WESTERN, 3, self.evManager),
                      Chef(CUISINE_CHINESE, 0, self.evManager), Chef(CUISINE_CHINESE, 3, self.evManager),
                      Chef(CUISINE_INDIAN, 0, self.evManager)]
        self.waiters = [Waiter(0, self.evManager)]

    def GetChefs(self):
        # Returns highest level of each cuisine chef in dictionary
        chefs = []
        for chef in self.chefs:
            if chef.cuisine not in (c['cuisine'] for c in chefs):
                chefDict = dict(cuisine=chef.cuisine, level=chef.level)
                chefs.append(chefDict)
            else:
                for c in chefs:
                    if chef.cuisine == c['cuisine'] and chef.level > c['level']:
                        c['level'] = chef.level
        return chefs

    def WaitersExperience(self):
        experience = 0
        for waiter in self.waiters:
            experience += waiter.level
        return experience / len(self.waiters)

    def ImpressionPoints(self):
        restaurantModifier = 0.05 * self.restaurantLvl
        marketingModifier = 0 # TODO: Call function in marketing module
        impression = self.baseImpression * (1 + restaurantModifier + marketingModifier)

        return math.floor(impression)

    def SatisfactionPoints(self, dishesServed, customers, unfedCustomers):
        # Calculate satisfaction based on base cost to sale price value
        costModifier = self.restaurantLvl ** 1.7
        totalSatisfaction = 0

        # Calculate gross satisfaction
        for dish in dishesServed:
            qualityModifier = (dish['quality'] / 20) + 1  # Scale from 10 to 1.5, 1 to 1.05
            cost = dish['dish'].baseCost ** qualityModifier
            adjustedCost = cost + costModifier

            satisfaction = (adjustedCost / dish['price']) * 100
            if satisfaction > 100:
                satisfaction = 100

            totalSatisfaction += satisfaction * dish['sales']

            if dish['demand'] > dish['sales']:
                missingDemand = dish['demand'] - dish['sales']
                totalSatisfaction -= missingDemand * 40

        totalSatisfaction -= unfedCustomers * 200

        # Customer service modifiers
        insufficientStaffToCustomers = customers - (len(self.waiters) * 50)
        if insufficientStaffToCustomers > 0:
            totalSatisfaction -= insufficientStaffToCustomers ** 2

        x = self.WaitersExperience()
        totalSatisfaction *= 0.95 + 0.5 * (x ** x)

        return math.floor(totalSatisfaction)

    def ProcessSales(self):
        impression = self.ImpressionPoints()

        rawCustomers = self.customerManager.CalculateCustomerSplit(impression) # Number not finalised
        dishesServed = self.dishManager.ProcessDishes(self, rawCustomers)

        actualCustomers = self.dishManager.Customers(dishesServed)
        unfedCustomers = self.dishManager.UnfedCustomers(dishesServed)
        salesRevenue = self.dishManager.SalesRevenue(dishesServed)

        satisfaction = self.SatisfactionPoints(dishesServed, actualCustomers, unfedCustomers)
        self.baseImpression += satisfaction

        ev = SalesReportEvent
        self.evManager.Post(ev)

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.ProcessSales()

        elif isinstance(event, BuyIngredientsEvent):
            new = True
            for batch in self.inventory.batches:
                # Loop and check for same-day batch
                if batch.age == 0:
                    batch.AddIngredients(event.cart)
                    new = False
            if new:
                newBatch = Batch(self.evManager)
                newBatch.AddIngredients(event.cart)
                self.inventory.batches.append(newBatch)

        elif isinstance(event, HireChefEvent):
            self.chefs.append(Chef(event.level, event.cuisine, self.evManager))

        elif isinstance(event, HireWaiterEvent):
            self.waiters.append(Waiter(self.evManager))


class AI(Player):
    def __init__(self, game, evManager):
        super().__init__(game, evManager)

        # TODO: Create AI mechanics

    def Notify(self, event):
        pass


class Chef:
    def __init__(self, cuisine, level, evManager):
        self.evManager = evManager
        self.name = ""
        self.cuisine = cuisine
        self.level = level
        # TODO: Possible features - chef experience


class Waiter:
    def __init__(self, level, evManager):
        self.evManager = evManager
        self.name = ""
        self.level = level
        # TODO: Possible features - waiter experience


class Menu:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        # Dishes stored as dictionary of 'dish' and 'price'
        self.dishes = []

    def AddDish(self, dish, price):
        dishDict = dict(dish=dish, price=price)
        if dishDict not in self.dishes:
            self.dishes.append(dishDict)

    @property
    def ImpressionPoints(self):
        points = 0
        for dish in self.dishes:
            points += dish['dish'].ImpressionPoints

        return points

    def Notify(self, event):
        if isinstance(event, AddDishEvent):
            self.AddDish(event.dish, event.price)


class Dish:
    def __init__(self, name, foodType, cuisine, ingredients, evManager):
        self.evManager = evManager

        self.name = name
        self.foodType = foodType
        self.cuisine = cuisine
        self.ingredients = ingredients

        self.numberIngredients = len(self.ingredients)

        self.baseCost = 0
        for ingredient in self.ingredients:
            self.baseCost += ingredient.baseCost

        self.trendModifier = 1

    @property
    def ImpressionPoints(self):
        points = DISH_POINTS * self.trendModifier
        return points


class Ingredient:
    def __init__(self, name, ingreType, baseCost, evManager):
        self.evManager = evManager

        self.name = name
        self.type = ingreType
        self.baseCost = baseCost

        self.quality = None
        self.amount = None

    def Price(self, quality):
        price = math.floor(self.baseCost ** (1 + quality/10))
        return price


class Inventory:
    def __init__ (self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.batches = []

    def IngredientStock(self, ingredient):
        stock = [0, 0, 0, 0, 0, 0] # Initialise based on quality 5 to 0
        for batch in self.batches:
            addStock = batch.IngredientStock(ingredient)
            stock = [sum(x) for x in zip(stock, addStock)] # Sums value of corresponding elements

        return stock

    def UseIngredients(self, dish, amount):
        # amount must be non-zero
        # Debits ingredient stock based on precalculated amount of dishes (amount reflects how much able to make)
        for ingredient in dish.ingredients:
            useAmount = amount
            quality = 5
            countIngredient = True
            while countIngredient:
                for batch in self.batches:
                    for i in batch.batch:
                        if i.name == ingredient.name and i.quality == quality:
                            i.amount -= useAmount
                            if i.amount < 0:
                                useAmount = - i.amount
                                i.amount = 0
                                break
                            else:
                                useAmount = 0
                                countIngredient = False
                quality -= 1


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

    def IngredientStock(self, ingredient):
        stock = [0, 0, 0, 0, 0, 0] # Initialise based on quality 0 to 5
        for i in self.batch:
            if i.name == ingredient.name:
                quality = i.quality
                amount = i.amount
                stock[quality] = amount

        stock.reverse()
        return stock

    def AddIngredients(self, list):
        new = True
        for ingredient in list:
            for i in self.batch:
                if i.name == ingredient.name and i.quality == ingredient.quality:
                    i.amount += ingredient.amount
                    new = False
            if new:
                self.batch.append(ingredient)

    def RemoveIngredients(self, ingredient, quality, amount):
        for ing in self.batch:
            if ing.name == ingredient.name \
                    and ing.quality == quality:
                ing.amount -= amount

                if ing.amount == 0:
                    for i in self.batch:
                        if i is ing:
                            self.batch.remove(ing)

    def Clear(self):
        self.batch = []

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.age += 1
            if self.age > 6:
                ev = BatchExpiredEvent(self)
                self.evManager.Post(ev)


class Cart:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.cart = []
        self.totalPrice = 0

    def AddToCart(self, ingredient, quality, amount):
        new = True
        for i in self.cart:
            if i.name == ingredient.name and i.quality == ingredient.quality:
                i.amount += amount
                new = False

        if new:
            newIng = ingredient
            newIng.quality = ingredient.quality
            newIng.amount = ingredient.amount
            self.cart.append(newIng)

        self.totalPrice += ingredient.Price(quality) * amount

        # Tell View to update cart list
        ev = CartUpdateEvent(self.cart, self.totalPrice)
        self.evManager.Post(ev)

    def RemoveFromCart(self, ingredient):
        for i in self.cart:
            if i.name == ingredient.name and i.quality == ingredient.quality:
                self.cart.remove(i)

        self.totalPrice -= ingredient.Price(ingredient.quality) * ingredient.amount

        ev = CartUpdateEvent(self.cart, self.totalPrice)
        self.evManager.Post(ev)

    def Notify(self, event):
        if isinstance(event, AddToCartEvent):
            self.AddToCart(event.ingredient, event.quality, event.amount)

        elif isinstance(event, RemoveFromCartEvent):
            self.RemoveFromCart(event.ingredient)


def main():
    evManager = EventManager()
    game = Game(evManager)
    view = View(evManager)
    control = Controller(evManager)

    control.Run()

if __name__ == '__main__':
    main()
