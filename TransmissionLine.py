from TransmissionLineData import TransmissionLineData


class TransmissionLine:

    def __init__(self, bus1, bus2, length, data: TransmissionLineData):
        self.data = data
        self.bus1 = bus1
        self.bus2 = bus2
        self.length = length
        self.R = data.R * self.length       # Resistance of line in Ohms
        self.X = data.L * self.length * data.w       # Reactance of line in Ohms
        self.G = data.C * self.length * data.w       # Shunt admittance of line

        self.buses = [self.bus1, self.bus2]
