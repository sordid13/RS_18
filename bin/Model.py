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

        self.players = [Player(self, self.evManager)]

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
            for ingredient in rawIngre.split(', '):
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
    def __init__(self, game, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.game = game

        self.impression = 20

        self.menu = Menu(self.evManager)
        self.inventory = Inventory(self.evManager)
        self.chefs = [Chef(CUISINE_WESTERN, self.evManager)]
        self.waiters = [Waiter(self.evManager)]

    def ProcessDay(self):
        dishByDemand = [self.menu.dishes[0]] # For initialize purposes
        customers = self.game.customerManager.CalculateCustomerSplit(self.impression)
        menuImpression = self.menu.ImpressionPoints

        # TODO: Transfer functions to DishManager

        # Arrange dishes based on demand
        for dish in self.menu.dishes:
            dish.demand = math.floor( (dish.ImpressionPoints / menuImpression) * customers )
            for d in dishByDemand:
                if dish.demand > d.demand and dish is not d:
                    i = dishByDemand.index(d)
                    dishByDemand = dishByDemand[:i] + [dish] + dishByDemand[i:]

        for dish in dishByDemand:
            dishAmount = int(dish.demand)
            print(dishAmount)

            # Calculate amount of dish can make based on ingredient availability
            for ingredient in dish.ingredients:
                stock = self.inventory.IngredientStock(ingredient)
                ingredientAmount = sum(stock)
                print(str(ingredient.name) + str(ingredientAmount))
                if ingredientAmount < dishAmount:
                    dishAmount = ingredientAmount
                dish.sales = dishAmount
            missingDemand = dish.demand - dishAmount

            # Calculate dish quality based on ingredients
            if dishAmount > 0:
                quality = 0
                for ingredient in dish.ingredients:
                    stock = self.inventory.IngredientStock(ingredient)
                    ingredientAmount = dishAmount
                    ingredientQuality = 5
                    for amount in stock:
                        if amount > 0:
                            amount -= ingredientAmount
                            if amount < 0:
                                ingredientAmount = - amount
                                quality += (dishAmount - ingredientAmount) * ingredientQuality
                            else:
                                quality += ingredientAmount * ingredientQuality
                                break
                        ingredientQuality -= 1

                averageQuality = quality / (dish.numberIngredients * dishAmount)
                print(averageQuality)
                self.inventory.UseIngredients(dish, dishAmount)
            else:
                dishByDemand.remove(dish)

            # Transfer missing demand to other dishes
            split = len(dishByDemand)
            if dish in dishByDemand:
                split -= 1

            for d in dishByDemand:
                if d is dish:
                    continue
                else:
                    d.demand += math.floor(missingDemand / split)

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.ProcessDay()

        elif isinstance(event, BuyIngredientEvent):
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


class AI(Player):
    def __init__(self, game, evManager):
        super().__init__(game, evManager)

        # TODO: Create AI mechanics

    def Notify(self, event):
        pass


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
        if dish not in self.dishes:
            self.dishes.append(dish)

    @property
    def ImpressionPoints(self):
        points = 0
        for dish in self.dishes:
            points += dish.ImpressionPoints

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
        self.numberIngredients = len(self.ingredients)

        self.trendModifier = 1

        # Only assigned and referenced in Player.ProcessDay() and DishManager
        # Not to be referenced elsewhere (will break)
        self.demand = 0
        self.sales = 0

    @property
    def ImpressionPoints(self):
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

        # Only assigned and referenced in Player.ProcessDay()
        # Not to be referenced elsewhere (will break)
        self.demand = 0

    @property
    def Price(self, quality):
        # TODO: Price-quality algo
        return


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
