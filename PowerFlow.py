import math as math
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

        # Jacobian quadrants
        self.J1 = np.zeros((self.N, self.N))
        self.J2 = np.zeros((self.N, self.N))
        self.J3 = np.zeros((self.N, self.N))
        self.J4 = np.zeros((self.N, self.N))

        # The Jacobian
        self.J = np.zeros((self.N * 2, self.N * 2))

    def flat_start(self):
        k = 0       # fills x vector with 0.0 for deltas and 1.0 for voltages
        while k < 2 * self.N:
            if k <= 6:
                self.x[k] = 0
                k = k + 1
            else:
                self.x[k] = 1.0
                k = k + 1

    # Uses power injection equations to fill f(x), then calculates power mismatch
    def power_mismatch(self):
        # filling Pk and Qk
        k = 0
        while k < 2 * self.N:
            n = 0
            while n < self.N:
                if k < 6:
                    # calculates Pk
                    self.f_x[k][0] = self.f_x[k][0] + (self.x[k+self.N][0] * abs(self.ybus.Y_matrix[k][n]) * self.x[n+self.N][0] * math.cos(self.x[k][0] - self.x[n][0] - math.phase(self.ybus.Y_matrix[k][n])))
                    n = n + 1

                else:
                    # calculates Qk
                    self.f_x[k][0] = self.f_x[k][0] + (self.x[k][0] * abs(self.ybus.Y_matrix[k-self.N][n]) * self.x[n+self.N][0] * math.sin(self.x[k][0] - self.x[n][0] - math.phase(self.ybus.Y_matrix[k-self.N][n])))
                    n = n + 1

            k = k + 1

        # Calculating power mismatch
        k = (2*self.N) - 1
        for key in reversed(self.ybus.network.buses):
            if self.ybus.network.buses[key].bustype == 1 or self.ybus.network.buses[key].bustype == 3:
                self.f_x = np.delete(self.f_x, k, axis=0)
                k = k - 1
            else:
                k = k - 1

        for key in reversed(self.ybus.network.buses):
            if self.ybus.network.buses[key].bustype == 1:
                self.f_x = np.delete(self.f_x, k, axis=0)
                k = k - 1
            else:
                k = k - 1

        # Calculating power mismatch
        k = 0
        while k < self.N - 1:
            self.dy_x[k][0] = self.y[k][0] - self.f_x[k][0]
            k = k + 1

    def fill_j1(self):
        k = 0
        while k < self.N - 1:
            n = 0
            while n < self.N - 1:
                if k == n:
                    self.J1[k][n] = 0
                else:
                    self.J1[k][n] = self.x[k+self.N][0] * abs(self.ybus.Y_matrix[k][n]) * self.x[n+self.N][0] * math.sin(self.x[k][0] - self.x[n][0] - math.phase(self.ybus.Y_matrix[k][n]))

    def fill_j2(self):
        k = 0
        while k < self.N - 1:
            n = 0
            while n < self.N - 1:
                if k == n:
                    self.J2[k][n] = 0
                else:
                    self.J2[k][n] = self.x[k + self.N][0] * abs(self.ybus.Y_matrix[k][n]) * math.cos(self.x[k][0] - self.x[n][0] - math.phase(self.ybus.Y_matrix[k][n]))

    def fill_j3(self):
        k = 0
        while k < self.N - 1:
            n = 0
            while n < self.N - 1:
                if k == n:
                    self.J3[k][n] = 0
                else:
                    self.J3[k][n] = -1 * self.x[k + self.N][0] * abs(self.ybus.Y_matrix[k][n]) * self.x[n + self.N][0] * math.cos(self.x[k][0] - self.x[n][0] - math.phase(self.ybus.Y_matrix[k][n]))

    def fill_j4(self):
        k = 0
        while k < self.N - 1:
            n = 0
            while n < self.N - 1:
                if k == n:
                    self.J4[k][n] = 0
                else:
                    self.J4[k][n] = self.x[k + self.N][0] * abs(self.ybus.Y_matrix[k][n]) * math.sin(self.x[k][0] - self.x[n][0] - math.phase(self.ybus.Y_matrix[k][n]))

    def jacobian(self):
        # calling functions to fill quadrants
        self.fill_j1()
        self.fill_j2()
        self.fill_j3()
        self.fill_j4()

        # combine quadrants using block function
        self.J = np.block([self.J1, self.J2], [self.J3, self.J4])

        # cut down necessary rows and columns, see how it was done in the power_mismatch section


    def temp_out(self):
        for inner_list in self.dy_x:
            for element in inner_list:
                print(element, end=" ")
            print()
