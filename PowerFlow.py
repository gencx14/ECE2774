import cmath as cmath
import numpy as np
from Ybus import Ybus
from Bus import Bus


class PowerFlow:

    def __init__(self, ybus: Ybus):
        # number of buses in system not including slack bus
        self.N = Bus.count

        # bringing in previously calculated admittance matrix
        self.ybus = ybus

        # column vector of bus Ps and bus Qs except for generator bus Q and no slack values
        self.y = [[0], [-1.1], [-1.0], [-1.0], [0], [2.0], [0], [-0.5], [-0.7], [-0.65], [0]]

        # empty matrix of calculated Ps and Qs, will be filled by power_mismatch method
        self.f_x = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]

        # initial column vector of bus deltas and voltages, empty now but filled in flat start function
        self.x = np.zeros((2 * self.N), 1)

        # power mismatch matrix
        self.dy_x = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]

        # Jacobian quadrant J1
        self.J1 = np.zeros((self.N, self.N))

        # Jacobian quadrant J2, one less column due to no V7
        self.J2 = np.zeros((self.N, self.N - 1))

        # Jacobian quadrant J3, one less row due to no Q7
        self.J3 = np.zeros((self.N - 1, self.N))

        # Jacobian quadrant J4, one less row and one less column due to no V7 and no Q7
        self.J4 = np.zeros((self.N - 1, self.N - 1))

    def flat_start(self):
        k = 0       # fills x vector with 0.0 for deltas and 1.0 for voltages
        while k < 2 * self.N:
            if k <= 6:
                self.x[k] = 0
            else:
                self.x[k] = 1.0



    # Uses power injection equations to fill f(x), then calculates power mismatch
    def power_mismatch(self):
        # filling Pk and Qk
        # first round of summations for Pk and Qk as V1 and d1 are not in the x vector
        k = 0
        while k < self.N - 1:
            # calculates Pk when n = 1
            self.f_x[k][0] = (self.x[k + self.N][0] * abs(self.ybus.Y_matrix[k + 1][0]) * self.V1 *
                              cmath.cos(self.x[k][0] - self.d1 - cmath.phase(self.ybus.Y_matrix[k + 1][0])))

            # calculates Qk when n = 1
            self.f_x[k + self.N][0] = (self.x[k + self.N][0] * abs(self.ybus.Y_matrix[k + 1][0]) * self.V1 *
                                       cmath.sin(self.x[k][0] - self.d1 - cmath.phase(self.ybus.Y_matrix[k + 1][0])))

            k = k + 1  # at the end of this set of while loops, k should become 5 and the loop terminates

        k = 0
        while k < self.N - 1:        # k runs from 0 -> 4, so it fills f_x 0 up to but not including 5
            n = 0
            while n < self.N - 1:
                # calculates Pk
                self.f_x[k][0] = self.f_x[k][0] + (self.x[k+self.N][0] * abs(self.ybus.Y_matrix[k+1][n+1]) * self.x[n+self.N][0] *
                                                   cmath.cos(self.x[k][0] - self.x[n][0] - cmath.phase(self.ybus.Y_matrix[k+1][n+1])))

                # calculates Qk
                self.f_x[k + self.N][0] = self.f_x[k + self.N][0] + (self.x[k + self.N][0] * abs(self.ybus.Y_matrix[k+1][n+1]) * self.x[n][0] *
                                                                     cmath.sin(self.x[k][0] - self.x[n][0] - cmath.phase(self.ybus.Y_matrix[k+1][n+1])))

                n = n + 1
            k = k + 1       # at the end of this set of while loops, k should become 5 and the loop terminates

        # first sum of P7 since V1 and d1 aren't in the x vector
        self.f_x[k][0] = self.V7 * abs(self.ybus.Y_matrix[k][0]) * self.V1 * \
                         cmath.cos(self.x[k][0] - self.d1 - cmath.phase(self.ybus.Y_matrix[k][0]))

        # while loop to fill P7 specifically, as V7 isn't included in the x matrix
        n = 0
        while n < self.N:
            self.f_x[k][0] = self.f_x[k][0] + (self.V7 * abs(self.ybus.Y_matrix[k][n]) * self.x[n][0] *
                                               cmath.cos(self.x[k][0] - self.x[n][0] - cmath.phase(self.ybus.Y_matrix[k][n])))
            n = n + 1

        # Pk and Qk values populated into f(x) matrix
        # Now solving for power mismatch
        k = 0
        while k < 11:
            self.dy_x[k][0] = (self.y[k][0]).real - (self.f_x[k][0]).real
            k = k + 1

    '''def fill_j1(self):
        k = 0
        while k < self.N - 1:
            n = 0
            while n < self.N-1:
                J1[k][n] = '''
    def jacobian(self):
        pass


    def temp_out(self):
        for inner_list in self.dy_x:
            for element in inner_list:
                print(element, end=" ")
            print()
