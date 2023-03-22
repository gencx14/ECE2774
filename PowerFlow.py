import numpy as np
import cmath as cmath
from Ybus import Ybus


class PowerFlow:

    def __init__(self, ybus: Ybus):
        # bringing in previously calculated admittance matrix
        self.ybus = ybus
        # matrix of bus Ps and bus Qs except for generator bus Q
        self.y = [[0], [110], [100], [100], [0], [200], [0], [50], [70], [65], [0]]

        # empty matrix of calculated Ps and Qs, will be filled by power_mismatch method
        self.f_x = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]

        # matrix of bus deltas and bus Vs except for generator bus V as it is given
        self.x = [[0], [0], [0], [0], [0], [0], [1], [1], [1], [1], [1]]

        # voltage on the generator bus, added as a member to be easily updated and used in power injection equations
        self.V7 = 1

        # power mismatch matrix
        self.dy_x = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]

    # Uses power injection equations to fill f(x), then calculates power mismatch
    def power_mismatch(self):
        # filling Pk
        k = 0
        while k < 5:
            # summation for Pk
            n = 0
            while n < 5:
                self.f_x[k][0] = self.x[6+k][0] * abs(self.ybus.Y_matrix[k][n]) * self.x[6+n][0] * cmath.cos(self.x[k][0] - self.x[n][0] - cmath.phase(self.ybus.Y_matrix[k][n]))
                n = n + 1
            k = k + 1       # at the end of this set of while loops, k should be 5

        # while loop to fill P7 specifically, as V7 isn't included in the x matrix
        n = 0
        while n < 5:
            self.f_x[k][0] = self.V7 * abs(self.ybus.Y_matrix[k][n]) * self.x[6 + n][0] * cmath.cos(self.x[k][0] - self.x[n][0] - cmath.phase(self.ybus.Y_matrix[k][n]))
            n = n + 1
        k = k + 1

        # new while loop to fill Qk
        while k < 11:
            # summation for Qk, matrix positions 6 -> 10
            n = 0
            while n < 5:
                self.f_x[k][0] = self.x[k][0] * abs(self.ybus.Y_matrix[k-6][n]) * self.x[6 + n][0] * cmath.sin(self.x[k-6][0] - self.x[n][0] - cmath.phase(self.ybus.Y_matrix[k-6][n]))
                n = n + 1
            k = k + 1
        # Pk and Qk values populated into f(x) matrix

        # Now solving for power mismatch
        k = 0
        while k < 11:
            self.dy_x[k][0] = abs(self.y[k][0] - self.f_x[k][0])
            k = k + 1

    def temp_out(self):
        for inner_list in self.dy_x:
            for element in  inner_list:
                print(element, end=" ")
            print()
