from System import System
from YbusFormation import YbusFormation
from ZbusFormation import ZbusFormation
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
        self.zbusobj = ZbusFormation(self.system, self.ybusobj)
        self.zbus = self.zbusobj.Zbus
        self.zbus1 = self.zbusobj.Zbus1
        self.zbus2 = self.zbusobj.Zbus2
        self.zbus0 = self.zbusobj.Zbus0
        # self.Sequence = SequenceNetwork(self.system)
        print()



    def print_nodal_voltages(self):
        print("Bus A voltage: {}\nBus B voltage: {}".format(self.bus_voltages[0], self.bus_voltages[1]))



