from Geometry import Geometry
from Bundles import Bundles
import math as m

class Line:
    #Constant Values
    #Angular Frequency in Hz
    f = 60

    #Imaginary Number
    j = 1j

    #Power Base in MVA
    S_Base = 100

    def __init__(self, Line: str, Length: float, LineGeometry: Geometry, LineBundles: Bundles, Bus1: str, Bus2: str, V_Base: float):
        #Line Name
        self.Line: str = Line

        #Line Length
        self.Length: float = Length

        #Name of First Bus Connected to Line
        self.Bus1: str = Bus1

        #Name of Second Bus Connected to Line
        self.Bus2: str = Bus2

        #Voltage Base of Line
        self.V_Base: float = V_Base

        #DEQ Associated with Line's Phase Geometry
        self.DEQ = LineGeometry.DEQ

        #Transmission Line Parameters
        self.DSL = LineBundles.DSL
        self.DSC = LineBundles.DSC

        #Inductance H nad Capacitance F
        L = Line.findL(self)
        C = Line.findC(self)

        #Base Impedance from Base Voltage and Power Rating
        Z_Base = (self.V_Base ** 2) / Line.S_Base

        #Resistance in pu
        self.Rpu = (LineBundles.R / Z_Base) * self.Length

        #X in pu
        self.Xpu = ((L * Line.f * m.pi * 2) / Z_Base)

        #C in pu
        self.Cpu = ((C * Line.f * m.pi * 2) / Z_Base)

    #Line Inductance in H
    def findL(self):
        D = (self.DEQ * 12) / self.DSL
        L = 1609.34 * (2 * (10 ** (-7)) *m.log(D)) * self.Length
        return L

    #Line Capacitance in C
    def findC(self):
        D = (self.DEQ * 12) / self.DSC
        E0 = 8.85 * (10 ** (-12))
        C = 1609.34 * ((2 * m.pi * E0) / (m.log(D)))
        return C * self.Length