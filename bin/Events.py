class TickEvent:
    def __init__(self):
        self.name = "Tick Event"


class QuitEvent:
    def __init__(self):
        self.name = "Quit Event"


class GameStartedEvent:
    def __init__(self, ingredientsList, dishesList):
        self.name = "Game Started Event"
        # Reference attributes to View/Controller
        self.ingredientsList = ingredientsList
        self.dishesList = dishesList


class NewDayEvent:
    def __init__(self):
        self.name = "New Day Event"


class NewWeekEvent:
    def __init__(self):
        self.name = "New Week Event"


class NewMonthEvent:
    def __init__(self):
        self.name = "New Week Event"


class NewYearEvent:
    def __init__(self):
        self.name = "New year Event"


class AddDishEvent:
    def __init__(self, dish):
        self.name = "Add Dish Event"
        self.dish = dish


class BuyIngredientEvent:
    def __init__(self, ingredient, quality, amount):
        self.name = "Buy Ingredient Event"
        self.ingredient = ingredient
        self.quality = quality
        self.amount = amount


class BatchExpiredEvent:
    def __init__(self, batch):
        self.name = "Batch Expired Event"
        self.batch = batch


class HireChefEvent:
    def __init__(self, cuisine):
        self.name = "Hire Chef Event"
        self.cuisine = cuisine


class HireWaiterEvent:
    def __init__(self):
        self.name = "Hire Waiter Event"
