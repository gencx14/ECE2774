from Bus import Bus
from Resistor import Resistor
from Bundle import Bundle
from Conductor import Conductor
from Generator import Generator
from Geometry import Geometry
from Load import Load
from Transformer import Transformer
from TransformerData import TransformerData
from TransmissionLine import TransmissionLine
from TransmissionLineData import TransmissionLineData
from BaseValues import BaseValues
from typing import Dict
from typing import List


class System:
    componentCount = 0
    SystemCount = 0
    dataCount = 0

    def __init__(self, name: str, pbase, vbase):
        self.name: str = name
        self.ybus = None
        self.bases = BaseValues(pbase, vbase)  # check on this if it gets messed up.
        # makes a list of the bus order and ensures that they are entered as strings
        self.buses_order: List[str] = list()
        # make a dictionary of string and bus objects
        self.buses: Dict[str, Bus] = dict()
        # make a dictionary of the admittance elements
        self.y_elements: Dict = dict()
        # make a dictionary for voltage source objects. VItemms will only accept Voltage Source objects, if no voltage
        # source is assigned then it will be given the value none
        self.generatorItems: Dict = dict()
        # make a dictionary for the resistor elements
        self.rItems: Dict[str, Resistor] = dict()
        # make a dictionary for the load elements
        self.loadItems: Dict[str, Load] = dict()
        # make a dictionary for your conductor elements
        self.conductors: Dict[str, Conductor] = dict()
        # make a dictionary for the geometries we have
        self.geometries: Dict[str, Geometry] = dict()
        # make a dictinoary for the bundles we have
        self.bundles: Dict[str, Bundle] = dict()
        # make a dictionary for the pure resistor items we have
        self.resistors: Dict[str, Resistor] = dict()
        # make a dictionary for the transformer data entreis
        self.transformerdataItems: Dict[str, TransformerData] = dict()
        # make a dictionary for the transformer items
        self.transformers: Dict[str, Transformer] = dict()
        # make a dictionary for transmission lines
        self.transmissionlines: Dict[str: TransmissionLine] = dict()
        # make a dictionary for transmission line data (Partridge)
        self.transmissionlineDataItems: Dict[str: TransmissionLineData] = dict()
        System.SystemCount += 1

    def add_bus(self, bus):
        if bus not in self.buses.keys():
            self.buses[bus] = Bus(bus)
            self.buses_order.append(bus)

    def add_generator(self, name, voltage, bus1):
        if name not in self.generatorItems.keys():
            self.generatorItems[name] = Generator(name, voltage, bus1, self.bases)
            self.add_bus(bus1)
            self.buses[bus1].setBusVoltage(voltage)
            System.componentCount += 1

    def add_conductor(self, name, outerDiameter, gmr, rAC, ampacity=None):
        if name not in self.conductors.keys():
            self.conductors[name] = Conductor(name, outerDiameter, gmr, rAC, ampacity)


    def add_geometry(self, name: str, ax, ay, bx, by, cx, cy):
        if name not in self.geometries.keys():
            self.geometries[name] = Geometry(name, ax, ay, bx, by, cx, cy)

    def add_bundle(self, name, bundleSize, bundleDistance, conductor: Conductor):
        if name not in self.bundles.keys():
            self.bundles[name] = Bundle(name, bundleSize, bundleDistance, conductor)

    def add_transformer(self, name: str, bus1, bus2, txData: TransformerData):
        if name not in self.transformers.keys():
            self.transformers[name] = Transformer(name, bus1, bus2, txData)
            self.y_elements[name] = Transformer(name, bus1, bus2, txData)
            self.add_bus(bus1)
            self.add_bus(bus2)
            System.componentCount += 1

    def add_transformerData(self, name, sRated, vPrimary, vSecondary, zPctTransformer, xrRatio):
        if name not in self.transformerdataItems.keys():
            self.transformerdataItems[name] = TransformerData(name, sRated, vPrimary, vSecondary, zPctTransformer,
                                                              xrRatio, self.bases)

    def add_transmissionLine(self, name: str, bus1, bus2, lineData: TransmissionLineData, length):
        if name not in self.transmissionlines.keys():
            self.transmissionlines[name] = TransmissionLine(name, bus1, bus2, lineData, length, self.bases)
            self.y_elements[name] = TransmissionLine(name, bus1, bus2, lineData, length, self.bases)
            self.add_bus(bus1)
            self.add_bus(bus2)
            System.componentCount += 1

    def add_transmissionLineData(self, name: str, bundle: Bundle, geometry: Geometry, conductor: Conductor):
        if name not in self.transmissionlineDataItems.keys():
            self.transmissionlineDataItems[name] = TransmissionLineData(name, bundle, geometry, conductor)

    def add_resistorElement(self, name, bus1_name, bus2_name, ohms):
        if name not in self.resistors.keys():
            self.resistors[name] = Resistor(name, bus1_name, bus2_name, ohms)
            self.add_bus(bus1_name)
            self.add_bus(bus2_name)
            System.componentCount += 1

    def add_loadElement(self, name, bus_name, power, voltage):
        if name not in self.loadItems.keys():
            self.loadItems[name] = Load(name, bus_name, power, voltage)
            self.add_bus(bus_name)
            System.componentCount += 1

    def set_bus(self, key, type, v1 = 0, d1 = 0, p = 0, q = 0):
        self.buses[key].type = type
        self.buses[key].vk = v1
        self.buses[key].delta1 = d1
        self.buses[key].pk = p * 1e6 / self.bases.pbase
        self.buses[key].qk = q * 1e6 /self.bases.pbase
        self.buses[key].getBusTypeCount()

