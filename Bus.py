class Bus:

    count = 0       # counts number of busses in network

    def __init__(self, name):
        self.name = name
        self.index = Bus.count

        self.voltage = None

        Bus.count = Bus.count + 1       # Updates bus count on creation of new bus object
