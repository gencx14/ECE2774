class Bus:

    count = 0       # counts number of busses in network

    def __init__(self, name):
        self.name = name
        Bus.count = Bus.count + 1  # Updates bus count on creation of new bus object

        self.index = Bus.count
        self.voltage = None

    def set_bus_voltage(self, voltage):     # function to set voltage of a bus
        self.voltage = voltage
