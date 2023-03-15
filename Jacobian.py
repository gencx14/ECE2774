import numpy as np
from Ybus import Ybus

class Jacobian:

    def __init__(self, ybus: Ybus):
        # bringing in previously calculated admittance matrix
        self.ybus = ybus
        # matrix of bus Ps and bus Qs except for generator bus Q
        self.y = [[0], [110], [100], [100], [0], [200], [0], [50], [70], [65], [0]]

        # empty matrix of calculated Ps and Qs, complex because of Q, will be filled by powerinjections method
        self.f_x = np.zeros((11,1), dtype= complex)

        # matrix of bus deltas and bus Vs except for generator bus V as it is given
        self.x = [[0], [0], [0], [0], [0], [0], [1], [1], [1], [1], [1]]

        def powerinjections(self):
            # filling Pk
            k = 0
            while k < 6:
                # summation for Pk
            # then iterate K
            # new while loop to fill Qk
            # summation for Qk
            # iterate K
        # function ends with Pk and Qk values populated



