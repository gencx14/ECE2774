from typing import Dict, List, Optional
from Resistor import Resistor
from Load import Load
from Generator import VoltageSource
from Bus import Bus
class Circuit:
    componentCount = 0
    CircuitCount = 0

    def __init__(self, name: str):
        self.name: str = name
        self.buses_order: List[str] = list() #makes a list of the bus order and ensures that they are entered as strings
        #make a dictionary of string and bus objects
        self.buses: Dict[str, Bus] = dict()
        #make a dictionary of the admittance elements
        self.g_elements: Dict = dict()
        #make a dictionary for voltage source objects. VItemms will only accept Voltage Source objects, if no voltage source is assigned then it will be given the value none
        self.vItems: Optional[VoltageSource] = None
        #make a dictionary for the resistor elements
        self.rItems: Dict[str, Resistor] = dict()
        #make a dictionary for the load elements
        self.loadItems: Dict[str, Load] = dict()
        Circuit.CircuitCount += 1

    def add_bus(self, bus):
        if bus not in self.buses.keys():
            self.buses[bus] = Bus(bus)
            self.buses_order.append(bus)

    def addVsourceElement(self, name, bus1, voltage):
        Circuit.componentCount += 1
        self.vsource = VoltageSource(name, bus1, voltage)
        self.add_bus(bus1)
        #access the bus in the buses dictionary with the key bus1 and set its voltage to V
        self.buses[bus1].setBusVoltage(voltage)
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
