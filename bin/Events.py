class TickEvent:
    def __init__(self):
        self.name = "Tick Event"


class QuitEvent:
    def __init__(self):
        self.name = "Quit Event"


class GameStartedEvent:
    def __init__(self):
        self.name = "Game Started Event"


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
        self.name = "New Year Event"


class SalesReportEvent:
    def __init__(self, customers, unfedCustomers, revenue, satisfaction):
        self.name = "Sales Report Event"
        self.customers = customers
        self.unfedCustomers = unfedCustomers
        self.revenue = revenue
        self.satisfaction = satisfaction


class AddDishEvent:
    def __init__(self, dish, price):
        self.name = "Add Dish Event"
        self.dish = dish
        self.price = price


class AddIngredientToCartEvent:
    def __init__(self, ingredient, quality, amount):
        self.name = "Add Ingredient To Cart Event"
        self.ingredient = ingredient
        self.quality = quality
        self.amount = amount


class BuyIngredientsEvent:
    def __init__(self, batch):
        self.name = "Buy Ingredients Event"
        self.batch = batch


class BatchExpiredEvent:
    def __init__(self, batch):
        self.name = "Batch Expired Event"
        self.batch = batch


class HireChefEvent:
    def __init__(self, level, cuisine):
        self.name = "Hire Chef Event"
        self.level = level
        self.cuisine = cuisine


class HireWaiterEvent:
    def __init__(self):
        self.name = "Hire Waiter Event"

class NoChefEvent:
    def __init__(self):
        self.name = "No Chef Event"

class LeftClickEvent:
    def __init__(self, pos):
        self.name = "Left Click Event"
        self.pos = pos


class ShiftLeftClickEvent:
    def __init__(self, pos):
        self.name = "Shift Left Click Event"
        self.pos = pos


class CtrlLeftClickEvent:
    def __init__(self, pos):
        self.name = "Ctrl Left Click Event"
        self.pos = pos