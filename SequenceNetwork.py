import Constants
import numpy as np
import cmath
from System import System
class SequenceNetwork:
    def __init__(self, system: System):
        self.system = system
        # pull in local transformation constant alpha from Constants.py
        self.a = Constants.ALPHA
        # create transfromation matrix used in sequence networks
        self.transformMatrix = np.matrix([[1, 1, 1],
                                [1, self.a**2, self.a],
                                [1, self.a, self.a**2]
                                ])
        self.seq0v = None
        self.seq1v = None
        self.seq2v = None
        self.build_voltage_sequence()

    def build_voltage_sequence(self):
        for bus_name, bus in self.system.buses.items():
            index = bus.index
            v_a = complex(bus.vk, bus.delta1)
            Vseq = np.zeros((3, 3), dtype=complex)
            Vseq = self.transformMatrix * v_a








