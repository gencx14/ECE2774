class Load:
    loadCount = 0
    def __init__(self, name, busObject, powerRating, voltageRating):
        self.name = name
        self.bus1 = busObject
        self.p_rated = powerRating
        self.v_rated = voltageRating
        self.loadResistance = (voltageRating ** 2) / powerRating
        Load.loadCount += 1


    # set functions
    def setName(self, name):
        self.name = name
    def setbus1(self, busObject):
        self.bus1 = busObject
    def setPower(self, power):
        self.p_rated = power
    def setvoltage(self, voltageRating):
        self.v_rated = voltageRating
    # get functions
    def getName(self):
        return self.name
    def getbus1(self):
        return self.bus1

    def getRatedPower(self):
        return self.p_rated
    def getRatedVoltage(self):
        return self.v_rated
    def getloadResistance(self):
        return self.loadResistance

