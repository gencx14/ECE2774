class Bus:

    count = 0       # counts number of busses in network

    def __init__(self, name):
        self.name = name
        Bus.count = Bus.count + 1  # Updates bus count on creation of new bus object

        self.index = Bus.count
        self.voltage = 0
        self.bustype = 0
        self.delta = 0
        self.P = 0
        self.Q = 0

    def set_bus_voltage(self, voltage):     # function to set voltage of a bus in per unit
        self.voltage = voltage

    def set_bus_type(self, bustype):   # sets the type of bus for power flow
        self.bustype = bustype         # 1 is slack, 2 is load, 3 is voltage controlled

    def set_delta(self, delta):     # sets the delta of the bus
        self.delta = delta

    def set_p(self, p):     # takes value in MW converts to W
        self.P = p * 10 ** 6

    def set_q(self, q):     # takes value in Mvar converts to W
        self.Q = q * 10 ** 6
