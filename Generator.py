class Generator:
    generator_count = 0

    def __init__(self, name, voltage, bus1, bus2=None):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.voltage = voltage
        Generator.generator_count += 1

    def set_name(self, name):
        self.name = name

    def set_bus1(self, bus1):
        self.bus1 = bus1

    def set_voltage(self, voltage):
        self.voltage = voltage

    def get_name(self):
        return self.name

    def get_bus1(self):
        return self.bus1

    def get_voltage(self):
        return self.voltage
