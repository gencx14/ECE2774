import pandas as pd
from Bus import Bus
class Generator:
    generator_count = 0

    def __init__(self, name, voltage, bus1: Bus, x1, x2, x0, Zg):
        self.name = name
        self.bus1 = bus1
        self.buses = [self.bus1]
        self.voltage = voltage
        self.voltDrop = None
        self.lineCurrent = None
        self.powerLosses = None
        self.powerSending_S = None
        self.powerRecieving_S = None
        self.y0 = None
        self.y1 = None
        self.y2 = None
        # if Zg = 0 then it is solid grounded, if Zg = inf then it is ungrounded, else it is what is given
        self.z0a = x0 + Zg * 3
        self.z1a = x1
        self.z2a = x2
        self.y0a = 1 / self.z0a
        self.y1a = 1 / self.z1a
        self.y2a = 1 / self.z2a
        self.currentOverRating = None
        self.calc_ysequence()
        Generator.generator_count += 1

    def calc_ysequence(self):
        y1pu_df = pd.DataFrame()
        y2pu_df = pd.DataFrame()
        y0pu_df = pd.DataFrame()

        # calculate positive sequence element y bus
        y1pu_df.loc[self.bus1, self.bus1] = self.y1a

        # calculate negative sequence element y bus
        y2pu_df.loc[self.bus1, self.bus1] = self.y2a

        # Calculate zero sequence element y bus
        y0pu_df.loc[self.bus1, self.bus1] = self.y0a

        #  Store the element y buses in the Transformer class
        self.y1 = y1pu_df
        self.y2 = y2pu_df
        self.y0 = y0pu_df
    def set_name(self, name):
        self.name = name

    def set_bus1(self, bus1):
        self.bus1 = bus1

    def set_voltage(self, voltage):
        self.voltage = voltage

    def get_name(self):
        return self.name

    def get_bus1(self):
        return self.bus1

    def get_voltage(self):
        return self.voltage
