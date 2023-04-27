from Bus import Bus
from Bundles import Bundles
from Generator import Generator
from Geometry import Geometry
from Line import Line
from Transformer import Transformer

from typing import Dict, List

import numpy as n
import sys

class YBus:
    #Imaginary Number
    j = 1j

    def __init__(self, YBus: str):
        #YBus Name
        self.Ybus: str = YBus

        #Empty List of Buses
        self.BusOrder: List[str] = list()

        #Empty Dictionary of Bus Names
        self.Buses: Dict[str, Bus] = dict()

        #Empty Dictionary of Line Names
        self.Lines: Dict[str, Line] = dict()

        #Empty Dictionary of Transformer Names
        self.Transformers: Dict[str, Transformer] = dict()

        #Empty Dictionary of Generator Names
        self.Generators: Dict[str, Generator] = dict()

    def calculate_YBus_Matrix(self):
        #d = 1.5in
        #Bundles = 2

        #ASCR Table
        #r = 0.321in, GMR = 0.0216ft, R = 0.465

        #Zero Matrix Size of Number of Buses
        YBus_Matrix = n.zeros((len(self.BusOrder), len(self.BusOrder)), dtype = complex)

        #Admittances for Network on Non-Diagonals, y = -1/Z
        #T1 Connected Bus 1 and Bus 2
        YBus_Matrix[0][1] = -1 / (self.Transformers["T1"].R + (YBus.j * self.Transformers["T1"].X))

        #L2 Connected Bus 2 and Bus 3
        YBus_Matrix[1][2] = -1 / (self.Lines["L2"].Rpu + (YBus.j * self.Lines["L2"].X))

        #L1 Connected Bus 4 and Bus 2
        YBus_Matrix[3][1] = -1 / (self.Lines["L1"].Rpu + (YBus.j * self.Lines["L1"].X))

        #L3 Connected Bus 5 and Bus 3
        YBus_Matrix[4][2] = -1 / (self.Lines["L3"].Rpu + (YBus.j * self.Lines["L3"].X))

        #L6 Connected Bus 5 and Bus 4
        YBus_Matrix[4][3] = -1 / (self.Lines["L6"].Rpu + (YBus.j * self.Lines["L6"].X))

        #L4 Connected Bus 6 and Bus 4
        YBus_Matrix[5][3] = -1 / (self.Lines["L4"].Rpu + (YBus.j * self.Lines["L4"].X))

        #L5 Connected Bus 6 and Bus 4
        YBus_Matrix[5][4] = -1 / (self.Lines["L5"].Rpu + (YBus.j * self.Lines["L5"].X))

        #T2 Connected Bus 7 and Bus 6
        YBus_Matrix[6][5] = -1 / (self.Transformers["T2"].R + (YBus.j * self.Transformers["T2"].X))

        #Symmetrical Elements
        YBus_Matrix[1][0] = YBus_Matrix[0][1]
        YBus_Matrix[2][1] = YBus_Matrix[1][2]
        YBus_Matrix[1][3] = YBus_Matrix[3][1]
        YBus_Matrix[2][4] = YBus_Matrix[4][2]
        YBus_Matrix[3][4] = YBus_Matrix[4][3]
        YBus_Matrix[3][5] = YBus_Matrix[5][3]
        YBus_Matrix[4][5] = YBus_Matrix[5][4]
        YBus_Matrix[5][6] = YBus_Matrix[6][5]

        #Diagonal Elements
        YBus_Matrix[0][0] = -YBus_Matrix[0][1]
        YBus_Matrix[1][1] = -YBus_Matrix[0][1] - YBus_Matrix[1][3] - YBus_Matrix[1][2] + ((YBus.j * self.Lines["L1"].Cpu) / 2) + ((YBus.j * self.Lines["L2"].Cpu) / 2)
        YBus_Matrix[2][2] = -YBus_Matrix[1][2] - YBus_Matrix[2][4] - YBus_Matrix[1][2] + ((YBus.j * self.Lines["L2"].Cpu) / 2) + ((YBus.j * self.Lines["L3"].Cpu) / 2)
        YBus_Matrix[3][3] = -YBus_Matrix[3][1] - YBus_Matrix[3][5] - YBus_Matrix[3][4] + ((YBus.j * self.Lines["L1"].Cpu) / 2) + ((YBus.j * self.Lines["L4"].Cpu) / 2)
        YBus_Matrix[4][4] = -YBus_Matrix[2][4] - YBus_Matrix[4][5] - YBus_Matrix[3][4] + ((YBus.j * self.Lines["L3"].Cpu) / 2) + ((YBus.j * self.Lines["L5"].Cpu) / 2)
        YBus_Matrix[5][5] = -YBus_Matrix[5][3] - YBus_Matrix[5][4] - YBus_Matrix[6][5] + ((YBus.j * self.Lines["L4"].Cpu) / 2) + ((YBus.j * self.Lines["L5"].Cpu) / 2)
        YBus_Matrix[6][6] = -YBus_Matrix[5][6]

        return YBus_Matrix

        #Adds Bus if Bus not Already Created
        def addBus(self, Bus: str):
            if Bus not in self.Buses.keys():
                self.Buses[Bus] = Bus(Bus)
                self.BusOrder.append(Bus)

        #Adds Line and Bus Connection if Line not Already Created
        def addLine(self, Line: str, Length: float, LineGeometry: Geometry, LineBundle: Bundles, Bus1: str, Bus2, str, V_Base: float):
            if Line not in self.Lines.keys():
                V_Base = self.Transformers[list(self.Transfomers.keys())[0]].V2
                self.Lines[Line] = Line(Line, Length, LineGeometry, LineBundle, Bus1, Bus2, V_Base)
                self.addBus(Bus1)
                self.addBus(Bus2)

        #Adds Transformer and Bus Connection if Transformer not Already Created
        def addTransformer(self, Transformer: str, Bus1: str, Bus2: str, RatedPower: float, V1: float, V2: float, Z: float, XR: float):
            if Transformer not in self.Transformers.keys():
                self.Transformers[Transformer] = Transformer(Transformer, Bus1, Bus2, RatedPower, V1, V2, Z, XR)
                self.addBus(Bus1)
                self.addBus(Bus2)

        #Adds Generator and Bus Connection if Generator not Already Created
        def addGenerator(self, Generator: str, Bus: str, RatedPower: float):
            if Generator not in self.Generators.keys():
                self.Generators[Generator] = Generator(Generator, Bus, RatedPower)
                self.addBus(Bus)