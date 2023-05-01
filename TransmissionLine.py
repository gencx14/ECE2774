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
        self.y = None
        self.y0 = None
        self.y1 = None
        self.y2 = None
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
        self.calc_y012()
        self.calc_z012()
        self.zPu = self.zseriesPu
        self.currentOverRating = None

    def calc_y(self):

        ypu_df = pd.DataFrame()
        ypu_df.loc[self.bus1, self.bus1] = self.yseriesPu + self.halfYshuntPu
        ypu_df.loc[self.bus1, self.bus2] = -1 * (self.yseriesPu)
        ypu_df.loc[self.bus2, self.bus1] = -1 * (self.yseriesPu)
        ypu_df.loc[self.bus2, self.bus2] = self.yseriesPu + self.halfYshuntPu
##check to see if this saves y as a variable
        self.y = ypu_df
    def calc_y012(self):
        self.y1 = self.y
        self.y2 = self.y
        self.y0 = 3 * self.y
    def calc_z012(self):
        self.z1 = 1 / self.y1
        self.z2 = 1 / self.y2
        self.z0 = 1 / self.y0

    def calc_vdf(self):
        vpu_df = pd.DataFrame()
        vpu_df.loc[self.bus1, self.bus1] = self.yseriesPu + self.halfYshuntPu
        vpu_df.loc[self.bus1, self.bus2] = -1 * (self.yseriesPu)
        vpu_df.loc[self.bus2, self.bus1] = -1 * (self.yseriesPu)
        vpu_df.loc[self.bus2, self.bus2] = self.yseriesPu + self.halfYshuntPu
        ##check to see if this saves y as a variable
        self.v = vpu_df










