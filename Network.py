from typing import Dict, List
from TransmissionLineData import TransmissionLineData
from TransformerData import TransformerData
from TransmissionLine import TransmissionLine
from Transformer import Transformer
from Generator import Generator
from Geometry import Geometry
from Bus import Bus


class Network:
    def __init__(self, name: str):
        self.name: str = name
        self.buses_order: List[str] = list()    # stores names of buses
        self.buses: Dict[str, Bus] = dict()     # stores buses with their data
        self.line_data: Dict[str, TransmissionLineData] = dict()     # stores types of transmission line data
        self.lines: Dict[str, TransmissionLine] = dict()    # stores transmission lines
        self.geometries: Dict[str, Geometry] = dict()
        self.transformer_data: Dict[str, TransformerData] = dict()
        self.transformers: Dict[str, Transformer] = dict()      # stores transformers and their data
        self.generators: Dict[str, Generator] = dict()      # stores generators and their data
        self.n = len(self.buses_order)      # n = number of buses in the network

    def add_bus(self, bus_name):
        if bus_name not in self.buses.keys():
            self.buses[bus_name] = Bus(bus_name)
            self.buses_order.append(bus_name)

    def add_geometry(self, name, x1, y1, x2, y2, x3, y3):      # put positions in array, pass array, cuts down on inputs
        if name not in self.geometries.keys():
            self.geometries[name] = Geometry(name, x1, y1, x2, y2, x3, y3)

    def add_transmission_line_type(self, name, bundle_num, line_geometry: Geometry, gmr, diam, d, rac):
        if name not in self.line_data.keys():
            self.line_data[name] = TransmissionLineData(name, bundle_num, line_geometry, gmr, diam, d, rac)

    def add_transmission_line(self, name, bus1, bus2, length, data: TransmissionLineData):
        if name not in self.lines.keys():
            self.lines[name] = TransmissionLine(name, bus1, bus2, length, data)
            self.add_bus(bus1)
            self.add_bus(bus2)

    def add_transformer_type(self, name, p_rated, v_rated_high, v_rated_low, z_pct, x_r):
        if name not in self.transformer_data.keys():
            self.transformer_data[name] = TransformerData(name, p_rated, v_rated_high, v_rated_low, z_pct, x_r)

    def add_transformer(self, name: str, data: TransformerData, bus1, bus2):
        if name not in self.transformers.keys():
            self.transformers[name] = Transformer(name, data, bus1, bus2)
            self.add_bus(bus1)
            self.add_bus(bus2)

    def add_generator(self, name, voltage, bus1):
        if name not in self.generators.keys():
            self.generators[name] = Generator(name, voltage, bus1)
            self.add_bus(bus1)
