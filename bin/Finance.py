from bin import *


class Finance:
    def __init__(self, player, evManager, revenue):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.player = player
        self.revenue = revenue

    # make sure that the cashflow day go through each transaction. Cashflowday updates dict. cashflowmonth

    def CreditCash(self, cost):
        self.player.cash -= cost
        CashFlowDay()

    def DebitCash(self, revenue):
        self.player.cash += revenue
        CashFlowDay()

    def CashFlowMonth(self, cost, revenue):
        cashHistoryMonth = []
        cashHistory.append({'day': Date.date, 'cash': self.player.cash, 'revenue': revenue, 'expense': cost})

    def CashFlowDay
        cashHistoryDay = []
        append.cashHistoryDay({'no.': y, 'transaction': z, 'earning': a, 'expense': b})