from bin import *
import numpy
import json


class TrendManager:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

    def SetTrend(self):
        pass


    def Notify(self, event):
        if isinstance(event, NewDayEvent):
            self.SetTrend()