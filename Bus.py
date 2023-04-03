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

    def set_bus_voltage(self, voltage):     # function to set voltage of a bus
        self.voltage = voltage

    def set_bus_type(self, bustype):   # sets the type of bus for power flow
        self.bustype = bustype         # 1 is slack, 2 is load, 3 is voltage controlled

    def set_delta(self, delta):     # sets the delta of the bus
        self.delta = delta

    def set_p(self, p):     # sets the P of the bus
        self.P = p

    def set_q(self, q):     # sets the Q of the bus
        self.Q = q
