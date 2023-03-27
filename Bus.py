class Bus:

    count = 0       # counts number of busses in network

    def __init__(self, name):
        self.name = name
        Bus.count = Bus.count + 1  # Updates bus count on creation of new bus object

        self.index = Bus.count
        self.voltage = None
        self.bustype = None
        self.delta = None
        self.P = None
        self.Q = None

    def set_bus_voltage(self, voltage):     # function to set voltage of a bus
        self.voltage = voltage

    def set_bus_type(self, bustype: str):   # sets the type of bus for power flow
        self.bustype = bustype

    def set_delta(self, delta):     # sets the delta of the bus
        self.delta = delta

    def set_p(self, p):     # sets the P of the bus
        self.P = p

    def set_q(self, q):     # sets the Q of the bus
        self.Q = q
