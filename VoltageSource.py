class VoltageSource:
    vSourceCount = 0
    def __init__(self, name, bus1, voltage):
        self.name = name
        self.bus1 = bus1
        self.voltage = voltage
        VoltageSource.vSourceCount += 1

    def setName(self, name):
        self.name = name
    def setBus1(self, bus1):
        self.bus1 = bus1
    def setVoltage(self, voltage):
        self.voltage = voltage

    def getName(self):
        return self.name
    def getBus1(self):
        return self.bus1
    def getVoltage(self):
        return self.voltage
