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
        self.f_x = np.zeros(((2 * self.N), 1))

        # initial column vector of bus deltas and voltages, empty now but filled in flat start function
        self.x = np.zeros(((2 * self.N), 1))

        # power mismatch matrix
        self.dy_x = np.zeros((((2*self.N) - 3), 1))

        # Jacobian quadrant J1
        self.J1 = np.zeros((self.N, self.N))

        # Jacobian quadrant J2, one less column due to no V7
        self.J2 = np.zeros((self.N, self.N))

        # Jacobian quadrant J3, one less row due to no Q7
        self.J3 = np.zeros((self.N, self.N))

        # Jacobian quadrant J4, one less row and one less column due to no V7 and no Q7
        self.J4 = np.zeros((self.N, self.N))

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
        k = 0
        while k < 2 * self.N:
            n = 0
            while n < 2 * self.N:
                if k <= 6:
                    # calculates Pk
                    self.f_x[k][0] = self.f_x[k][0] + (self.x[k+self.N][0] * abs(self.ybus.Y_matrix[k][n]) * self.x[n+self.N][0] * cmath.cos(self.x[k][0] - self.x[n][0] - cmath.phase(self.ybus.Y_matrix[k][n])))
                    n = n + 1

                else:
                    # calculates Qk
                    self.f_x[k + self.N][0] = self.f_x[k + self.N][0] + (self.x[k + self.N][0] * abs(self.ybus.Y_matrix[k-self.N][n-self.N]) * self.x[n][0] * cmath.sin(self.x[k][0] - self.x[n][0] - cmath.phase(self.ybus.Y_matrix[k-self.N][n-self.N])))
                    n = n + 1

            k = k + 1

        # Pk and Qk values populated into f(x) matrix
        # Cutting out unnecessary P and Q in f_x for slack and voltage controlled bus
        k = (2*self.N) - 1
        for key in reversed(self.ybus.network.buses):
            if k >= 7:
                if self.ybus.network.buses[key].bustype == 1 or self.ybus.network.buses[key].bustype == 3:
                    np.delete(self.f_x[k][0])
                    k = k + 1
            else:
                if self.ybus.network.buses[key].bustype == 1:
                    np.delete(self.f_x[k][0])
                    k = k + 1

        # Calculating power mismatch
        k = 0
        while k < self.N - 1:
            self.dy_x[k][0] = (self.y[k][0]).real - (self.f_x[k][0]).real

    def fill_j1(self):
        k = 0
        while k < self.N - 1:
            n = 0
            while n < self.N-1:
                pass

    def fill_j2(self):
        pass

    def fill_j3(self):
        pass

    def fill_j4(self):
        pass

    def jacobian(self):
        # calling functions to fill quadrants
        self.fill_j1()
        self.fill_j2()
        self.fill_j3()
        self.fill_j4()
        # combine quadrants using block function
        # cut down necessary rows and columns, see how it was done in the power_mismatch section

    def temp_out(self):
        for inner_list in self.dy_x:
            for element in inner_list:
                print(element, end=" ")
            print()
