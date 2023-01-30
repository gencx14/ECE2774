class Bus:
    #Class Attribute
    busCount = 0
    def __init__(self, name):
        Bus.busCount += 1
        self.name = name
    def getBusCount(self):
        return Bus.busCount
    def getName(self):
        return self.name
    def setName(self, name):
        self.name = name

