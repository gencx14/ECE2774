import numpy as n

class Transformer:
    #Constant Values
    #Angular Frequency in Hz
    w = 377

    #Imaginary Number
    j = 1j

    #Power Base in MVA
    S_Base = 100

    def __init__(self, Transformer: str, Bus1: str, Bus2: str, RatedPower: float, V1: float, V2: float, Z: float, XR: float):
        #Transformer Name
        self.Transformer: str = Transformer

        #Transformer Power Rating
        self.RatedPower: float = RatedPower

        #Rated Voltage 1
        self.V1: float = V1

        #Rated Voltage 2
        self.V2: float = V2

        #Transformer Impedance in pu
        self.Z: float = Z

        #Transformer X/R Ratio
        self.XR: float = XR

        #Transformer Bus1 Connection
        self.Bus1: str = Bus1

        # Transformer Bus2 Connection
        self.Bus2: str = Bus2

        #Base Voltage as High Side Voltage
        self.V_Base = V2

        #R + jX
        self.R = self.Z * ((self.V2 ** 2) / self.RatedPower) / (self.V_Base * (self.V_Base / Transformer.S_Base)) * n.cos(n.arctan(self.XR))
        self.X = self.Z * ((self.V2 ** 2) / self.RatedPower) / (self.V_Base * (self.V_Base / Transformer.S_Base)) * n.sin(n.arctan(self.XR))