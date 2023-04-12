import pandas as pd
class Resistor:
    def __init__(self, name, bus1, bus2, ohms):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.resistance = ohms

        #creates an list of all the buses in the object
        self.buses = [self.bus1, self.bus2]


    def setName(self, name):
        self.name = name
    def setBus1(self, bus1):
        self.bus1 = bus1
    def setBus2(self, bus2):
        self.bus2 = bus2
    def setResistance(self, ohms):
        self.resistance = ohms
    def getName(self):
        return self.name
    def getBus1(self):
        return self.bus1
    def getBus2(self):
        return self.bus2
    def getResistance(self):
        return self.resistance
    #calculate the admittance
    def calcAdmittance(self):
        g = 1/self.resistance

        g_df = pd.DataFrame()

        g_df.loc[self.bus1, self.bus1] = g
        g_df.loc[self.bus2, self.bus2] = g
        g_df.loc[self.bus1, self.bus2] = -g
        g_df.loc[self.bus2, self.bus1] = -g

        self.g = g_df



