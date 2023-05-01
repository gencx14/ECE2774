from System import System
from YbusFormation import YbusFormation
from PowerFlow import PowerFlow
from SequenceNetwork import SequenceNetwork
class Solution:
    def __init__(self, system: System):
        self.system = system
        self.ybusobj = YbusFormation(self.system)
        self.ybus = self.ybusobj.ymatrix
        self.ybus0 = self.ybusobj.Ybus0
        self.ybus1 = self.ybusobj.Ybus1
        self.ybus2 = self.ybusobj.Ybus2
        self.bus_voltages = []
        self.pf = PowerFlow(self.ybus, self.system)
        self.Sequence = SequenceNetwork(self.system)
        print()



    def print_nodal_voltages(self):
        print("Bus A voltage: {}\nBus B voltage: {}".format(self.bus_voltages[0], self.bus_voltages[1]))



