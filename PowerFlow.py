import cmath as cmath
import numpy as np
from Ybus import Ybus
from Bus import Bus


class PowerFlow:

    def __init__(self, ybus: Ybus):
        # number of buses in system not including slack bus
        self.N = Bus.count - 1

        # bringing in previously calculated admittance matrix
        self.ybus = ybus

        # start with a matrix of every P and Q, then use an if statement to cut down to only Load P and Q and PV bus P
        # the rows that contain PV Qs need to also be cut out of the Jacobian

        '''# vector of every P, Q
        self.y1 = np.zeros(1, self.N)

        value = 0
        for key in self.ybus.network.buses:
            self.tempP = self.ybus.network.buses[key].P
            self.tempQ = self.ybus.network.buses[key].Q
            if self.ybus.network.buses[key].bustype != 'slack' and self.ybus.network.buses[key].bustype != 'PV':
                self.y1[0][value] = self.tempP
                self.y1[0][value + self.N] = self.tempQ'''

        # matrix of bus Ps and bus Qs except for generator bus Q
        self.y = [[0], [-110], [-100], [-100], [-0], [200], [0], [-50], [-70], [-65], [0]]

        # empty matrix of calculated Ps and Qs, will be filled by power_mismatch method
        self.f_x = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]

        # matrix of bus deltas and bus Vs except for generator bus V as it is given
        self.x = [[0], [0], [0], [0], [0], [0], [1], [1], [1], [1], [1]]

        # voltage on the generator bus, added as a member to be easily updated and used in power injection equations
        self.V7 = 1

        # voltage on slack bus
        self.V1 = 1

        # delta on slack bus
        self.d1 = 0

        # power mismatch matrix
        self.dy_x = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]

    # Uses power injection equations to fill f(x), then calculates power mismatch
    def power_mismatch(self):
        # filling Pk and Qk
        # first round of summations for Pk and Qk as V1 and d1 are not in the x vector
        k = 0
        while k < self.N - 1:
            # calculates Pk when n = 1
            self.f_x[k][0] = (self.x[k + self.N][0] * abs(self.ybus.Y_matrix[k + 1][0]) * self.V1 * cmath.cos(self.x[k][0] - self.d1 - (cmath.phase(self.ybus.Y_matrix[k + 1][0] * 180 / cmath.pi))))

            # calculates Qk when n = 1
            self.f_x[k + self.N][0] = (self.x[k + self.N][0] * abs(self.ybus.Y_matrix[k + 1][0]) * self.V1 * cmath.sin(self.x[k][0] - self.d1 - (cmath.phase(self.ybus.Y_matrix[k + 1][0] * 180 / cmath.pi))))

            k = k + 1  # at the end of this set of while loops, k should become 5 and the loop terminates

        k = 0
        while k < self.N - 1:        # k runs from 0 -> 4, so it fills f_x 0 up to but not including 5
            n = 0
            while n < self.N - 1:
                # calculates Pk
                self.f_x[k][0] = self.f_x[k][0] + (self.x[k+self.N][0] * abs(self.ybus.Y_matrix[k+1][n+1]) * self.x[n+self.N][0] * cmath.cos(self.x[k][0] - self.x[n][0] - (cmath.phase(self.ybus.Y_matrix[k+1][n+1]) * 180 / cmath.pi)))

                # calculates Qk
                self.f_x[k + self.N][0] = self.f_x[k + self.N][0] + (self.x[k + self.N][0] * abs(self.ybus.Y_matrix[k+1][n+1]) * self.x[n][0] * cmath.sin(self.x[k][0] - self.x[n][0] - (cmath.phase(self.ybus.Y_matrix[k+1][n+1]) * 180 / cmath.pi)))

                n = n + 1
            k = k + 1       # at the end of this set of while loops, k should become 5 and the loop terminates

        # first sum of P7 since V1 and d1 aren't in the x vector
        self.f_x[k][0] = self.V7 * abs(self.ybus.Y_matrix[k][0]) * self.V1 * cmath.cos(self.x[k][0] - self.d1 - (cmath.phase(self.ybus.Y_matrix[k][0]) * 180 / cmath.pi))

        # while loop to fill P7 specifically, as V7 isn't included in the x matrix
        n = 0
        while n < self.N:
            self.f_x[k][0] = self.f_x[k][0] + (self.V7 * abs(self.ybus.Y_matrix[k][n]) * self.x[n][0] * cmath.cos(self.x[k][0] - self.x[n][0] - (cmath.phase(self.ybus.Y_matrix[k][n])  * 180 / cmath.pi)))
            n = n + 1

        # Pk and Qk values populated into f(x) matrix
        # Now solving for power mismatch
        k = 0
        while k < 11:
            self.dy_x[k][0] = (self.y[k][0]).real - (self.f_x[k][0]).real
            k = k + 1

    def temp_out(self):
        for inner_list in self.dy_x:
            for element in inner_list:
                print(element, end=" ")
            print()
