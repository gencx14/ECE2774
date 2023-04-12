from Bus import Bus
import pandas as pd
from BaseValues import BaseValues
from TransmissionLineData import TransmissionLineData
from BaseValues import BaseValues
class TransmissionLine:
 #when calling this class the user bus insert a string name, bus object Busses, and an object of the transmission line Data class for the data
    def __init__(self, name: str, bus1: Bus, bus2: Bus, lineData: TransmissionLineData, length, bases: BaseValues):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.buses = [self.bus1, self.bus2]
        self.data = lineData
        self.bases = bases
        self.totalZseries = self.data.zseriesperMile * length
        self.zseriesPu = self.totalZseries / bases.zbase
        self.totalYseries = 1 / self.totalZseries
        self.yseriesPu = self.totalYseries / bases.ybase
        self.totalYshunt = self.data.yshuntperMile * length
        self.halfYshunt = self.totalYshunt / 2
        self.halfYshuntPu = self.halfYshunt / bases.ybase
        self.calc_y()

    def calc_y(self):

        ypu_df = pd.DataFrame()
        ypu_df.loc[self.bus1, self.bus1] = self.yseriesPu + self.halfYshuntPu
        ypu_df.loc[self.bus1, self.bus2] = -1 * (self.yseriesPu)
        ypu_df.loc[self.bus2, self.bus1] = -1 * (self.yseriesPu)
        ypu_df.loc[self.bus2, self.bus2] = self.yseriesPu + self.halfYshuntPu
##check to see if this saves y as a variable
        self.y = ypu_df










