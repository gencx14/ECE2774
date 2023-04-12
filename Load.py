import pandas as pd
class Load:
    loadCount = 0
    def __init__(self, name, busObject, powerRating, voltageRating):
        self.name = name
        self.bus1 = busObject
        self.p_rated = powerRating
        self.v_rated = voltageRating
        self.loadResistance = (voltageRating ** 2) / powerRating
        Load.loadCount += 1

        #may eventually want the following line:
        #self.buses = [self.bus1]


    # set functions
    def set_name(self, name):
        self.name = name
    def set_bus1(self, busObject):
        self.bus1 = busObject
    def set_power(self, power):
        self.p_rated = power
    def set_voltage(self, voltageRating):
        self.v_rated = voltageRating
    # get functions
    def get_name(self):
        return self.name
    def get_bus1(self):
        return self.bus1

    def get_ratedpower(self):
        return self.p_rated
    def get_ratedvoltage(self):
        return self.v_rated
    def get_loadresistance(self):
        return self.loadResistance
    #calculate the admittance
    def calc_admittance(self):
        #caluclate admittance locally
        g = 1/self.loadResistance
        #create a pandas dataframe
        g_df = pd.DataFrame()
        #stores the admittance value in the row and column both associated with bus1
        g_df.loc[self.bus1, self.bus1] = g
        #stores the admittance to the load object
        self.g = g_df



