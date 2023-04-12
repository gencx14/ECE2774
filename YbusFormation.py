from System import System
import numpy as np


class YbusFormation:

    def __init__(self, system: System):
        self.system = system
        self.ymatrix = None
        self.numBusses = len(self.system.buses)
        self.ymatrix = np.zeros((len(self.system.buses), len(self.system.buses)), dtype=complex) # creates an n by n matrix of 0s
        self.bus_order = list()
        self.fillYbus()

    def fillYbus(self):
        for element_name, element in self.system.y_elements.items():
            for row in element.buses:
                for col in element.buses:
                    index_row = self.system.buses[row].index
                    index_col = self.system.buses[col].index

                    self.ymatrix[index_row, index_col] = self.ymatrix[index_row, index_col] + element.y.loc[row, col]


""""  This was my first attempt but the above method is much more succinct and brief

    def fillYbusMatrix(self):
        for n in range(len(self.system.buses)):
            for k in range(len(self.system.buses)):
                if n == k:
                    #solve the kk method
                    #loop through all of the transmission lines **** NEED TO MAKE TLINES PU BEFORE THIS********
                    tline_y = 0
                    tx_y = 0
                    for i in range(len(self.system.transmissionlines)):
                        #if the bus for the tLine is the bus we are currently on then add its series and 1/2 its shunt to the node
                        if ((self.system.transmissionlines[tline_order[n]].bus1 == self.system.buses_order[n]) and (self.system.transmissionlines[tline_order[k]].bus1 == self.system.buses_order[k])) or ((self.system.transmissionlines[tline_order[n]].bus2 == self.system.buses_order[n]) and (self.system.transmissionlines[tline_order[k]].bus2 == self.system.buses_order[k])):
                            tline_y = tline_y + self.system.transmissionlines[tline_order[n]].totalYseries + self.system.transmissionlines[tline_order[n]].halfYshunt
                    for i in range(len(self.system.transformers))
                        if ((self.system.transformers[tx_order[n]].bus1 == self.system.buses_order[n]) and (self.system.transformers[tx_order[k]].bus1 == self.system.buses_order[k])) or ((self.system.transformers[tx_order[n]].bus2 == self.system.buses_order[n]) and (self.system.transformers[tx_order[k]].bus2 == self.system.buses_order[k])):
                            tx_y = tx_y + self.system.transformers[tx_order[n]].data.txYpu
                    self.yBusMatrix[n][k] = tline_y + tx_y
                        #loop thorugh your tx and tline and loop through to identify the busses, if bus = bus we are searching for then add them
                        #look up lists comprehension
                else:
                    #solve for kn method
                    self.yBusMatrix[n][k] =

"""

# form a [Bus.busCount]i [Bus.busCount]k matrix
# do a loop through k inside a loop through i. In the inner loop have an if statement that if i == k do the Ykk
#  calculation. If i != k then do the Ykn calculation and store the value in the [i][k] spot in the matrix.
