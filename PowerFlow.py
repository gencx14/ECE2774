import numpy as np
from Ybus import Ybus
from Bus import Bus
from Network import Network


class PowerFlow:

    def __init__(self, ybus: Ybus, network: Network):
        # number of buses in system not including slack bus
        self.N = Bus.count

        self.network = network

        # bringing in previously calculated admittance matrix
        self.y_matrix = ybus.Y_matrix

        # column vector of bus Ps and bus Qs except for generator bus Q and no slack values
        self.y = [[0], [-1.1], [-1.0], [-1.0], [0], [2.0], [0], [-0.5], [-0.7], [-0.65], [0]]

        # empty matrix of calculated Ps and Qs, will be filled by power_mismatch method
        self.f_x = np.zeros(((2 * self.N), 1))

        # initial column vector of bus deltas and voltages, empty now but filled in flat start function
        self.x = np.zeros(((2 * self.N), 1))

        # empty column vector to be filled by the output of J^-1 dot dy_x
        self.dx = np.zeros((len(self.x), 1))

        # empty column vector that will be filled with the new x values
        self.x_new = np.zeros((len(self.x), 1))

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
        # fills x vector with 0.0 for deltas and 1.0 for voltages
        for k in range(len(self.x)):
            if k <= 6:
                self.x[k] = 0
            else:
                self.x[k] = 1.0

    # Uses power injection equations to fill f(x), then calculates power mismatch
    def power_mismatch(self):
        # filling Pk and Qk
        for k in range(len(self.f_x)):
            n = 0
            while n < self.N:
                if k < self.N:
                    # calculates Pk
                    self.f_x[k][0] += (self.x[k+self.N][0] * abs(self.y_matrix[k][n]) * self.x[n+self.N][0] * np.cos(self.x[k][0] - self.x[n][0] - np.angle(self.y_matrix[k][n])))

                else:
                    # calculates Qk
                    self.f_x[k][0] += (self.x[k][0] * abs(self.y_matrix[k-self.N][n]) * self.x[n+self.N][0] * np.sin(self.x[k-self.N][0] - self.x[n][0] - np.angle(self.y_matrix[k-self.N][n])))

                n = n + 1

        # Trimming f_x to match the length of y
        k = 2 * self.N - 1
        w = 0
        while w < 2:
            for key in reversed(self.network.buses):
                if self.network.buses[key].bustype == 1:
                    self.f_x = np.delete(self.f_x, k, axis=0)
                    k = k - 1
                elif self.network.buses[key].bustype == 3 and k > 6:
                    self.f_x = np.delete(self.f_x, k, axis=0)
                    k = k - 1
                else:
                    k = k - 1
            w = w + 1

        # Calculating power mismatch
        for k in range(len(self.dy_x)):
            self.dy_x[k][0] = self.y[k][0] - self.f_x[k][0]

    def j1_diagonal(self, k):
        w = 0
        num = 0
        while w < self.N:
            if k != w:
                num += (abs(self.y_matrix[k][w]) * self.x[w + self.N][0] * np.sin(self.x[k][0] - self.x[w][0] - np.angle(self.y_matrix[k][w])))
                w = w + 1
            else:
                w = w + 1
        return num * -1 * self.x[k + self.N]

    def j2_diagonal(self, k):
        w = 0
        num = 0
        while w < self.N:
            num += (abs(self.y_matrix[k][w]) * self.x[w + self.N][0] * np.cos(self.x[k][0] - self.x[w][0] - np.angle(self.y_matrix[k][w])))
            w = w + 1
        return num + (self.x[k + self.N][0] * abs(self.y_matrix[k][k]) * np.cos(np.angle(self.y_matrix[k][k])))

    def j3_diagonal(self, k):
        w = 0
        num = 0
        while w < self.N:
            if k != w:
                num += (abs(self.y_matrix[k][w]) * self.x[w + self.N][0] * np.cos(self.x[k][0] - self.x[w][0] - np.angle(self.y_matrix[k][w])))
                w = w + 1
            else:
                w = w + 1
        return num * self.x[k + self.N]

    def j4_diagonal(self, k):
        w = 0
        num = 0
        while w < self.N:
                num += (abs(self.y_matrix[k][w]) * self.x[w + self.N][0] * np.sin(self.x[k][0] - self.x[w][0] - np.angle(self.y_matrix[k][w])))
                w = w + 1
        return num + (-1 * self.x[k + self.N] * abs(self.y_matrix[k][k]) * np.sin(np.angle(self.y_matrix[k][k])))

    def fill_j1(self):
        k = 0
        while k < self.N:
            n = 0
            while n < self.N:
                if k != n:
                    self.J1[k][n] = self.x[k + self.N][0] * abs(self.y_matrix[k][n]) * self.x[n + self.N][0] * np.sin(self.x[k][0] - self.x[n][0] - np.angle(self.y_matrix[k][n]))
                    n = n + 1
                else:
                    self.J1[k][n] = self.j1_diagonal(k)
                    n = n + 1
            k = k + 1

    def fill_j2(self):
        k = 0
        while k < self.N:
            n = 0
            while n < self.N:
                if k != n:
                    self.J2[k][n] = self.x[k + self.N][0] * abs(self.y_matrix[k][n]) * np.cos(self.x[k][0] - self.x[n][0] - np.angle(self.y_matrix[k][n]))
                    n = n + 1
                else:
                    self.J2[k][n] = self.j2_diagonal(k)
                    n = n + 1
            k = k + 1

    def fill_j3(self):
        k = 0
        while k < self.N:
            n = 0
            while n < self.N:
                if k != n:
                    self.J3[k][n] = -1 * self.x[k + self.N][0] * abs(self.y_matrix[k][n]) * self.x[n + self.N][0] * np.cos(self.x[k][0] - self.x[n][0] - np.angle(self.y_matrix[k][n]))
                    n = n + 1
                else:
                    self.J3[k][n] = self.j3_diagonal(k)
                    n = n + 1
            k = k + 1

    def fill_j4(self):
        k = 0
        while k < self.N:
            n = 0
            while n < self.N:
                if k != n:
                    self.J4[k][n] = self.x[k + self.N][0] * abs(self.y_matrix[k][n]) * np.sin(self.x[k][0] - self.x[n][0] - np.angle(self.y_matrix[k][n]))
                    n = n + 1
                else:
                    self.J4[k][n] = self.j4_diagonal(k)
                    n = n + 1
            k = k + 1

    def jacobian(self):

        # calling functions to fill quadrants
        self.fill_j1()
        self.fill_j2()
        self.fill_j3()
        self.fill_j4()

        # combine quadrants using block function
        self.J = np.block([[self.J1, self.J2], [self.J3, self.J4]])

        # cut down necessary rows. Rows involving P1, Q1, and Q7 should be removed
        k = (self.N * 2) - 1
        w = 0
        while w < 2:
            for key in reversed(self.network.buses):
                if self.network.buses[key].bustype == 1:
                    self.J = np.delete(self.J, k, axis=0)
                    k = k - 1
                elif self.network.buses[key].bustype == 3 and k > 6:
                    self.J = np.delete(self.J, k, axis=0)
                    k = k - 1
                else:
                    k = k - 1
            w = w + 1

        # cut down necessary columns
        n = (self.N * 2) - 1
        w = 0
        while w < 2:
            for key in reversed(self.network.buses):
                if self.network.buses[key].bustype == 1:
                    self.J = np.delete(self.J, n, axis=1)
                    n = n - 1
                elif self.network.buses[key].bustype == 3 and n > 6:
                    self.J = np.delete(self.J, n, axis=1)
                    n = n - 1
                else:
                    n = n - 1
            w = w + 1
        # J should be filled with proper rows and columns cut out

    def calculate_mismatch(self):
        # calculating dx
        self.dx = np.dot(np.linalg.inv(self.J), self.dy_x)

        # padding dx vector with zeros for values related to a slack or voltage controlled bus

