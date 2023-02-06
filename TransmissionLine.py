from TransmissionLineData import TransmissionLineData


class TransmissionLine:

    def __init__(self, bus1, bus2, length, data: TransmissionLineData):
        self.data = data
        self.bus1 = bus1
        self.bus2 = bus2
        self.length = length

        self.buses = [self.bus1, self.bus2]
