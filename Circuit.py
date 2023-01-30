from Resistor import Resistor
from Load import Load
from VoltageSource import VoltageSource
from Bus import Bus
class Circuit:
    componentCount = 0
    CircuitCount = 0

    def __init__(self, name):
        self.name = name
        self.vItems = []
        self.rItems = []
        self.loadItems = []
        Circuit.CircuitCount += 1

    def addVsourceElement(self, name, bus_name, voltage):
        Circuit.componentCount += 1
        bus1 = Bus(bus_name)
        vsObject = VoltageSource(name, bus1, voltage)
        self.vItems.append(vsObject)
    def addResistorElement(self, name, bus1_name, bus2_name, ohms):
        Circuit.componentCount += 1
        bus1 = Bus(bus1_name)
        bus2 = Bus(bus2_name)
        resistorObject = Resistor(name, bus1, bus2, ohms) #creates a resistor object within my circuit object
        self.rItems.append(resistorObject)
    def addLoadElement(self, name, bus_name, power, voltage):
        Circuit.componentCount += 1
        bus1 = Bus(bus_name)
        loadObject = Load(name, bus1, power, voltage)
        self.loadItems.append(loadObject)
    def getVsourceElement(self, name):
        return self.vItems[self.vItems.index(name)]
    def getResistorElement(self, name):
        return self.rItems[self.rItems.index(name)]
    def getLoadElement(self, name):
        return self.loadItems[self.loadItems.index(name)]
    def getVitems(self):
        return self.vItems
    def getrItems(self):
        return self.rItems
    def getloadItems(self):
        return self.loadItems

    def removeVsourceElement(self, vsource):
        self.componentCount -= 1
        self.vItems.remove(vsource)
    def removeResistorElement(self, resistor):
        self.componentCount -= 1
        self.rItems.remove(resistor)
    def removeLoadElement(self, load):
        self.componentCount -= 1
        self.loadItems.remove(load)

    def getNumComponents(self):
        return Circuit.componentCount
    def getNumVsourceElements(self):
        return VoltageSource.vSourceCount
    def getNumResistors(self):
        return Resistor.resistorCount
    def getNumLoads(self):
        return Load.loadCount
