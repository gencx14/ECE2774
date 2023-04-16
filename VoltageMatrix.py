import cmath

from System import System
import numpy as np

class VoltageMatrix:

    def __init__(self, system: System):
        self.system = system
        self.voltagematrix = None
        self.numBusses = len(self.system.buses)
        self.voltagematrix = np.zeros((len(self.system.buses), len(self.system.buses)), dtype=complex)  # creates an n by n matrix of 0s
        self.bus_order = list()
        self.fillVoltageMatrix()

    def fillVoltageMatrix(self):
        for element_name, element in self.system.y_elements.items():
            for row in element.buses:
                for col in element.buses:
                    index_row = self.system.buses[row].index
                    index_col = self.system.buses[col].index

                    if index_row == index_col:
                        self.voltagematrix[index_row, index_col] = complex(cmath.rect(self.system.buses[row].vk, self.system.buses[row].delta1))
                    else:
                        self.voltagematrix[index_row, index_col] = complex(cmath.rect(self.system.buses[row].vk, self.system.buses[row].delta1) - cmath.rect(self.system.buses[col].vk, self.system.buses[col].delta1))

