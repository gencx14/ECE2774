from System import System
from YbusFormation import YbusFormation

class ZbusFormation:

    def __init__(self, system: System, ybus: YbusFormation):
        self.system = system
        self.ybus = ybus
        # Zbus from original Ybus
        self.Zbus = 1 / self.ybus.ymatrix
        self.Zbus1 = 1 / self.ybus.Ybus1
        self.Zbus2 = 1 / self.ybus.Ybus2
        self.Zbus0 = 1 / self.ybus.Ybus0
