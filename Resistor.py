class Resistor:
    def __init__(self, name, bus1, bus2, ohms):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.resistance = ohms

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
