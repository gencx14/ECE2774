from TransmissionLineData import TransmissionLineData
import math


class TransmissionLine:

    p_base = 100       # target apparent power base is 100MVA
    v_base = 230       # voltage base is 230kV
    z_rated = v_base**2/p_base    # impedance base
    y_rated = 1/z_rated     # admittance base
    j = math.sqrt(-1)

    def __init__(self, name, bus1, bus2, length, data: TransmissionLineData):
        self.name = name
        self.data = data
        self.bus1 = bus1
        self.bus2 = bus2
        self.length = length
        self.R = data.R * self.length / TransmissionLine.z_rated      # Resistance of line in pu
        self.X = data.L * self.length * data.w / TransmissionLine.z_rated     # Reactance of line in pu
        self.B = data.C * self.length * data.w / TransmissionLine.y_rated      # Shunt admittance of line in pu
        self.y = 1/(self.R + (TransmissionLine.j * self.X))     # Admittance of line
