from bin import *
import json
import matplotlib
import pygame
import pylab
import matplotlib.backends.backend_agg as agg
from pygame.locals import *
matplotlib.use("Agg")


class Finance:
    def __init__(self, player, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.player = player

        self.folder = "data"

        try:
            with open(self.folder + '/cashFlow.json', 'r') as json_file:
                json_file.close()
        except FileNotFoundError:
            key = {'daily': [], 'monthly': [], 'yearly': []}
            with open(self.folder + '/cashFlow.json', 'a+') as json_file:
                json.dump(key, json_file)
                json_file.close()

    def NewDay(self):
        cashFlow = dict()
        cashFlow[CASH] = self.player.cash
        cashFlow[SALES] = 0
        cashFlow[INVENTORY] = 0
        cashFlow[MARKETING] = 0
        cashFlow[RENOVATION] = 0
        cashFlow[SALARY] = 0
        cashFlow[MISC] = 0
        cashFlow['Expense'] = 0
        cashFlow['Profit'] = 0
        cashFlow['Day'] = Date.day
        cashFlow['Month'] = Date.month
        cashFlow['Year'] = Date.year

        with open(self.folder + '/cashFlow.json', 'r') as json_file:
            cashDict = json.load(json_file)
            cashDict['daily'].append(cashFlow)
        json_file.close()

        with open(self.folder + '/cashFlow.json', 'w') as json_file:
            json.dump(cashDict, json_file, indent=2)
        json_file.close()

    def NewMonth(self):
        cashFlow = dict()
        cashFlow[CASH] = self.player.cash
        cashFlow[SALES] = 0
        cashFlow[INVENTORY] = 0
        cashFlow[MARKETING] = 0
        cashFlow[RENOVATION] = 0
        cashFlow[SALARY] = 0
        cashFlow[MISC] = 0
        cashFlow['Expense'] = 0
        cashFlow['Profit'] = 0
        cashFlow['Month'] = Date.month
        cashFlow['Year'] = Date.year

        with open(self.folder + '/cashFlow.json', 'r') as json_file:
            cashDict = json.load(json_file)
            cashDict['monthly'].append(cashFlow)
        json_file.close()

        with open(self.folder + '/cashFlow.json', 'w') as json_file:
            json.dump(cashDict, json_file, indent=2)
        json_file.close()

    def NewYear(self):
        cashFlow = dict()
        cashFlow[CASH] = self.player.cash
        cashFlow[SALES] = 0
        cashFlow[INVENTORY] = 0
        cashFlow[MARKETING] = 0
        cashFlow[RENOVATION] = 0
        cashFlow[SALARY] = 0
        cashFlow[MISC] = 0
        cashFlow['Expense'] = 0
        cashFlow['Profit'] = 0
        cashFlow['Year'] = Date.year

        with open(self.folder + '/cashFlow.json', 'r') as json_file:
            cashDict = json.load(json_file)
            cashDict['yearly'].append(cashFlow)
        json_file.close()

        with open(self.folder + '/cashFlow.json', 'w') as json_file:
            json.dump(cashDict, json_file, indent=2)
        json_file.close()

    #   This edit the current day's dictionary. Make sure the entry would be corresponding!! Ask Hakeem,
    def CashFlowDay(self, value, category):

        with open(self.folder + '/cashFlow.json', 'r') as json_file:
            cashFlow = json.load(json_file)
        json_file.close()

        for i in range(0, len(cashFlow['day'])):
            if cashFlow['daily'][i]['Day'] == Date.day and cashFlow['daily'][i]['Month'] == Date.month and\
                    cashFlow['daily'][i]['Year'] == Date.year:

                with open(self.folder + '/cashFlow.json', 'w') as json_file:
                    cashFlow = json.load(json_file)

                cashFlow['daily'][i][CASH] = self.player.cash
                cashFlow['daily'][i][category] += value

                json_file.close()

    def CashFlowMonth(self, category, value):
        with open(self.folder + '/cashFlow.json', 'r') as json_file:
            cashFlow = json.load(json_file)
        json_file.close()

        for i in range(0, len(cashFlow['month'])):
            if cashFlow['monthly'][i]['Month'] == Date.month and cashFlow['monthly'][i]['Year'] == Date.year:
                with open(self.folder + '/cashFlow.json', 'w') as json_file:
                    cashFlow = json.load(json_file)

                cashFlow['monthly'][i][CASH] = self.player.cash
                cashFlow['monthly'][i][category] += value

                json_file.close()

    def CashFlowYear(self, category, value):
        with open(self.folder + '/cashFlow.json', 'r') as json_file:
            cashFlow = json.load(json_file)
        json_file.close()

        for i in range(0, len(cashFlow['year'])):
            if cashFlow['yearly'][i]['Year'] == Date.year:
                with open(self.folder + '/cashFlow.json', 'w') as json_file:
                    cashFlow = json.load(json_file)

                cashFlow['yearly'][i][CASH] = self.player.cash
                cashFlow['yearly'][i][category] += value

                json_file.close()

    def Graph(self, category, type):
        graph = []
        with open(self.folder + '/cashFlow.json', 'r') as json_file:
            cashFlow = json.load(json_file)

        for dictionary in cashFlow[type]:
            graph.append(dictionary[category])
        json_file.close()

        fig = pylab.figure(figsize=[6, 6],  # Inches width * height
                           dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        ax.plot([10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000])
        ax.plot([12000, 10222, 13422, 11111, 13333, 12345, 12314, 11345])
        ax.plot(graph)
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        pygame.init()
        # width *height
        window = pygame.display.set_mode((600, 600), DOUBLEBUF)
        screen = pygame.display.get_surface()

        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (0, 0))
        pygame.display.flip()

    def CashBook(self, fiscalTerm, type):
        with open(self.folder + '/cashFlow.json', 'r') as json_file:
            cashFlow = json.load(json_file)
        json_file.close()

        if fiscalTerm == DAILY:
            for book in cashFlow[fiscalTerm]:
                if book['Day'] == date.day and book['Month'] == date.month and book['Year'] == date.year:
                    Cash = book[CASH]
                    Sales = book[SALES]
                    Inventory = book[INVENTORY]
                    Marketing = book[MARKETING]
                    Renovation = book[RENOVATION]
                    Salary = book[SALARY]
                    Misc = book[MISC]
                    Expense = book[EXPENSE]
                    Profit = book[PROFIT]
                    dayBefore = book['DayNumber']


    # get daily or monthly or yearly
    # check date
    # pass the value in the dict

    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.NewDay()
            self.Graph(CASH, "daily")

        elif isinstance(event, NewMonthEvent):
            self.NewMonth()

        elif isinstance(event, NewYearEvent):
            self.NewYear()

        elif isinstance(event, CashFlowUpdateEvent):
            self.CashFlowDay(self, event.category)
            self.CashFlowMonth(self, event.category)
            self.CashFlowYear(self, event.category)
