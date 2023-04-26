import numpy as np
import cmath as cmath
from Ybus import Ybus
from Bus import Bus
from Network import Network


class PowerFlow:

    def __init__(self, ybus: Ybus, network: Network):
        # number of buses in system not including slack bus
        self.N = Bus.count

        # power base of system
        self.sbase = 100 * 10**6

        # voltage base of system
        self.vbase = 230 * 10**3

        # current base
        self.ibase = self.sbase / (self.vbase * np.sqrt(3))

        self.network = network

        # bringing in previously calculated admittance matrix
        self.y_matrix = ybus.Y_matrix

        # column vector of bus Ps and bus Qs except for generator bus Q and no slack values
        self.y = np.zeros(((2 * self.N) - 3, 1))

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

        # The new x vector
        self.x_new = np.zeros((len(self.x), 1))

        # tolerance of the system
        self.tolerance = 0

        # matrix to store current flow between buses
        self.I_flow = np.zeros((self.N, self.N), dtype=complex)

        # total losses in the system
        self.total_losses = 0

        # power flowing through lines
        self.power_flow = np.zeros((self.N, self.N), dtype=complex)

    def fill_y(self):
        k = 0
        for w in range(2):
            for key in self.network.buses:
                if self.network.buses[key].bustype == 1:
                    continue
                elif k < 7:
                    self.y[k] = self.network.buses[key].P / self.sbase
                    k = k + 1
                elif k >= 7 and self.network.buses[key].bustype == 3:
                    continue
                else:
                    self.y[k] = self.network.buses[key].Q / self.sbase
                    k = k + 1

    def flat_start(self):
        # fills x vector with 0.0 for deltas and 1.0 for voltages
        for k in range(len(self.x)):
            if k <= 6:
                self.x[k] = 0.0
            else:
                self.x[k] = 1.00

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
        for w in range(2):
            for key in reversed(self.network.buses):
                if self.network.buses[key].bustype == 1:
                    self.J = np.delete(self.J, k, axis=0)
                    k = k - 1
                elif self.network.buses[key].bustype == 3 and k > 6:
                    self.J = np.delete(self.J, k, axis=0)
                    k = k - 1
                else:
                    k = k - 1

        # cut down necessary columns
        n = (self.N * 2) - 1
        for w in range(2):
            for key in reversed(self.network.buses):
                if self.network.buses[key].bustype == 1:
                    self.J = np.delete(self.J, n, axis=1)
                    n = n - 1
                elif self.network.buses[key].bustype == 3 and n > 6:
                    self.J = np.delete(self.J, n, axis=1)
                    n = n - 1
                else:
                    n = n - 1
        # J should be filled with proper rows and columns cut out

    def calculate_mismatch(self):
        # calculating dx
        self.dx = np.dot(np.linalg.inv(self.J), self.dy_x)

        # combining x with dx to update x vector to new values
        k = 0  # iterator for x vector
        i = 0     # iterator for dx vector
        for w in range(2):
            for key in self.network.buses:
                if k < 7:
                    if self.network.buses[key].bustype == 1:
                        self.x_new[k] = self.x[k]
                        k = k + 1
                    else:
                        self.x_new[k] = self.x[k] + self.dx[i]
                        k = k + 1
                        i = i + 1
                else:
                    if self.network.buses[key].bustype == 1 or self.network.buses[key].bustype == 3:
                        self.x_new[k] = self.x[k]
                        k = k + 1
                    else:
                        self.x_new[k] = self.x[k] + self.dx[i]
                        k = k + 1
                        i = i + 1

    def set_tolerance(self, tolerance):
        self.tolerance = tolerance

    def Newton_Raphson(self):

        # calculating change in y, reset f_x vector -> without resetting f_x, there is an out-of-bounds indexing issue
        self.f_x = np.zeros(((2 * self.N), 1))

        self.power_mismatch()

        # if mismatch is within tolerance, end recursion, calculate necessary values
        if np.amax(abs(self.dy_x)) < self.tolerance:
            return

        else:
            # building Jacobian
            self.jacobian()

            # calculating change in x
            self.calculate_mismatch()

            # updating x to the new value
            self.x = self.x_new

            # running Newton Raphson again
            return self.Newton_Raphson()

    def output_voltages(self):
        i = 0
        print("The voltages and angles at the buses in order are:")
        while i < self.N:
            print("V" + str(i+1) + " = " + str(self.x[i+self.N]) + " at an angle d" + str(i+1) + " = " + str(self.x[i]))
            i = i + 1
        k = 0
        for key in self.network.buses:
            if self.network.buses[key].bustype == 1:
                k = k + 1
                continue

            elif self.network.buses[key].bustype == 3:
                self.network.buses[key].delta = self.x[k]
                k = k + 1

            else:
                self.network.buses[key].voltage = self.x[k + self.N]
                self.network.buses[key].delta = self.x[k]
                k = k + 1

    # This function will set the voltages and angles for the buses based on the previous calculations
    def update_buses(self):
        k = 0
        for key in self.network.buses:
            if self.network.buses[key].bustype == 1:
                k = k + 1
                continue
            elif self.network.buses[key].bustype == 3 and k <= 6:
                self.network.buses[key].set_delta(self.x[k][0])
                k = k + 1
            else:
                self.network.buses[key].set_delta(self.x[k][0])
                self.network.buses[key].set_bus_voltage(self.x[k + self.N][0])
                k = k + 1

    def calculate_current_flow(self):
        # Calculating per unit current
        for i in range(self.N):
            for j in range(self.N):
                self.I_flow[i][j] = ((cmath.rect(self.x[j + self.N][0], self.x[j][0]) - cmath.rect(self.x[i + self.N][0], self.x[i][0])) * self.y_matrix[i][j])

        # putting current values into proper lines
        self.network.lines['L1'].set_current(self.I_flow[1][3])
        self.network.lines['L2'].set_current(self.I_flow[1][2])
        self.network.lines['L3'].set_current(self.I_flow[2][4])
        self.network.lines['L4'].set_current(self.I_flow[3][5])
        self.network.lines['L5'].set_current(self.I_flow[4][5])
        self.network.lines['L6'].set_current(self.I_flow[3][4])

        '''for key in self.network.lines:
            print(abs(self.network.lines[key].current))'''

    def calculate_losses(self):
        # Calculate losses in transmission lines in pu
        for key in self.network.lines:
            p_loss = (abs(self.network.lines[key].current)) ** 2 * self.network.lines[key].R
            self.network.lines[key].set_ploss(p_loss * 100)
            self.total_losses += p_loss

        # Calculate secondary currents in transformers
        self.network.transformers['T1'].i_secondary = abs(self.network.lines['L1'].current) + abs(self.network.lines['L2'].current)
        self.network.transformers['T2'].i_secondary = abs(self.network.lines['L4'].current) + abs(self.network.lines['L5'].current)

        # Calculating power loss in transformers
        self.network.transformers['T1'].loss = self.network.transformers['T1'].i_secondary ** 2 * (1/self.network.transformers['T1'].y).real
        self.network.transformers['T2'].loss = self.network.transformers['T2'].i_secondary ** 2 * (1 / self.network.transformers['T2'].y).real
        self.total_losses += self.network.transformers['T1'].loss + self.network.transformers['T2'].loss

    def flow_of_power(self):
        # Calculate the power flowing through each line using and taking the real part of the result
        for i in range(self.N):
            for j in range(self.N):
                self.power_flow[i][j] = self.x[i + self.N] * self.I_flow[i][j].conjugate()
        # Assigning values from self.power_flow to the proper lines
        self.network.lines['L1'].power_flow = abs(np.real(self.power_flow[1][3]))
        self.network.lines['L2'].power_flow = abs(np.real(self.power_flow[1][2]))
        self.network.lines['L3'].power_flow = abs(np.real(self.power_flow[2][4]))
        self.network.lines['L4'].power_flow = abs(np.real(self.power_flow[3][5]))
        self.network.lines['L5'].power_flow = abs(np.real(self.power_flow[4][5]))
        self.network.lines['L6'].power_flow = abs(np.real(self.power_flow[3][4]))

        # Power in each line is correct, checked with this loop
        '''for key in self.network.lines:
            print(self.network.lines[key].power_flow * 100)'''

    def slack_pv_calculations(self):
        # Calculating P and Q of slack bus
        self.network.buses['bus1'].set_p(self.network.transformers['T1'].loss + self.network.lines['L1'].power_flow + self.network.lines['L2'].power_flow)
        print(self.network.buses['bus1'].P)
        

    