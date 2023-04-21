from TransmissionLineData import TransmissionLineData


class TransmissionLine:

    p_base = 100       # target apparent power base is 100MVA
    v_base = 230       # voltage base is 230kV
    z_rated = v_base ** 2 / p_base    # impedance base
    y_rated = 1/z_rated     # admittance base
    j = complex(0, 1)

    def __init__(self, name, bus1, bus2, length, data: TransmissionLineData):
        self.name = name
        self.data = data
        self.bus1 = bus1
        self.bus2 = bus2
        self.length = length
        self.R = data.R * self.length / TransmissionLine.z_rated      # Resistance of line in pu
        self.X = (self.j * data.L * self.length * data.w) / TransmissionLine.z_rated    # Reactance of line in pu
        self.B = self.j * data.C * self.length * data.w / TransmissionLine.y_rated      # Shunt admittance of line in pu
        self.y = 1/(self.R + self.X)     # Admittance of line
        self.current = None
        self.loss = None
        self.power_flow = None

    def set_current(self, i):
        self.current = i

    def set_ploss(self, ploss):
        self.loss = ploss

    def set_power_flow(self, flow):
        self.power_flow = flow
