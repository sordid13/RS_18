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


class AddToCartEvent:
    def __init__(self, ingredient, quality, amount):
        self.name = "Add Ingredient To Cart Event"
        self.ingredient = ingredient
        self.quality = quality
        self.amount = amount


class RemoveFromCartEvent:
    def __init__(self, ingredient):
        self.name = "Remove Ingredient From Cart Event"
        self.ingredient = ingredient


class CartUpdateEvent:
    def __init__(self, cart, price):
        self.name = "Cart Update Event"
        self.cart = cart
        self.price = price

class ClearCartEvent:
    def __init__(self):
        self.name = "Clear Cart"


class BuyIngredientsEvent:
    def __init__(self, cart):
        self.name = "Buy Ingredients Event"
        self.cart = cart


class BatchExpiredEvent:
    def __init__(self, batch):
        self.name = "Batch Expired Event"
        self.batch = batch


class OpenHireStaffEvent:
    def __init__(self):
        self.name = "Open Hire Staff"



class OpenMyStaffEvent:
    def __init__(self):
        self.name = "Open My Staff"



class SelectStaffEvent:
    def __init__(self, staffType):
        self.name = "Select Staff"
        self.staffType = staffType





class SelectCuisineEvent:
    def __init__(self, cuisine):
        self.name = "Select Cuisine"
        self.cuisine = cuisine


class HireChefEvent:
    def __init__(self, level, cuisine):
        self.name = "Hire Chef Event"
        self.level = level
        self.cuisine = cuisine


class HireWaiterEvent:
    def __init__(self, level):
        self.name = "Hire Waiter Event"
        self.level = level

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


# AI-Related Events

class RivalSalesReportEvent:
    def __init__(self, customers, unfedCustomers, revenue, satisfaction):
        self.name = "Rival Sales Report Event"
        self.customers = customers
        self.unfedCustomers = unfedCustomers
        self.revenue = revenue
        self.satisfaction = satisfaction