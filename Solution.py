from System import System
from YbusFormation import YbusFormation
from PowerFlow import PowerFlow
class Solution:
    def __init__(self, system: System):
        self.system = system
        self.ybusobj = YbusFormation(self.system)
        self.ybus = self.ybusobj.ymatrix
        self.bus_voltages = []
        self.pf = PowerFlow(self.ybus, self.system)

    def do_power_flow(self):
        """
        current of system
            Z_load --> found in Load Class
            I = Vs/(Z_load + Resistance)
            Va = Vs
            Vb = Vs - I * R
            V_res = I * R
            V_load = I * Z_load

        """
        vsElements = self.circuit.getVitems()
        resElements = self.circuit.getrItems()
        loadElements = self.circuit.getloadItems()

        voltage = 0
        for e in vsElements:
            voltage += e.voltage

        zload = 0
        for e in loadElements:
            zload += e.loadResistance

        resistance = 0
        for e in resElements:
            resistance += e.resistance
        #Va = voltage
        self.bus_voltages.append(voltage)
        current = voltage / (zload + resistance)
        v_res = current * resistance
        vb = voltage - v_res
        #v_load = vb
        self.bus_voltages.append(vb)
        print('Source Voltage: {}\nVoltage Across Resistor: {}'.format(voltage, v_res))
        print('Voltage Across the Load: {}\nCurrent though Circuit: {}'.format(vb, current))

    def print_nodal_voltages(self):
        print("Bus A voltage: {}\nBus B voltage: {}".format(self.bus_voltages[0], self.bus_voltages[1]))



